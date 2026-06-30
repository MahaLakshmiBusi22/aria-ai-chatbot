# 🤖 Aria – AI Chatbot

> A production-ready AI chatbot built with **Python**, **Streamlit**, **Google Gemini**, and **Retrieval-Augmented Generation (RAG)** for intelligent document-based conversations.

---

## 📌 Overview

Aria is an AI-powered chatbot that combines conversational AI with document retrieval to deliver accurate and context-aware responses. It supports natural conversations, secure user authentication, persistent chat history, and document question-answering using vector search.

The application is designed with a clean Streamlit interface and uses Google's Gemini models for fast, intelligent responses while leveraging ChromaDB for efficient semantic search over uploaded documents.

---

## ✨ Features

### 💬 AI Conversations
- Natural and context-aware conversations
- Powered by Google Gemini 2.5 Flash
- Supports general knowledge, coding, writing, and daily conversations

### 🧠 Persistent Memory
- Remembers previous conversation context
- Maintains continuity throughout the chat session

### 🔐 User Authentication
- Secure Login & Registration
- Password hashing using bcrypt
- User-specific account management

### 📂 Conversation History
- Individual chat history for every user
- Stored securely using SQLite
- Resume previous conversations anytime

### 📄 Document Question Answering (RAG)
Upload documents and ask questions directly from them.

Supported formats:
- PDF
- DOCX
- TXT

The chatbot:
- Extracts document text
- Splits text into chunks
- Generates embeddings
- Stores them in ChromaDB
- Retrieves the most relevant chunks before answering

This significantly improves factual accuracy and reduces hallucinations.

### 📁 Per-Conversation Documents
Each conversation can have its own uploaded document, allowing independent document-based chats.

### 🖥️ Streamlit Interface
- Clean and responsive UI
- Easy to use
- No frontend framework required

---

# 🏗️ System Architecture

```
User
   │
   ▼
Streamlit UI
   │
   ▼
Authentication (bcrypt)
   │
   ▼
SQLite Database
   │
   ├── User Accounts
   ├── Chat History
   └── Conversation Data
   │
   ▼
Google Gemini API
   │
   ▼
Response Generation
   ▲
   │
ChromaDB Vector Store
   ▲
   │
Document Embeddings
   ▲
   │
PDF / DOCX / TXT Upload
```

---

# 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| UI | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Vector Database | ChromaDB |
| Database | SQLite |
| Authentication | bcrypt |
| PDF Processing | PyMuPDF |
| DOCX Processing | python-docx |
| Environment Variables | python-dotenv |

---

# 📂 Project Structure

```
aria-ai-chatbot/
│
├── app.py
├── database.py
├── auth.py
├── rag.py
├── embeddings.py
├── utils.py
│
├── chroma_db/
│
├── uploads/
│
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/aria-ai-chatbot.git

cd aria-ai-chatbot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Environment File

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 📚 How RAG Works

1. User uploads a document
2. Text is extracted from the document
3. The text is split into smaller chunks
4. Embeddings are generated
5. Embeddings are stored in ChromaDB
6. User asks a question
7. Relevant chunks are retrieved using vector similarity search
8. Retrieved context is sent to Gemini
9. Gemini generates an accurate answer based on the document

---

# 🔒 Security Features

- Secure password hashing with bcrypt
- User-specific chat history
- Private document storage
- Separate conversation context
- Environment variables for API keys

---

# 🎯 Use Cases

- AI Assistant
- Document Question Answering
- Research Assistant
- Resume Analysis
- Study Material Chatbot
- Company Knowledge Base
- PDF Assistant
- Notes Summarization
- Technical Documentation Search

---

# 📈 Future Improvements

- Voice Conversations
- Image Understanding
- OCR Support
- Multi-file RAG
- Citation-Based Answers
- Web Search Integration
- Streaming Responses
- Conversation Export
- Docker Deployment
- PostgreSQL Support
- Cloud Deployment
- Multi-LLM Support (Gemini, OpenAI, Claude, Llama)

---

# 📸 Screenshots

Add screenshots here.

```
assets/
├── login.png
├── register.png
├── chat.png
├── upload.png
└── rag.png
```

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Maha Lakshmi Busi**

GitHub: https://github.com/MahaLakshmiBusi22

---

## ⭐ If you found this project useful, consider giving it a Star!
