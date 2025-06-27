'use client'; // Mark this as a client component to enable React hooks and client-only logic

import { useState } from 'react'; // Import useState to manage local component state
import DropZone from './DropZone'; // Component to handle file uploads
import dynamic from 'next/dynamic'; // Import dynamic to support client-only rendering

// Dynamically import ChatBox and disable server-side rendering (SSR)
// This is critical to prevent hydration mismatch errors in Next.js
const ChatBox = dynamic(() => import('./ChatBox'), {
  ssr: false, // Ensures ChatBox is only rendered on the client, avoiding SSR issues
});

export default function DocumentChatWrapper() {
  // Local state to store the uploaded document's ID
  const [documentId, setDocumentId] = useState(null);

  return (
    <div className="space-y-6">
      {/* File upload section */}
      {/* DropZone will upload the file and pass the documentId via setDocumentId */}
      <DropZone setDocumentId={setDocumentId} />

      {/* Conditionally render ChatBox only if a document is uploaded */}
      {/* This prevents rendering ChatBox without a valid document context */}
      {documentId && <ChatBox documentId={documentId} />}
    </div>
  );
}
