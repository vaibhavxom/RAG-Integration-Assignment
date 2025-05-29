# 📄 Document Intelligence Platform

A full-stack Retrieval-Augmented Generation (RAG) system that lets users upload documents, store them locally, extract and embed content into a vector database (ChromaDB), and ask questions answered by AI using the uploaded content.

---

## 🔍 Description

A RAG-based document question-answering platform using Django, ReactJS, MySQL, ChromaDB, and OpenAI API to extract insights from uploaded documents.

---

## 🖼️ Screenshots

### Upload Document Page
![Upload Screenshot](./screenshot-1.png)

### Chat with Document Page
![Chat Screenshot](./Screenshot-2.png)

---

## ⚙️ Setup Instructions

### 🧠 Backend (Django + ChromaDB + MySQL)


# 1. Clone the repo
```bash
git clone https://github.com/vaibhavxom/RAG-Integration-Assignment.git
cd document-ai/backend
```
# 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
# 3. Install dependencies
```bash
pip install -r requirements.txt
```
# 4. Run migrations
```bash
python manage.py migrate
```
# 5. Start server
```bash
python manage.py runserver
```

💻 Frontend (Next.js + Tailwind CSS)
```bash
cd ../frontend/document-ai-frontend
```
### Install frontend dependencies
```bash
npm install
```
# Start the frontend dev server
```bash
npm run dev
```
### 📡 API Documentation  
# `POST /documents/upload/`  
Uploads a document and stores metadata in MySQL.  
Extracts and splits text into chunks.  
Embeds content using OpenAI or LM Studio.  
Stores vectors in ChromaDB.   

Payload (FormData):  
- `file`: PDF or TXT document  
- `title`: Title of the document

Response:
```json
{
  "id": 1,
  "title": "My PDF",
  "filename": "my_pdf.pdf"
}
```

# `POST /documents/ask`
- Accepts a question and document ID.
- Searches similar vectors from ChromaDB.
- Sends combined context and question to LLM (e.g., OpenAI).
- Returns the answer.

Payload:

```json
{
  "document_id": 1,
  "question": "What is the main idea of the document?"
} 
```
Response:

```json
{
  "answer": "The document discusses the impact of AI on education..."
} 
```

### 💬 Sample Questions and Answers
- Q: What is the key summary of this uploaded document?
-- A: This document outlines the core principles of machine learning and its application in finance.

- Q: What does the author say about sustainable energy?
-- A: The author emphasizes the urgency of transitioning to solar and wind to meet global goals.

# 📦 Backend Requirements (`requirements.txt`)

```bash
Django>=4.2
djangorestframework
mysqlclient
openai
chromadb
langchain
python-dotenv
PyPDF2
unstructured
tiktoken
```

📦 Frontend Dependencies (package.json)
```json

{
  "dependencies": {
    "axios": "^1.6.7",
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "react-markdown": "^9.0.0",
    "tailwindcss": "^3.4.1"
  }
}
```
To install all frontend dependencies:

```bash
cd frontend/document-ai-frontend
npm install
```