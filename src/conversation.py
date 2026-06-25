# src/conversation.py
# AI Chatbot with memory — powered by Ollama (local, no API needed)

import ollama


def chat_with_memory():
    """
    A conversation loop that remembers everything.
    Powered by Mistral running locally on your computer.
    """

    conversation_history = []

    system_message = {
        "role": "system",
        "content": """You are Aria, an AI assistant helping beginner Python developers.

YOUR RULES — FOLLOW STRICTLY:
1. You are Aria. Never describe yourself as the user.
2. Maximum 3 sentences per response. No exceptions.
3. Always remember and use facts the user tells you about themselves.
4. Address the user by their name whenever possible.
5. Never suggest ChatterBot or outdated tools.
6. Never give code unless specifically asked.
7. When asked where someone is from — answer with their location, not your description.

EXAMPLE:
User: "Where am I from?"
Wrong answer: "You are an AI assistant..."
Correct answer: "You are from Hyderabad, Mahalakshmi!"
"""
    }

    print("=" * 50)
    print("Aria - AI Chatbot (Powered by Mistral locally)")
    print("=" * 50)
    print("Type your message and press Enter.")
    print("Type 'quit' to exit.")
    print("Type 'history' to see conversation history.")
    print("Type 'clear' to start fresh.")
    print("=" * 50)
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "history":
            print("\n--- Conversation History ---")
            if not conversation_history:
                print("No messages yet.")
            for msg in conversation_history:
                role = "You" if msg["role"] == "user" else "Aria"
                print(f"[{role}]: {msg['content']}")
            print("----------------------------\n")
            continue

        if user_input.lower() == "clear":
            conversation_history = []
            print("Conversation cleared. Starting fresh!\n")
            continue

        if not user_input:
            print("Please type something!\n")
            continue

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            messages_to_send = [system_message] + conversation_history

            response = ollama.chat(
                model="mistral",
                messages=messages_to_send
            )

            ai_reply = response["message"]["content"]

            conversation_history.append({
                "role": "assistant",
                "content": ai_reply
            })

            print(f"\nAria: {ai_reply}\n")

        except Exception as e:
            print(f"Error: {e}\n")
            conversation_history.pop()


def demonstrate_memory():
    """
    Automatically tests that Aria remembers across messages.
    """

    conversation_history = []

    system_message = {
        "role": "system",
        "content": """You are Aria, an AI assistant for Python developers.
Keep all responses under 3 sentences.
Always address the user by name.
Remember everything they tell you."""
    }

    test_messages = [
        "My name is Mahalakshmi and I live in Hyderabad.",
        "I am learning Python to build AI chatbots.",
        "What is my name and where do I live?",
        "What am I learning?"
    ]

    print("=" * 50)
    print("MEMORY DEMONSTRATION")
    print("=" * 50)

    for message in test_messages:
        print(f"\nYou: {message}")
        print(f"(History size: {len(conversation_history)} messages)")

        conversation_history.append({
            "role": "user",
            "content": message
        })

        messages_to_send = [system_message] + conversation_history

        response = ollama.chat(
            model="mistral",
            messages=messages_to_send
        )

        ai_reply = response["message"]["content"]

        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        print(f"Aria: {ai_reply.strip()}")
        print("-" * 40)


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Interactive Chat (talk to Aria)")
    print("2. Memory Demonstration (automatic test)")
    print()

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        chat_with_memory()
    elif choice == "2":
        demonstrate_memory()
    else:
        print("Invalid choice. Running interactive chat...")
        chat_with_memory()