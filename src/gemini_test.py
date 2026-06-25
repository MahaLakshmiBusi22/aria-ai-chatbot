# src/gemini_test.py
# Your first real AI message using the new google-genai library

import os
from dotenv import load_dotenv
from google import genai


def setup_gemini():
    """
    Load API key from .env and configure the Gemini client.
    Always do this before making any API call.
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file!")

    if "your-key-will-go-here" in api_key:
        raise ValueError("You forgot to replace the placeholder with your real API key!")

    client = genai.Client(api_key=api_key)
    print("✅ Gemini configured successfully!")
    return client


def send_single_message(client, user_message):
    """
    Send one message to Gemini and get one response back.
    This is the simplest possible AI interaction.
    """

    print()
    print("=" * 50)
    print("SENDING MESSAGE TO GEMINI")
    print("=" * 50)
    print(f"You: {user_message}")
    print()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_message
    )

    ai_reply = response.text
    print(f"Gemini: {ai_reply}")
    return ai_reply


def understand_response_structure(client, user_message):
    """
    Look at the FULL response object so you understand
    what Gemini sends back — not just the text.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_message
    )

    print()
    print("=" * 50)
    print("FULL RESPONSE STRUCTURE")
    print("=" * 50)

    print(f"Response text     : {response.text[:100]}...")
    print(f"Finish reason     : {response.candidates[0].finish_reason}")

    usage = response.usage_metadata
    print(f"Tokens sent       : {usage.prompt_token_count}")
    print(f"Tokens received   : {usage.candidates_token_count}")
    print(f"Total tokens used : {usage.total_token_count}")


def test_different_prompts(client):
    """
    Test Gemini with different types of questions.
    """

    prompts = [
        "What is Python in one sentence?",
        "Give me 3 tips for learning programming as a beginner.",
        "What is the capital of Telangana state in India?"
    ]

    print()
    print("=" * 50)
    print("TESTING MULTIPLE PROMPTS")
    print("=" * 50)

    for i, prompt in enumerate(prompts, 1):
        print(f"\nQuestion {i}: {prompt}")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        print(f"Answer: {response.text.strip()}")
        print("-" * 40)


if __name__ == "__main__":
    # Step 1: Always set up first
    client = setup_gemini()

    # Step 2: Send your first ever AI message
    send_single_message(
        client,
        "Hello Gemini! I am learning to build an AI chatbot. Say hello back!"
    )

    # Step 3: Understand the response structure
    understand_response_structure(
        client,
        "What is artificial intelligence?"
    )

    # Step 4: Test different prompts
    test_different_prompts(client)