from flask import Blueprint, request, jsonify, Response, stream_with_context
from utils.decorators import require_api_key, APIError
from services.ollama_service import get_models, generate_chat_completion, generate_completion
from services.token_counter import count_tokens, update_token_usage
import time
import json

bp = Blueprint('llm', __name__)

@bp.route('/v1/models', methods=['GET'])
@require_api_key
def list_models(user):
    try:
        models = get_models()
        return jsonify({"object": "list", "data": models})
    except Exception as e:
        raise APIError(f"Erro ao listar modelos: {str(e)}", 500)

@bp.route('/v1/chat/completions', methods=['POST'])
@require_api_key
def chat_completions(user):
    data = request.json
    if not data or 'messages' not in data or 'model' not in data:
        raise APIError("Parâmetros inválidos", 400)

    model = data['model']
    messages = data['messages']
    stream = data.get('stream', False)
    
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    prompt_tokens = count_tokens(prompt, model)

    if stream:
        return Response(stream_with_context(stream_response(user, model, prompt, data)), content_type='text/event-stream')
    else:
        try:
            completion = generate_chat_completion(model, prompt, data)
            completion_tokens = count_tokens(completion, model)
            total_tokens = prompt_tokens + completion_tokens
            
            update_token_usage(user, total_tokens)

            return jsonify({
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": completion
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens
                }
            })
        except Exception as e:
            raise APIError(f"Erro ao gerar resposta: {str(e)}", 500)

def stream_response(user, model, prompt, data):
    try:
        total_tokens = count_tokens(prompt, model)
        for chunk in generate_chat_completion(model, prompt, data, stream=True):
            total_tokens += count_tokens(chunk, model)
            yield f"data: {json.dumps({
                'id': f"chatcmpl-{int(time.time())}",
                'object': 'chat.completion.chunk',
                'created': int(time.time()),
                'model': model,
                'choices': [{
                    'index': 0,
                    'delta': {
                        'content': chunk
                    },
                    'finish_reason': None
                }]
            })}\n\n"
        update_token_usage(user, total_tokens)
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@bp.route('/v1/completions', methods=['POST'])
@require_api_key
def completions(user):
    data = request.json
    if not data or 'prompt' not in data or 'model' not in data:
        raise APIError("Parâmetros inválidos", 400)

    model = data['model']
    prompt = data['prompt']

    try:
        completion = generate_completion(model, prompt, data)
        prompt_tokens = count_tokens(prompt, model)
        completion_tokens = count_tokens(completion, model)
        total_tokens = prompt_tokens + completion_tokens
        
        update_token_usage(user, total_tokens)

        return jsonify({
            "id": f"cmpl-{int(time.time())}",
            "object": "text_completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "text": completion,
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": "length"
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        })
    except Exception as e:
        raise APIError(f"Erro ao gerar resposta: {str(e)}", 500)