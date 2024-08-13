from flask import Blueprint, request, jsonify
from models import User
from utils.extensions import db, bcrypt 
from utils.decorators import APIError
import uuid

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        raise APIError("Dados de registro inválidos", 400)

    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        raise APIError("Nome de usuário já existe", 400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    api_key = str(uuid.uuid4())
    new_user = User(username=username, password_hash=hashed_password, api_key=api_key)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso", "api_key": api_key}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        raise APIError("Dados de login inválidos", 400)

    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login bem-sucedido", "api_key": user.api_key})
    else:
        raise APIError("Credenciais inválidas", 401)
