from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site route (e.g., http://localhost:8000/admin/)
    path('admin/', admin.site.urls),

    # Include URLs from the 'documents' app (e.g., http://localhost:8000/documents/)
    path('documents/', include('documents.urls')),
]

# Serve media files during development (when DEBUG=True)
# Allows access to uploaded files via MEDIA_URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
