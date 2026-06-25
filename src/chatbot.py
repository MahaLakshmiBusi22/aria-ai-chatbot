# src/chatbot.py

class Chatbot:
    """
    A simple chatbot class.
    This is the blueprint — we will expand this throughout the course.
    """

    def __init__(self, name, personality):
        """
        __init__ runs automatically when you create a new Chatbot.
        Think of it as the 'setup' function.
        """
        self.name = name                    # store the bot's name
        self.personality = personality      # store its personality
        self.conversation_history = []      # empty list — no messages yet
        self.message_count = 0             # counter

    def add_message(self, role, content):
        """Add a message to conversation history."""
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        self.message_count += 1

    def show_history(self):
        """Print all messages in the conversation."""
        print(f"\n--- {self.name}'s Conversation History ---")
        if not self.conversation_history:
            print("No messages yet.")
            return

        for msg in self.conversation_history:
            print(f"[{msg['role']}]: {msg['content']}")

        print(f"--- Total: {self.message_count} messages ---\n")

    def get_stats(self):
        """Return a summary of the conversation."""
        return {
            "bot_name": self.name,
            "personality": self.personality,
            "total_messages": self.message_count
        }