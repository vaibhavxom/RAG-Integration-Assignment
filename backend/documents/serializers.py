from rest_framework import serializers
from .models import Document, Chunk, Query

# Serializer for the Document model
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document  # Specifies which model this serializer is for
        fields = [  # Fields to be included in serialization/deserialization
            'id', 'title', 'file', 'file_type', 'file_size', 'num_pages',
            'processing_status', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_at', 'updated_at']  # These fields are read-only

# Serializer for the Chunk model
class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk  # Specifies which model this serializer is for
        fields = [  # Fields to be included in serialization/deserialization
            'id', 'document', 'content', 'vector_id',
            'chunk_index', 'page_start', 'page_end', 'created_at'
        ]
        read_only_fields = ['created_at']  # This field is read-only

# Serializer for the Query model
class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query  # Specifies which model this serializer is for
        fields = ['id', 'document', 'question', 'answer', 'created_at']  # Included fields
        read_only_fields = ['created_at']  # This field is read-only
