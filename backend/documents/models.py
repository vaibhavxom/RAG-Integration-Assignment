from django.db import models
from django.utils import timezone

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'pdf', 'docx'
    file_size = models.PositiveIntegerField(blank=True, null=True)  # in bytes
    num_pages = models.PositiveIntegerField(blank=True, null=True)  # for PDFs
    processing_status = models.CharField(
        max_length=20,
        default='pending',
        choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('error', 'Error')]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    vector_id = models.CharField(max_length=255)  # ID used in ChromaDB
    chunk_index = models.PositiveIntegerField(default=0)  # Index of chunk
    page_start = models.PositiveIntegerField(blank=True, null=True)  # Estimated start page
    page_end = models.PositiveIntegerField(blank=True, null=True)    # Estimated end page
    created_at = models.DateTimeField(default=timezone.now)

    

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"


class Query(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='queries')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query on {self.document.title} at {self.created_at}"
