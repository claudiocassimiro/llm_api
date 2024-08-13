from flask import Blueprint, jsonify
from utils.decorators import require_api_key

bp = Blueprint('user', __name__)

@bp.route('/user/usage', methods=['GET'])
@require_api_key
def get_usage(user):
    return jsonify({
        "username": user.username,
        "tokens_used": user.tokens_used
    })
