# 🤖 Aria — AI Chatbot

A production-ready AI chatbot built from scratch with Python, Streamlit, Google Gemini, and RAG-powered document search.

## ✨ Features

- 💬 **Natural conversation** — chat about anything: tech, advice, casual talk, emotional support, or deep dives into any topic
- 🧠 **Persistent memory** — Aria remembers facts about you across the conversation
- 🔐 **User authentication** — secure login/register system with bcrypt password hashing
- 📂 **Per-user conversation history** — every user has their own private chat history, saved to a database
- 📄 **Document Q&A (RAG)** — upload a PDF, DOCX, or TXT file and ask Aria questions about it; uses vector search (ChromaDB) to find the most relevant sections instead of guessing
- 📁 **Per-conversation documents** — attach a different file to each individual conversation
- ⚡ **Powered by Gemini 2.5 Flash** — fast, accurate responses
- 🖥️ **Clean web UI** — built entirely with Streamlit, no frontend code required

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Google Gemini API |
| Vector Search / RAG | ChromaDB |
| Database | SQLite |
| Auth | bcrypt |
| Document Parsing | PyMuPDF, python-docx |

## 🚀 Running Locally

1. Clone the repo
```bash
   git clone https://github.com/MahaLakshmiBusi22/aria-ai-chatbot.git
   cd aria-ai-chatbot
```

2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   venv\Scripts\Activate.ps1   # Windows
   pip install -r requirements.txt
```

3. Add your Gemini API key to a `.env` file
