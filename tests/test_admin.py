import json
from tests.base import BaseTestCase
from app.models import User
from app import db

class TestAdmin(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create and login an admin user
        self.admin = self.create_admin_user()
        response = self.login_user(email='admin@example.com', password='admin123')
        data = json.loads(response.data)
        self.admin_headers = self.get_auth_headers(data['token'])
        
        # Create a regular user
        self.regular_user = self.create_test_user(
            email='user@example.com',
            password='password123',
            name='Regular User'
        )
        response = self.login_user(email='user@example.com', password='password123')
        data = json.loads(response.data)
        self.user_headers = self.get_auth_headers(data['token'])

    def create_admin_user(self):
        admin = User(
            email='admin@example.com',
            name='Admin User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        return admin

    def test_list_users_as_admin(self):
        """Test that admin can list all users"""
        response = self.client.get('/admin/users', headers=self.admin_headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(len(data['users']), 2)  # admin and regular user
        
        # Verify user details are included
        users_emails = [user['email'] for user in data['users']]
        self.assertIn('admin@example.com', users_emails)
        self.assertIn('user@example.com', users_emails)

    def test_list_users_as_regular_user(self):
        """Test that regular users cannot list users"""
        response = self.client.get('/admin/users', headers=self.user_headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Admin privileges required')

    def test_get_specific_user_as_admin(self):
        """Test that admin can get specific user details"""
        response = self.client.get(
            f'/admin/users/{self.regular_user.id}',
            headers=self.admin_headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['user']['email'], 'user@example.com')
        self.assertEqual(data['user']['name'], 'Regular User')

    def test_get_nonexistent_user_as_admin(self):
        """Test getting a user that doesn't exist"""
        response = self.client.get('/admin/users/999', headers=self.admin_headers)
        self.assertEqual(response.status_code, 404)

    def test_toggle_admin_status(self):
        """Test toggling admin status of a user"""
        # Toggle regular user to admin
        response = self.client.post(
            f'/admin/users/{self.regular_user.id}/toggle-admin',
            headers=self.admin_headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertTrue(data['user']['is_admin'])
        
        # Verify in database
        user = User.query.get(self.regular_user.id)
        self.assertTrue(user.is_admin)
        
        # Toggle back to regular user
        response = self.client.post(
            f'/admin/users/{self.regular_user.id}/toggle-admin',
            headers=self.admin_headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertFalse(data['user']['is_admin'])
        
        # Verify in database
        user = User.query.get(self.regular_user.id)
        self.assertFalse(user.is_admin)

    def test_admin_cannot_toggle_own_status(self):
        """Test that admin cannot toggle their own admin status"""
        response = self.client.post(
            f'/admin/users/{self.admin.id}/toggle-admin',
            headers=self.admin_headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Cannot modify your own admin status')
        
        # Verify admin status unchanged
        admin = User.query.get(self.admin.id)
        self.assertTrue(admin.is_admin)

    def test_regular_user_cannot_toggle_admin_status(self):
        """Test that regular users cannot toggle admin status"""
        response = self.client.post(
            f'/admin/users/{self.regular_user.id}/toggle-admin',
            headers=self.user_headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Admin privileges required')
        
        # Verify status unchanged
        user = User.query.get(self.regular_user.id)
        self.assertFalse(user.is_admin)
