'use client';  // Mark this as a client-side React component

import { useState } from 'react';   // React hook for managing local state
import DropZone from './DropZone';  // Component to upload/select a document
import ChatBox from './ChatBox';    // Component to ask questions about the uploaded document

export default function DocumentChatWrapper() {
  // State to store the currently selected/uploaded document's ID
  const [documentId, setDocumentId] = useState(null);

  return (
    <div className="space-y-6">
      {/* DropZone component handles file upload and updates documentId via setDocumentId */}
      <DropZone setDocumentId={setDocumentId} />

      {/* Render ChatBox only if a documentId is set (i.e., after a document is uploaded/selected) */}
      {documentId && <ChatBox documentId={documentId} />}
    </div>
  );
}
