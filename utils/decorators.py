from functools import wraps
from flask import request, jsonify
from models import User

class APIError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key.split('Bearer ')[1]
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                return view_function(user, *args, **kwargs)
        raise APIError("API key inválida ou ausente", 401)
    return decorated_function
