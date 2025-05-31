from django.urls import path
from .views import DocumentListView, UploadDocumentView, AskQuestionView  # Import views

urlpatterns = [
    # Route to list all documents (GET request)
    path('', DocumentListView.as_view(), name='document-list'),  # Example: GET /documents/

    # Route to upload a new document (POST request with file data)
    path('upload/', UploadDocumentView.as_view(), name='document-upload'),  # Example: POST /documents/upload/

    # Route to ask a question related to a document (POST request with question and document ID)
    path('ask/', AskQuestionView.as_view(), name='document-ask'),  # Example: POST /documents/ask/
]
