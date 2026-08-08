from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import BankAccount

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')

    def test_account_creation_signal_or_manual(self):
        account = BankAccount.objects.create(
            user=self.user,
            account_number='1234567890',
            account_holder_name='Test User',
            balance=100.00
        )
        self.assertEqual(account.balance, 100.00)
        self.assertEqual(account.user.username, 'testuser')

    def test_registration_view(self):
        response = self.client.post('/auth/register/', {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'initial_deposit': '250.00'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newuser')
        self.assertTrue(BankAccount.objects.filter(user=new_user).exists())
        self.assertEqual(new_user.account.balance, 250.00)
