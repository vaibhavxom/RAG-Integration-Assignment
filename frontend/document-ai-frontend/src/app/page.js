//page.js
import DocumentChatWrapper from '@/components/DocumentChatWrapper';

export default function Home() {
  return (
    <main className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">📄 Document Intelligence Platform</h1>
      <DocumentChatWrapper />
    </main>
  );
}
