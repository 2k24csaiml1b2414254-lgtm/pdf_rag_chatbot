# 📚 PDF RAG Chatbot

**Chat with your documents using Retrieval-Augmented Generation (RAG).**

A document-based AI chatbot built with Flask, LangChain, FAISS, Hugging Face embeddings, and Groq. Upload a PDF or TXT file, ask questions about its contents, and receive answers generated using retrieved document context.

## ✨ Features

- **PDF & TXT Support:** Upload PDF or plain-text documents.
- **Retrieval-Augmented Generation:** Retrieve relevant document chunks before generating answers.
- **Semantic Vector Search:** Use FAISS to index and retrieve document chunks through embeddings.
- **Hosted Embeddings:** Generate embeddings using Hugging Face's hosted endpoint.
- **LLM-Powered Answers:** Generate responses using Groq's Llama 3.1 8B Instant model.
- **Conversational Memory:** Maintain chat history through LangChain's conversation memory.
- **Simple Web Interface:** Dark-themed interface with document upload, chat, loading indicators, and a reset button.
- **File Validation:** Restrict uploads to PDF and TXT extensions, with a maximum request size of 16 MB.
- **Production Server:** Include Gunicorn for deployment on supported hosting platforms.

## 🏗️ Architecture

```text
                 ┌─────────────────────┐
                 │   User / Browser    │
                 │  HTML, CSS, JS      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Flask App       │
                 │ Upload / Chat / Reset│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     RAG Engine      │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌────────────────┐     ┌────────────────┐
       │ PDF / TXT Loader│     │ Conversation   │
       │ Text Chunking   │     │ Memory         │
       └────────┬───────┘     └────────────────┘
                ▼
       ┌────────────────┐
       │ Hugging Face   │
       │ Embeddings     │
       └────────┬───────┘
                ▼
       ┌────────────────┐
       │ FAISS Vector   │
       │ Store          │
       └────────┬───────┘
                │ Retrieve top 4 chunks
                ▼
       ┌────────────────┐
       │ Groq LLM       │
       │ Llama 3.1 8B   │
       └────────┬───────┘
                ▼
          Generated Answer
```

## 🔄 How It Works

1. **Upload:** The user uploads a PDF or TXT document through the web interface.
2. **Load:** The backend loads the document using LangChain document loaders.
3. **Chunk:** `RecursiveCharacterTextSplitter` splits the content into chunks of 500 characters, with a 50-character overlap.
4. **Embed:** Hugging Face's hosted embedding endpoint generates vector embeddings.
5. **Index:** FAISS creates a vector index or adds new document chunks to the existing index.
6. **Retrieve:** The retriever selects up to four relevant chunks for a question.
7. **Generate:** Groq's Llama 3.1 8B Instant model generates an answer through LangChain's conversational retrieval chain.
8. **Respond:** The answer is returned to the browser and displayed in the chat interface.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| RAG Framework | LangChain |
| PDF Processing | PyPDFLoader, pypdf |
| Text Processing | TextLoader, RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face Endpoint Embeddings |
| Embedding Model | `BAAI/bge-small-en-v1.5` |
| Vector Store | FAISS CPU |
| Language Model | Groq `llama-3.1-8b-instant` |
| Conversation Memory | LangChain ConversationBufferMemory |
| Frontend | HTML, CSS, JavaScript |
| Environment Configuration | python-dotenv |
| WSGI Server | Gunicorn |
| Deployment Target | Render |

## 📁 Project Structure

```text
pdf_rag_chatbot/
├── templates/
│   └── index.html
├── app.py
├── rag_engine.py
├── requirements.txt
├── Procfile
└── .gitignore
```

Uploaded files are stored in the `uploads/` directory, which is created by the application at runtime.

## ⚙️ Getting Started

### 1. Prerequisites

- Python installed on your system
- A Hugging Face access token
- A Groq API key

The embedding and language models are accessed through hosted services, so the application requires network access and valid credentials for those services.

### 2. Clone the Repository

```bash
git clone https://github.com/2k24csaiml1b2414254-lgtm/pdf_rag_chatbot.git
cd pdf_rag_chatbot
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_api_key
```

