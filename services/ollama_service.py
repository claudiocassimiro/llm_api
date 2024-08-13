import requests
from flask import current_app
import json

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
    if not model or not prompt:
        raise ValueError("model and prompt are required parameters")

    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": data.get('max_tokens', 16),
            "temperature": max(min(data.get('temperature', 0.7), 1.0), 0.0),
            "top_p": max(min(data.get('top_p', 1.0), 1.0), 0.0)
        }

        response = requests.post(
            f"{current_app.config['OLLAMA_BASE_URL']}/api/generate",
            json=payload
        )

        response.raise_for_status()

        # Processar a resposta linha por linha
        responses = []
        for line in response.text.strip().splitlines():
            try:
                json_response = json.loads(line)
                responses.append(json_response['response'])  # Armazena a parte 'response'
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {line}. Error: {str(e)}")

        return ''.join(responses)  # Retorna a concatenação das respostas

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error generating completion: {str(e)}")
