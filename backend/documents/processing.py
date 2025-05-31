import os
import fitz  # PyMuPDF, used for extracting text from PDF files
from docx import Document as DocxDocument  # For reading .docx files

# Function to extract text from a file based on its extension
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()  # Get file extension (e.g., .pdf, .docx)
    text = ""

    try:
        # Extract text from PDF
        if ext == '.pdf':
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()  # Append text from each page

        # Extract text from DOCX (Word document)
        elif ext == '.docx':
            doc = DocxDocument(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"  # Append paragraph text with newline

        # Extract text from TXT file
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()  # Read entire text file content

        # Raise error for unsupported file types
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        # Raise runtime error if any exception occurs during extraction
        raise RuntimeError(f"Failed to extract text: {str(e)}")

    return text  # Return the extracted text


# Function to split text into smart chunks based on paragraph and max size
def smart_chunk_text(text, max_chunk_size=500):
    # Remove empty lines and strip whitespace
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

    chunks = []  # List to store chunks
    current_chunk = ""  # Buffer for current chunk

    for para in paragraphs:
        # Check if adding this paragraph stays within max_chunk_size
        if len(current_chunk) + len(para) + 1 <= max_chunk_size:
            current_chunk += para + "\n"  # Add paragraph to current chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())  # Save current chunk
            current_chunk = para + "\n"  # Start new chunk

    # Add any remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks  # Return list of smart text chunks