- `HF_TOKEN` is read explicitly by the embedding configuration.
- `GROQ_API_KEY` is the conventional environment variable used by the Groq integration.

Replace the example values with your own credentials. Never commit real API keys or tokens to GitHub.

### 5. Run the Application

```bash
python app.py
```

Open the local address printed by Flask in your browser. The default Flask development server normally uses:

```text
http://127.0.0.1:5000
```

### 6. Use the Chatbot

1. Choose a PDF or TXT file.
2. Click **Upload** and wait for the indexing status.
3. Enter a question related to the uploaded document.
4. Click **Send** or press Enter.
5. Use **Reset** to clear the current in-memory RAG state and visible conversation.

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Render the chatbot interface |
| `/upload` | POST | Upload and index a PDF or TXT document |
| `/chat` | POST | Submit a question and receive an answer |
| `/reset` | POST | Clear the current RAG state and conversation memory |

### Upload a Document

Send a multipart form request with a `file` field to `/upload`.

Example response:

```json
{
  "message": "'document.pdf' loaded — 42 chunks indexed."
}
```

The chunk count shown above is illustrative; the actual count depends on the uploaded document.

### Ask a Question

Send a JSON request to `/chat`:

```json
{
  "question": "What are the main points in this document?"
}
```

Example response:

```json
{
  "answer": "The answer generated from the retrieved document context..."
}
```

The response above is illustrative, not a guaranteed answer.

### Reset the Session

Send a POST request to `/reset` to clear the in-memory vector store, retrieval chain, and conversation memory.

## 🚀 Deployment on Render

The repository includes a `Procfile` with the following command:

```text
web: gunicorn app:app
```

To deploy on Render:

1. Push the project to GitHub.
2. Sign in to Render and create a new **Web Service**.
3. Connect the `pdf_rag_chatbot` repository.
4. Select a Python runtime compatible with the pinned dependencies.
5. Configure the build command:

   ```bash
   pip install -r requirements.txt
   ```

6. Configure the start command:

   ```bash
   gunicorn app:app
   ```

7. Add the following environment variables in Render's environment settings:

   - `HF_TOKEN`
   - `GROQ_API_KEY`

8. Deploy the service and review the build and runtime logs.

**Deployment note:** The included `Procfile` provides a Gunicorn start command, but a successful Render deployment has not been independently verified. Check dependency compatibility and service logs if the build or startup fails.

## 🔐 Security and Limitations

- Only PDF and TXT filename extensions are accepted, and the Flask request size limit is 16 MB. This does not replace validation of the uploaded file's actual contents.
- API credentials must be configured securely and must not be exposed in client-side code.
- The current application uses one global `RAGEngine` instance. Multiple users may share the same document index and conversation memory. It should not be treated as a multi-user-isolated application without further changes.
- Uploaded files are saved on the server. The reset operation clears the in-memory RAG state but does not delete uploaded files from disk.
- The FAISS index and conversation memory are maintained in application memory; persistent storage across restarts is not implemented in the supplied code.
- Answers depend on document content, retrieval quality, and the external model services. Generated responses should be checked for accuracy.
- The application returns exception messages in API error responses. Production deployments should use safer error handling.
- Hosted model APIs require network connectivity, valid credentials, and service availability.

## 🔮 Potential Future Improvements

- Add per-user sessions and isolated document indexes.
- Add source citations or page references to generated answers.
- Validate file contents and improve upload security.
- Add robust frontend and backend error handling.
- Delete uploaded files when a session is reset.
- Add persistent document storage and index management.
- Add automated tests for document ingestion, retrieval, and API endpoints.
- Add rate limiting and production-grade logging.

These are possible future enhancements, not features currently claimed as implemented.

## 👨‍💻 Author

**Himesh Mishra**

B.Tech Computer Science Engineering — AI/ML

GitHub: [2k24csaiml1b2414254-lgtm](https://github.com/2k24csaiml1b2414254-lgtm)

---

*Built to explore document question answering, retrieval-augmented generation, vector search, and LLM application development.*
