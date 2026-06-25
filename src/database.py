# src/database.py
# Handles all database operations — users, conversations, messages

import sqlite3
import os
from datetime import datetime

DB_PATH = "database/chatbot.db"


def init_database():
    """
    Create all tables if they don't exist.
    Run this once when the app starts.
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table 1: users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Table 2: conversations (now linked to a user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Table 3: messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    conn.commit()
    conn.close()


# ─── User Functions ───────────────────────────────────────────────────────────

def create_user(username, email, password_hash):
    """Create a new user. Returns user_id or None if username/email exists."""
    now = datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
        """, (username.lower().strip(), email.lower().strip(), password_hash, now))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username):
    """Fetch a user row by username."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, email, password_hash
        FROM users WHERE username = ?
    """, (username.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}
    return None


def get_user_by_email(email):
    """Fetch a user row by email."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, email, password_hash
        FROM users WHERE email = ?
    """, (email.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}
    return None


# ─── Conversation Functions ───────────────────────────────────────────────────

def create_conversation(user_id, title=None):
    """Start a new conversation for a specific user."""
    if not title:
        title = f"Chat on {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    now = datetime.now().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (user_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, title, now, now))
    conversation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return conversation_id


def save_message(conversation_id, role, content):
    """Save one message to the database."""
    now = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, role, content, now))
    cursor.execute("""
        UPDATE conversations SET updated_at = ? WHERE id = ?
    """, (now, conversation_id))
    conn.commit()
    conn.close()


def load_conversation(conversation_id):
    """Load all messages from a conversation."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def get_all_conversations(user_id):
    """Get all conversations for a specific user (newest first)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, created_at, updated_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY updated_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "title": row[1], "created_at": row[2], "updated_at": row[3]}
        for row in rows
    ]


def delete_conversation(conversation_id):
    """Delete a conversation and all its messages."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()