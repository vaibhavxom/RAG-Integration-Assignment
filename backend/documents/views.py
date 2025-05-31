# Standard library imports
import os
import logging

# PDF and DOCX processing
import fitz  # PyMuPDF for reading PDFs
from docx import Document as DocxDocument

# For sending HTTP requests to LM Studio API
import requests

# Django REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Importing models and serializers
from .models import Document, Chunk, Query
from .serializers import DocumentSerializer, ChunkSerializer, QuerySerializer

# For generating text embeddings
from sentence_transformers import SentenceTransformer

# ChromaDB vector database
import chromadb

# Set up logging
logger = logging.getLogger(__name__)

# Load sentence transformer model for text embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.Client(
    chromadb.config.Settings(persist_directory="./chroma_db")
)

# Function to extract text from uploaded file (PDF, DOCX, TXT)
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif ext == '.docx':
        doc = DocxDocument(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# Function to split long text into smaller chunks (smartly, paragraph-based)
def smart_chunk_text(text, max_chunk_size=500):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_chunk_size:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Function to call LM Studio's local API and get a language model response
def ask_lm_studio(prompt):
    LM_STUDIO_API_URL = "http://localhost:1234/v1/completions"
    payload = {
        "model": "mistralai/mathstral-7b-v0.1",  # Model to use
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": None,
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0].get("text", "").strip()
        else:
            logger.error(f"LM Studio response missing choices: {data}")
            return "No valid response from LM Studio."
    except Exception as e:
        logger.exception("Error calling LM Studio")
        return f"Error contacting LM Studio API: {str(e)}"

# API View to handle document uploads
@permission_classes([AllowAny])
class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            file_path = document.file.path
            try:
                # Extract metadata
                document.file_type = os.path.splitext(file_path)[1].lower()
                document.file_size = os.path.getsize(file_path)
                if document.file_type == '.pdf':
                    document.num_pages = fitz.open(file_path).page_count
                else:
                    document.num_pages = 0
                document.processing_status = 'processing'
                document.save()
            except Exception as e:
                logger.error(f"Metadata extraction failed: {e}")
                document.processing_status = 'failed'
                document.save()
                return Response({'error': f'Metadata extraction failed: {str(e)}'}, status=400)

            try:
                # Extract full text from document
                full_text = extract_text(file_path)
            except Exception as e:
                logger.error(f"Text extraction failed: {e}")
                document.processing_status = 'failed'
                document.save()
                return Response({'error': f'Text extraction failed: {str(e)}'}, status=400)

            # Split text into chunks
            chunks = smart_chunk_text(full_text)

            try:
                # Create vector collection and store embeddings
                collection = chroma_client.get_or_create_collection(name=f"doc_{document.id}")
                for i, chunk in enumerate(chunks):
                    embedding = model.encode(chunk).tolist()
                    vector_id = f"{document.id}_{i}"
                    collection.add(documents=[chunk], embeddings=[embedding], ids=[vector_id])
                    Chunk.objects.create(document=document, content=chunk, vector_id=vector_id, chunk_index=i)
                document.processing_status = 'processed'
                document.save()
            except Exception as e:
                logger.error(f"Chunk storage or embedding error: {e}")
                document.processing_status = 'failed'
                document.save()
                return Response({'error': f'Chunk storage failed: {str(e)}'}, status=500)

            return Response(DocumentSerializer(document).data, status=201)

        else:
            logger.error(f"Invalid serializer data: {serializer.errors}")
            return Response(serializer.errors, status=400)

# API view to list all documents
class DocumentListView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# API view to ask question related to a document
@permission_classes([AllowAny])
class AskQuestionView(APIView):
    def get(self, request):
        return Response({"message": "AskQuestionView GET works!"})

    def post(self, request):
        document_id = request.data.get('document_id')
        question = request.data.get('question')
        top_k = int(request.data.get('top_k', 3))

        # Validate input
        if not document_id or not question:
            return Response({'error': 'document_id and question are required.'}, status=400)

        try:
            # Retrieve vector collection for the document
            collection = chroma_client.get_collection(name=f"doc_{document_id}")
        except Exception:
            return Response({'error': 'Vector collection not found.'}, status=404)

        try:
            # Generate embedding for the question and perform similarity search
            question_embedding = model.encode(question).tolist()
            results = collection.query(query_embeddings=[question_embedding], n_results=top_k)
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return Response({'error': f'Error during vector search: {str(e)}'}, status=500)

        # Prepare the context from top-k retrieved chunks
        retrieved_chunks = results['documents'][0]
        chunk_ids = results['ids'][0]
        context = "\n\n".join([f"[{cid}]: {chunk}" for cid, chunk in zip(chunk_ids, retrieved_chunks)])

        # Prepare prompt for LM Studio
        prompt = f"""You are a helpful assistant answering based on the following document excerpts:

{context}

Question: {question}

Answer with reference to the chunks like [chunk_id] if needed.
"""

        # Get the answer from the language model
        answer = ask_lm_studio(prompt)

        # Save query to DB
        Query.objects.create(document_id=document_id, question=question, answer=answer)

        return Response({
            'question': question,
            'answer': answer,
            'sources': chunk_ids
        })
