//dropzone.js 
'use client';
import { useState } from 'react';
import axios from 'axios';

export default function DropZone({ setDocumentId }) {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setTitle(selectedFile?.name || '');
  };

  const handleUpload = async () => {
    if (!file || !title.trim()) {
      alert("Please select a file and enter a title.");
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);

    try {
      const res = await axios.post("http://localhost:8000/documents/upload/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setDocumentId(res.data.id);
      alert("File uploaded successfully!");
    } catch (err) {
      console.error(err.response?.data || err);
      alert("Upload failed");
    }
    setUploading(false);
  };

  return (
    <div className="border-2 border-dashed p-6 rounded-md text-center space-y-4">
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter document title"
        className="w-full p-2 border rounded"
      />
      <button
        onClick={handleUpload}
        disabled={uploading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {uploading ? 'Uploading...' : 'Upload Document'}
      </button>
    </div>
  );
}
