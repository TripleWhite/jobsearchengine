from flask import Blueprint, jsonify, g
from app.middleware import jwt_required, admin_required
from app.models import User
from app import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users', methods=['GET'])
@jwt_required
@admin_required
def list_users():
    """List all users (admin only)"""
    users = User.query.all()
    return jsonify({
        'status': 'ok',
        'users': [user.to_dict() for user in users]
    })

@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
@admin_required
def get_user(user_id):
    """Get specific user details (admin only)"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'status': 'ok',
        'user': user.to_dict()
    })

@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@jwt_required
@admin_required
def toggle_admin_status(user_id):
    """Toggle admin status of a user (admin only)"""
    if user_id == g.current_user.id:
        return jsonify({
            'status': 'error',
            'message': 'Cannot modify your own admin status'
        }), 400
        
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return jsonify({
        'status': 'ok',
        'message': f'Admin status {"enabled" if user.is_admin else "disabled"} for user {user.email}',
        'user': user.to_dict()
    })
