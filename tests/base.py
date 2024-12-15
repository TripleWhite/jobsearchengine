import unittest
import json
from unittest.mock import MagicMock
from app import create_app, db
from app.models import User

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        # 创建 MCP 客户端 mock
        self.mcp_mock = MagicMock()
        self.app.mcp = self.mcp_mock
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, email='test@example.com', password='password123', name='Test User'):
        return self.client.post('/auth/register', json={
            'email': email,
            'password': password,
            'name': name
        })

    def login_user(self, email='test@example.com', password='password123'):
        return self.client.post('/auth/login', json={
            'email': email,
            'password': password
        })

    def get_auth_headers(self, token):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def create_test_user(self, email='test@example.com', password='password123', name='Test User'):
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
