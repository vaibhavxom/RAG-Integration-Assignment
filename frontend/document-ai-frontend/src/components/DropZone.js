'use client';  // Indicates this is a client-side React component

import { useState } from 'react';  // React hook for managing local component state
import axios from 'axios';         // HTTP client to make API requests

export default function DropZone({ setDocumentId }) {
  // State to hold the selected file object
  const [file, setFile] = useState(null);
  // State to hold the document title input by the user
  const [title, setTitle] = useState('');
  // State to indicate if upload is in progress (to disable button and show loading)
  const [uploading, setUploading] = useState(false);

  // Called when user selects a file from the file input
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];  // Get first selected file
    setFile(selectedFile);                    // Save the file object in state
    setTitle(selectedFile?.name || '');      // Set the title input to the file name by default
  };

  // Handles the file upload to the backend server
  const handleUpload = async () => {
    // Validate if file is selected and title is not empty
    if (!file || !title.trim()) {
      alert("Please select a file and enter a title.");
      return;
    }
    setUploading(true);  // Set uploading flag to disable UI and show loading

    // Prepare multipart form data for file upload
    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", title);

    try {
      // Send POST request to upload endpoint with form data
      const res = await axios.post("http://localhost:8000/documents/upload/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'  // Required for file upload
        }
      });
      setDocumentId(res.data.id);  // Set uploaded document ID in parent component
      alert("File uploaded successfully!"); // Inform user of success
    } catch (err) {
      // Log error details and show alert on failure
      console.error(err.response?.data || err);
      alert("Upload failed");
    }

    setUploading(false);  // Reset uploading flag to re-enable UI
  };

  return (
    <div className="border-2 border-dashed p-6 rounded-md text-center space-y-4">
      {/* File input for selecting document to upload */}
      <input type="file" onChange={handleFileChange} />

      {/* Text input for entering/editing document title */}
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter document title"
        className="w-full p-2 border rounded"
      />

      {/* Upload button that triggers handleUpload; disabled during upload */}
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
