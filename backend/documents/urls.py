from django.urls import path
from .views import DocumentListView, UploadDocumentView, AskQuestionView  # will add AskQuestionView soon

urlpatterns = [
    path('', DocumentListView.as_view(), name='document-list'),           # GET /documents/
    path('upload/', UploadDocumentView.as_view(), name='document-upload'),  # POST /documents/upload/
    path('ask/', AskQuestionView.as_view(), name='document-ask'),           # POST /documents/ask/
]
