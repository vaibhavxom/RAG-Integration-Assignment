// Import the main wrapper component that handles document upload and chat
import DocumentChatWrapper from '@/components/DocumentChatWrapper';

export default function Home() {
  return (
    // Main container with max width, centered horizontally, with vertical and horizontal padding
    <main className="max-w-3xl mx-auto py-10 px-4">
      {/* Page title with large bold font and margin below */}
      <h1 className="text-3xl font-bold mb-6">📄 Document Intelligence Platform</h1>

      {/* Include the DocumentChatWrapper component which manages file upload and Q&A */}
      <DocumentChatWrapper />
    </main>
  );
}
