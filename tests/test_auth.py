import json
from tests.base import BaseTestCase

class TestAuth(BaseTestCase):
    def test_successful_registration(self):
        """Test successful user registration"""
        response = self.register_user()
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['message'], 'User registered successfully')

    def test_duplicate_email_registration(self):
        """Test registration with already registered email"""
        # First registration
        self.register_user()
        
        # Second registration with same email
        response = self.register_user()
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Email already in use')

    def test_invalid_email_registration(self):
        """Test registration with invalid email format"""
        response = self.register_user(email='invalid-email')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid email format')

    def test_short_password_registration(self):
        """Test registration with too short password"""
        response = self.register_user(password='short')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Password must be at least 8 characters long')

    def test_successful_login(self):
        """Test successful login"""
        # Register user first
        self.register_user()
        
        # Try to login
        response = self.login_user()
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertIn('token', data)
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test@example.com')

    def test_login_with_wrong_password(self):
        """Test login with incorrect password"""
        # Register user first
        self.register_user()
        
        # Try to login with wrong password
        response = self.login_user(password='wrongpassword')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """Test login with email that doesn't exist"""
        response = self.login_user(email='nonexistent@example.com')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Invalid credentials')

    def test_password_hashing(self):
        """Test that passwords are properly hashed in the database"""
        self.register_user()
        from app.models import User
        user = User.query.filter_by(email='test@example.com').first()
        
        # Check that password is hashed
        self.assertNotEqual(user.password_hash, 'password123')
        # Check that password verification works
        self.assertTrue(user.check_password('password123'))
