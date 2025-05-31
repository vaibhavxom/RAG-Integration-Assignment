from django.db import models
from django.utils import timezone

# Model to store uploaded documents and their metadata
class Document(models.Model):
    title = models.CharField(max_length=255)  # Title of the document
    file = models.FileField(upload_to='uploads/')  # File upload location
    file_type = models.CharField(max_length=50, blank=True, null=True)  # Type of file (e.g., PDF, DOCX)
    file_size = models.PositiveIntegerField(blank=True, null=True)  # File size in bytes
    num_pages = models.PositiveIntegerField(blank=True, null=True)  # Number of pages (mainly for PDFs)
    
    # Processing status to track the state of document analysis
    processing_status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('error', 'Error')
        ]
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when uploaded
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update
    
    def __str__(self):
        return self.title  # String representation of the document


# Model to store individual text chunks extracted from a document
class Chunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks'  # Allows reverse lookup: document.chunks.all()
    )
    content = models.TextField()  # Content of the chunk
    vector_id = models.CharField(max_length=255)  # Vector ID used in ChromaDB or similar system
    chunk_index = models.PositiveIntegerField(default=0)  # Order of the chunk in the document
    
    # Estimated page range this chunk belongs to
    page_start = models.PositiveIntegerField(blank=True, null=True)
    page_end = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp when chunk was created
    
    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"  # Helpful representation


# Model to store questions asked about a document and the generated answers
class Query(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='queries'  # Allows reverse lookup: document.queries.all()
    )
    question = models.TextField()  # User's question about the document
    answer = models.TextField()  # Answer generated for the question
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the query

    def __str__(self):
        return f"Query on {self.document.title} at {self.created_at}"  # Useful representation
