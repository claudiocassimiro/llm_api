import requests
from flask import current_app

def get_models():
    try:
        response = requests.get(f"{current_app.config['OLLAMA_BASE_URL']}/api/tags")
        response.raise_for_status()
        models = response.json()['models']
        return [{"id": model['name'], "object": "model"} for model in models]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching models: {str(e)}")

def generate_chat_completion(model, prompt, data, stream=False):
    try:
        response = requests.post(
            f"{current_app.config['OLLAMA_BASE_URL']}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "temperature": data.get('temperature', 0.7),
                "top_p": data.get('top_p', 1.0),
                "max_tokens": data.get('max_tokens', None)
            },
            stream=stream
        )
        response.raise_for_status()
        if stream:
            return (chunk['response'] for chunk in response.iter_lines() if chunk)
        else:
            return response.json()['response']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error generating chat completion: {str(e)}")

def generate_completion(model, prompt, data):
    try:
        response = requests.post(
            f"{current_app.config['OLLAMA_BASE_URL']}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": data.get('max_tokens', 16),
                "temperature": data.get('temperature', 0.7),
                "top_p": data.get('top_p', 1.0)
            }
        )
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error generating completion: {str(e)}")
