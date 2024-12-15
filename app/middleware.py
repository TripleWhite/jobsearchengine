from functools import wraps
from flask import request, jsonify, g, current_app
import jwt
from datetime import datetime, timedelta, UTC
from app.models import User
from app import db
from config import Config

def get_token_from_header():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]

def generate_token(user_id):
    expiration = datetime.now(UTC) + timedelta(hours=Config.get_jwt_expiration())
    return jwt.encode(
        {'user_id': user_id, 'exp': expiration},
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        
        if not token:
            current_app.logger.error('Missing token in request')
            return jsonify({'status': 'error', 'message': 'Missing token'}), 401
        
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            user = db.session.get(User, payload['user_id'])
            if not user:
                current_app.logger.error(f'User not found for token payload: {payload}')
                return jsonify({'status': 'error', 'message': 'User not found'}), 401
            g.current_user = user
        except jwt.ExpiredSignatureError:
            current_app.logger.error('Token has expired')
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            current_app.logger.error(f'Invalid token error: {str(e)}')
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        except Exception as e:
            current_app.logger.error(f'Unexpected error in jwt_required: {str(e)}')
            return jsonify({'status': 'error', 'message': 'Authentication error'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @jwt_required  # 先验证 JWT 并设置 g.current_user
    def decorated_function(*args, **kwargs):
        if not g.current_user.is_admin:
            current_app.logger.error(f'Non-admin user attempted to access admin endpoint: {g.current_user.email}')
            return jsonify({'status': 'error', 'message': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function
