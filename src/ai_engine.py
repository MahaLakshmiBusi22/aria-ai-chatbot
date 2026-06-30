# src/llm.py
# Smart LLM handler — uses Ollama locally, Gemini on cloud

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_response(messages, system_prompt):
    """
    Automatically picks the right AI:
    - If GEMINI_API_KEY is set → use Gemini (cloud)
    - Otherwise → use Ollama Mistral (local)
    
    messages = list of {"role": "user"/"assistant", "content": "..."}
    system_prompt = string with instructions for the AI
    """
    api_key = os.getenv("GEMINI_API_KEY", "")

    # Use Gemini if API key exists and is not a placeholder
    if api_key and "your-key" not in api_key and len(api_key) > 10:
        return _call_gemini(messages, system_prompt, api_key)
    else:
        return _call_ollama(messages, system_prompt)


def _call_gemini(messages, system_prompt, api_key):
    """Call Gemini API."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Convert messages to Gemini format
    gemini_history = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=gemini_history,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            max_output_tokens=800
        )
    )

    return response.text


def _call_ollama(messages, system_prompt):
    """Call local Ollama Mistral."""
    import ollama

    ollama_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        ollama_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    response = ollama.chat(
        model="mistral",
        messages=ollama_messages
    )
    return response["message"]["content"]


def get_current_llm():
    """Returns which LLM is being used — for display in UI."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key and "your-key" not in api_key and len(api_key) > 10:
        return "Gemini (Cloud)"
    return "Mistral (Local)"