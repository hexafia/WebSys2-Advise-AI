from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class RoleBasedAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create Student User
        self.student_user = User.objects.create_user(username='student@test.com', password='password123')
        UserProfile.objects.create(user=self.student_user, role='student')
        
        # Create Adviser User
        self.adviser_user = User.objects.create_user(username='adviser@test.com', password='password123')
        UserProfile.objects.create(user=self.adviser_user, role='adviser')
        
        # Create Admin User
        self.admin_user = User.objects.create_user(username='admin@test.com', password='password123', is_superuser=True)
        UserProfile.objects.create(user=self.admin_user, role='admin')

    def test_student_cannot_access_adviser_dashboard(self):
        self.client.login(username='student@test.com', password='password123')
        response = self.client.get(reverse('adviser_dashboard'))
        # Should redirect to student dashboard because of the decorator logic
        self.assertRedirects(response, reverse('student_dashboard'))
        
    def test_adviser_cannot_access_student_dashboard(self):
        self.client.login(username='adviser@test.com', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        # Should redirect to adviser dashboard
        self.assertRedirects(response, reverse('adviser_dashboard'))

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('student_dashboard')}", target_status_code=200, fetch_redirect_response=False)
        # Handle the fact that our decorators might just redirect directly to login without the ?next= parameter, let's use a looser check
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)
        
    def test_student_can_access_student_dashboard(self):
        self.client.login(username='student@test.com', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_adviser_can_access_adviser_dashboard(self):
        self.client.login(username='adviser@test.com', password='password123')
        response = self.client.get(reverse('adviser_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='admin@test.com', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
