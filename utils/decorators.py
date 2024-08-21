from functools import wraps
from flask import request, jsonify
from models import User
import logging

class APIError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'error': self.message}

    def handle(self):
        response = jsonify(self.to_dict())
        response.status_code = self.status_code
        return response

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key.split('Bearer ')[1]
            user = User.query.filter_by(api_key=api_key).first()
            if user:
                return view_function(user, *args, **kwargs)
        logging.error(f"Invalid or missing API key: {api_key}")
        raise APIError("API key inválida ou ausente", 401)
    return decorated_function
