# src/api_test.py
# Understanding how APIs work before we connect to Gemini

import requests
import json


def call_public_api():
    """
    Call a free public API and understand the response structure.
    This is EXACTLY how we will call Gemini later — same pattern.
    """

    url = "https://api.chucknorris.io/jokes/random"

    print("=" * 50)
    print("MAKING AN API CALL")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Method: GET")
    print()

    response = requests.get(url)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("✅ Request successful!")
    else:
        print("❌ Something went wrong!")
        return

    data = response.json()

    print()
    print("RAW RESPONSE (JSON):")
    print(json.dumps(data, indent=2))

    print()
    print("EXTRACTING SPECIFIC DATA:")
    print(f"Joke ID  : {data['id']}")
    print(f"Joke Text: {data['value']}")
    print(f"Category : {data['categories']}")


def demonstrate_post_request():
    """
    POST request — this is how we send messages to Gemini.
    POST = we are SENDING data, not just fetching it.
    """

    url = "https://httpbin.org/post"

    payload = {
        "message": "Hello AI!",
        "role": "user",
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json"
    }

    print()
    print("=" * 50)
    print("MAKING A POST REQUEST")
    print("=" * 50)
    print(f"Sending payload: {payload}")
    print()

    response = requests.post(url, json=payload, headers=headers)

    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print("❌ Request failed")
        print(response.text)
        return

    data = response.json()
    print(f"Server received our JSON: {data['json']}")


def safe_api_call(url):
    """
    Production-grade API call with proper error handling.
    Always write API calls like this in real projects.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. Server took too long.")
        return None

    except requests.exceptions.ConnectionError:
        print("❌ Error: No internet connection or server unreachable.")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return None

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


if __name__ == "__main__":
    call_public_api()
    demonstrate_post_request()

    print()
    print("=" * 50)
    print("SAFE API CALL TEST")
    print("=" * 50)

    result = safe_api_call("https://api.chucknorris.io/jokes/random")
    if result:
        print(f"✅ Got joke: {result['value']}")

    result = safe_api_call("https://this-url-does-not-exist-123.com/api")
    if result is None:
        print("✅ Error handled gracefully — app did not crash!")