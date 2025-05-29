from rest_framework import serializers
from .models import Document, Chunk, Query

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'file_type', 'file_size', 'num_pages',
            'processing_status', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_at', 'updated_at']


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = [
            'id', 'document', 'content', 'vector_id',
            'chunk_index', 'page_start', 'page_end', 'created_at'
        ]
        read_only_fields = ['created_at']


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id', 'document', 'question', 'answer', 'created_at']
        read_only_fields = ['created_at']
