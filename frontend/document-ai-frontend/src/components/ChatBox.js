'use client'; // Enables React Server Components to treat this as a client component

import { useState } from 'react';      // React hook to manage local state
import axios from 'axios';             // HTTP client for making API requests
import ReactMarkdown from 'react-markdown'; // Allows rendering markdown syntax in response

// ChatBox component receives the documentId as a prop
export default function ChatBox({ documentId }) {
  // Local state variables
  const [question, setQuestion] = useState('');  // Holds the user's question
  const [answer, setAnswer] = useState('');      // Holds the AI's response
  const [loading, setLoading] = useState(false); // Indicates if a request is in progress

  // Function to handle the "Ask AI" button click
  const handleAsk = async () => {
    if (!question.trim() || !documentId) return;  // Do nothing if input is empty or documentId missing
    setLoading(true);  // Show loading indicator

    try {
      // Send a POST request to the Django backend to ask a question
      const res = await axios.post('http://localhost:8000/documents/ask/', {
        document_id: documentId,  // Pass the document ID
        question: question,       // Pass the user's question
      });

      // Set the answer from the response
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err); // Log error in console for debugging
      setAnswer("Failed to get response from server."); // Show fallback message
    }

    setLoading(false); // Reset loading state
  };

  return (
    <div className="mt-8 space-y-4">
      {/* Text area for user input */}
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)} // Update question on change
        rows={4}
        className="w-full p-2 border rounded"
        placeholder="Ask a question about your document..."
      />

      {/* Ask AI button */}
      <button
        onClick={handleAsk}
        disabled={loading} // Disable while loading
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        {loading ? 'Asking...' : 'Ask AI'} {/* Button text changes based on loading state */}
      </button>

      {/* Display AI answer if available */}
      {answer && (
        <div className="mt-4 p-4 bg-gray-100 border rounded-md">
          <strong className="text-green-700 block mb-2">AI Response:</strong>
          <div className="prose prose-sm">
            <ReactMarkdown>{answer}</ReactMarkdown> {/* Render markdown-formatted answer */}
          </div>
        </div>
      )}
    </div>
  );
}
