import requests

def ask_llm(prompt):
    url = "http://127.0.0.1:11434/api/generate"

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        return response.json().get("response", "No response from model")

    except Exception as e:
        return f"❌ LLM Connection Error: {e}"