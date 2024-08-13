from transformers import AutoTokenizer
from models import User
from app import db

MODEL_MAPPING = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "mistral": "mistralai/Mistral-7B-v0.1",
    "gpt4": "gpt2",  # Usando GPT-2 como fallback para GPT-4
}

tokenizers = {}

def get_tokenizer(model_name):
    if model_name not in tokenizers:
        hf_model_name = MODEL_MAPPING.get(model_name, "gpt2")  # Use GPT-2 como fallback
        tokenizers[model_name] = AutoTokenizer.from_pretrained(hf_model_name)
    return tokenizers[model_name]

def count_tokens(text, model_name):
    tokenizer = get_tokenizer(model_name)
    return len(tokenizer.encode(text))

def update_token_usage(user, token_count):
    user.tokens_used += token_count
    db.session.commit()
