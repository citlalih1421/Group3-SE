from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class AccountTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, is_buyer=True)
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.account_url = reverse('account')
        self.payment_methods_url = reverse('payment_methods')
        self.shipping_methods_url = reverse('shipping_methods')

    def test_register(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'is_buyer': True,
            'is_seller': False
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username_or_email': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login
        self.assertTrue('_auth_user_id' in self.client.session)  # User should be logged in

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)  # User should be logged out

    def test_account_access(self):
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page if not logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)  # Should return status code 200 if logged in

    def test_payment_methods_access(self):
        response = self.client.get(self.payment_methods_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page if not logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.payment_methods_url)
        self.assertEqual(response.status_code, 200)  # Should return status code 200 if logged in

    def test_shipping_methods_access(self):
        response = self.client.get(self.shipping_methods_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page if not logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.shipping_methods_url)
        self.assertEqual(response.status_code, 200)  # Should return status code 200 if logged in

    