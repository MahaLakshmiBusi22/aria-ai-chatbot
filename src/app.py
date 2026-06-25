# src/app.py
# Aria AI Chatbot — with Auth + Database + RAG + File Upload

import streamlit as st
import ollama
import tempfile
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from document_reader import read_document
from database import (
    init_database, create_conversation, save_message,
    load_conversation, get_all_conversations, delete_conversation
)
from auth import register_user, login_user
from rag import index_document, get_relevant_context, remove_document

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aria - AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ─── Init DB ──────────────────────────────────────────────────────────────────
init_database()

# ─── Session State Defaults ───────────────────────────────────────────────────
for key, default in {
    "logged_in": False,
    "user": None,
    "conversation_history": [],
    "message_count": 0,
    "document_name": None,
    "conversation_id": None,
    "auth_mode": "login"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are Aria, an AI assistant helping beginner Python developers.

YOUR RULES:
1. You are Aria — never describe yourself as the user.
2. Maximum 4 sentences per response unless asked for detail.
3. Always remember facts the user shares about themselves.
4. Address the user by their name whenever possible.
5. Never suggest ChatterBot or outdated tools.
6. When document context is provided, answer ONLY from that context.
7. When asked where someone is from — answer with their location."""
}


# ==============================================================================
# AUTH PAGE
# ==============================================================================
def show_auth_page():
    st.title("🤖 Aria - AI Chatbot")
    st.caption("Your personal AI learning assistant")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])

        with tab_login:
            st.subheader("Welcome back!")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True, type="primary"):
                if username and password:
                    success, message, user = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields.")

        with tab_register:
            st.subheader("Create your account")
            new_username = st.text_input("Choose a username", key="reg_username")
            new_email = st.text_input("Email address", key="reg_email")
            new_password = st.text_input("Choose a password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")

            if st.button("Create Account", use_container_width=True, type="primary"):
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        success, message, user_id = register_user(new_username, new_email, new_password)
                        if success:
                            st.success(message + " Please login now.")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields.")


# ==============================================================================
# CHAT PAGE
# ==============================================================================
def show_chat_page():
    user = st.session_state.user

    # ─── Header ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 Aria - AI Chatbot")
        st.caption(f"Logged in as **{user['username']}** · Powered by Mistral locally")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.conversation_history = []
            st.session_state.message_count = 0
            st.session_state.conversation_id = None
            st.session_state.document_name = None
            st.rerun()

    st.divider()

    # ─── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.header(f"👋 Hello, {user['username']}!")

        if st.button("➕ New Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.message_count = 0
            st.session_state.conversation_id = None
            st.session_state.document_name = None
            st.rerun()

        st.divider()

        # Past Conversations
        st.header("🕓 My Conversations")
        all_convs = get_all_conversations(user["id"])

        if not all_convs:
            st.caption("No conversations yet. Start chatting!")
        else:
            for conv in all_convs:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    if st.button(conv["title"][:30], key=f"load_{conv['id']}", use_container_width=True):
                        st.session_state.conversation_history = load_conversation(conv["id"])
                        st.session_state.conversation_id = conv["id"]
                        st.session_state.message_count = len(st.session_state.conversation_history) // 2
                        st.rerun()
                with col_b:
                    if st.button("🗑", key=f"del_{conv['id']}"):
                        delete_conversation(conv["id"])
                        if st.session_state.conversation_id == conv["id"]:
                            st.session_state.conversation_history = []
                            st.session_state.conversation_id = None
                        st.rerun()

        st.divider()

        # File Upload with RAG
        st.header("📄 Upload Document")
        st.caption("Aria will search the most relevant parts of your document to answer questions.")

        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt"],
            help="Supported: PDF, DOCX, TXT"
        )

        if uploaded_file is not None:
            if st.session_state.document_name != uploaded_file.name:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(uploaded_file.name)[1]
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                with st.spinner("Reading and indexing document..."):
                    document_text = read_document(tmp_path)
                    os.unlink(tmp_path)

                    if document_text.startswith("Error"):
                        st.error(document_text)
                    else:
                        chunk_count = index_document(
                            document_text,
                            uploaded_file.name,
                            user["id"]
                        )
                        st.session_state.document_name = uploaded_file.name
                        word_count = len(document_text.split())
                        st.success(f"✅ {uploaded_file.name} indexed!")
                        st.metric("Words", word_count)
                        st.metric("Chunks indexed", chunk_count)

        if st.session_state.document_name:
            st.info(f"📄 Active: {st.session_state.document_name}")
            if st.button("❌ Remove Document", use_container_width=True):
                remove_document(st.session_state.document_name, user["id"])
                st.session_state.document_name = None
                st.rerun()

        st.divider()
        st.metric("Messages this session", st.session_state.message_count)

    # ─── Chat Display ─────────────────────────────────────────────────────────
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])

    # ─── Chat Input ───────────────────────────────────────────────────────────
    user_input = st.chat_input("Type your message here...")

    if user_input:
        if st.session_state.conversation_id is None:
            title = user_input[:40] + "..." if len(user_input) > 40 else user_input
            st.session_state.conversation_id = create_conversation(user["id"], title)

        with st.chat_message("user"):
            st.write(user_input)

        # RAG: search for relevant document context
        if st.session_state.document_name:
            with st.spinner("Searching document..."):
                context = get_relevant_context(
                    user_input,
                    st.session_state.document_name,
                    user["id"],
                    top_k=3
                )

            if context:
                full_message = f"""The user uploaded '{st.session_state.document_name}'.
Most relevant sections found by search:

{context}

User question: {user_input}

Answer based only on the document content above."""
            else:
                full_message = user_input
        else:
            full_message = user_input

        save_message(st.session_state.conversation_id, "user", user_input)
        st.session_state.conversation_history.append({"role": "user", "content": full_message})

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Aria is thinking..."):
                try:
                    messages_to_send = [SYSTEM_MESSAGE] + st.session_state.conversation_history
                    response = ollama.chat(model="mistral", messages=messages_to_send)
                    ai_reply = response["message"]["content"]
                    st.write(ai_reply)

                    save_message(st.session_state.conversation_id, "assistant", ai_reply)
                    st.session_state.conversation_history.append({"role": "assistant", "content": ai_reply})
                    st.session_state.message_count += 1

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.conversation_history.pop()


# ==============================================================================
# MAIN
# ==============================================================================
if st.session_state.logged_in:
    show_chat_page()
else:
    show_auth_page()