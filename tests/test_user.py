import json
from tests.base import BaseTestCase
import time
from datetime import timedelta
from app.middleware import generate_token
from config import Config

class TestUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Register and login a test user
        self.register_user()
        response = self.login_user()
        data = json.loads(response.data)
        self.token = data['token']
        self.headers = self.get_auth_headers(self.token)

    def tearDown(self):
        Config.reset_jwt_expiration()
        super().tearDown()

    def test_get_profile_authenticated(self):
        """Test getting profile with valid authentication"""
        response = self.client.get('/profile', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['user']['email'], 'test@example.com')
        self.assertEqual(data['user']['name'], 'Test User')

    def test_get_profile_unauthenticated(self):
        """Test getting profile without authentication"""
        response = self.client.get('/profile')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Missing token')

    def test_get_profile_invalid_token(self):
        """Test getting profile with invalid token"""
        headers = self.get_auth_headers('invalid-token')
        response = self.client.get('/profile', headers=headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid token')

    def test_update_profile(self):
        """Test updating user profile"""
        new_name = 'Updated Name'
        response = self.client.put('/profile', 
                                 headers=self.headers,
                                 json={'name': new_name})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        
        # Verify the update
        response = self.client.get('/profile', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(data['user']['name'], new_name)

    def test_update_resume(self):
        """Test updating resume text"""
        resume_text = 'This is my professional resume...'
        response = self.client.put('/update_resume',
                                 headers=self.headers,
                                 json={'resume_text': resume_text})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        
        # Verify the update
        response = self.client.get('/profile', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(data['user']['resume_text'], resume_text)

    def test_update_resume_too_long(self):
        """Test updating resume with text exceeding maximum length"""
        resume_text = 'x' * 51000  # Exceeds 50K character limit
        response = self.client.put('/update_resume',
                                 headers=self.headers,
                                 json={'resume_text': resume_text})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Resume text exceeds maximum length')

    def test_token_expiration(self):
        """Test that tokens expire after the configured time"""
        # Set a very short expiration time (1 second)
        Config.set_jwt_expiration(1/3600)
        
        # Create a new token with the short expiration
        from app.models import User
        user = User.query.filter_by(email='test@example.com').first()
        token = generate_token(user.id)
        headers = self.get_auth_headers(token)
        
        # Wait for token to expire
        time.sleep(2)
        
        # Try to access protected endpoint
        response = self.client.get('/profile', headers=headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401, "Token should have expired")
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Token has expired')

    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are prevented"""
        malicious_name = "'; DROP TABLE user; --"
        response = self.client.put('/profile',
                                 headers=self.headers,
                                 json={'name': malicious_name})
        
        # The request should process normally, storing the malicious input as a regular string
        self.assertEqual(response.status_code, 200)
        
        # Verify the database is intact and the string was stored safely
        response = self.client.get('/profile', headers=self.headers)
        data = json.loads(response.data)
        self.assertEqual(data['user']['name'], malicious_name)
        
        # Verify we can still query the database
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
