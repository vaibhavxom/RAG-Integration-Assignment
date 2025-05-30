//documetchatwrapper.js 
'use client';
import { useState } from 'react';
import DropZone from './DropZone';
import ChatBox from './ChatBox';

export default function DocumentChatWrapper() {
  const [documentId, setDocumentId] = useState(null);

  return (
    <div className="space-y-6">
      <DropZone setDocumentId={setDocumentId} />
      {documentId && <ChatBox documentId={documentId} />}
    </div>
  );
}

