//chatbox.js
'use client';
import { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

export default function ChatBox({ documentId }) {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim() || !documentId) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/documents/ask/', {
        document_id: documentId,
        question: question,
      });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("Failed to get response from server.");
    }
    setLoading(false);
  };

  return (
    <div className="mt-8 space-y-4">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        rows={4}
        className="w-full p-2 border rounded"
        placeholder="Ask a question about your document..."
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        {loading ? 'Asking...' : 'Ask AI'}
      </button>

      {answer && (
  <div className="mt-4 p-4 bg-gray-100 border rounded-md">
    <strong className="text-green-700 block mb-2">AI Response:</strong>
    <div className="prose prose-sm">
      <ReactMarkdown>{answer}</ReactMarkdown>
    </div>
  </div>
    )}
    </div>
  );
}
