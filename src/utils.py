# src/utils.py

# Basic function — takes input, returns output
def greet_user(name):
    message = f"Hello, {name}! Welcome to the AI Chatbot."
    return message


# Function with a default value
def greet_user_formal(name, title="Mr/Ms"):
    message = f"Hello, {title} {name}!"
    return message


# Function that does a calculation
def count_words(text):
    words = text.split()       # splits text into a list of words
    total = len(words)         # counts how many words
    return total
# Dictionary basics
def show_user_profile():
    user = {
        "name": "Mahal",
        "city": "Hyderabad",
        "language": "Python",
        "level": "Beginner"
    }

    # Access a value by its key
    print(user["name"])           # Mahal
    print(user["city"])           # Hyderabad

    # Add a new key
    user["goal"] = "Build AI Chatbot"

    # Check if a key exists
    if "goal" in user:
        print(f"Goal: {user['goal']}")

    # Loop through all key-value pairs
    for key, value in user.items():
        print(f"{key} → {value}")

    return user
# Lists — this is EXACTLY how chat history works in AI APIs
def demonstrate_chat_history():
    # Every message is a dictionary with "role" and "content"
    # This is the REAL format that OpenAI and Gemini expect
    chat_history = []

    # User sends a message
    chat_history.append({"role": "user", "content": "Hello!"})

    # AI responds
    chat_history.append({"role": "assistant", "content": "Hi! How can I help?"})

    # User sends another message
    chat_history.append({"role": "user", "content": "What is Python?"})

    # Print all messages
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        print(f"[{role}]: {content}")

    print(f"\nTotal messages: {len(chat_history)}")
    return chat_history
# File reading and writing
def read_text_file(filepath):
    """Read a text file and return its content."""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def write_text_file(filepath, content):
    """Write content to a text file."""
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"File saved: {filepath}")


def count_lines_in_file(filepath):
    """Count how many lines a file has."""
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return len(lines)
import os
from dotenv import load_dotenv

# Environment variables
def load_config():
    """Load configuration from .env file."""
    load_dotenv()   # reads the .env file and loads all variables

    config = {
        "app_name": os.getenv("APP_NAME", "Default App"),
        "debug": os.getenv("DEBUG_MODE", "False"),
        "api_key": os.getenv("GEMINI_API_KEY", "not-set")
    }

    return config