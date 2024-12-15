from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.middleware import generate_token
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    return len(password) >= 8

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({
            'status': 'error',
            'message': 'Email and password are required'
        }), 400

    email = data['email']
    password = data['password']
    name = data.get('name')

    if not is_valid_email(email):
        return jsonify({
            'status': 'error',
            'message': 'Invalid email format'
        }), 400

    if not is_valid_password(password):
        return jsonify({
            'status': 'error',
            'message': 'Password must be at least 8 characters long'
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({
            'status': 'error',
            'message': 'Email already in use'
        }), 400

    user = User(email=email, name=name)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 'ok',
        'message': 'User registered successfully'
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({
            'status': 'error',
            'message': 'Email and password are required'
        }), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({
            'status': 'error',
            'message': 'Invalid credentials'
        }), 401

    token = generate_token(user.id)
    
    return jsonify({
        'status': 'ok',
        'token': token,
        'user': user.to_dict()
    }), 200
