from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import BankAccount
from transactions.models import Transaction

class TransactionsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='password123')
        self.account1 = BankAccount.objects.create(
            user=self.user1,
            account_number='1111111111',
            account_holder_name='Alice Smith',
            balance=500.00
        )

        self.user2 = User.objects.create_user(username='bob', password='password123')
        self.account2 = BankAccount.objects.create(
            user=self.user2,
            account_number='2222222222',
            account_holder_name='Bob Jones',
            balance=200.00
        )

    def test_deposit(self):
        self.client.login(username='alice', password='password123')
        response = self.client.post('/deposit/', {'amount': '150.00', 'description': 'Test Deposit'})
        self.assertEqual(response.status_code, 302)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 650.00)
        self.assertEqual(Transaction.objects.filter(account=self.account1, transaction_type='DEPOSIT').count(), 1)

    def test_withdraw_success(self):
        self.client.login(username='alice', password='password123')
        response = self.client.post('/withdraw/', {'amount': '200.00', 'description': 'Test Withdrawal'})
        self.assertEqual(response.status_code, 302)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 300.00)
        self.assertEqual(Transaction.objects.filter(account=self.account1, transaction_type='WITHDRAWAL').count(), 1)

    def test_withdraw_overdraft_prevention(self):
        self.client.login(username='alice', password='password123')
        response = self.client.post('/withdraw/', {'amount': '1000.00', 'description': 'Excessive Withdrawal'})
        self.account1.refresh_from_db()
        # Balance should remain unchanged at 500.00
        self.assertEqual(self.account1.balance, 500.00)

    def test_data_isolation(self):
        # Ensure user1 cannot see user2's transactions
        Transaction.objects.create(
            account=self.account2,
            transaction_type='DEPOSIT',
            amount=100.00,
            balance_after_transaction=300.00,
            description="Bob's private transaction"
        )
        self.client.login(username='alice', password='password123')
        response = self.client.get('/history/')
        self.assertNotContains(response, "Bob's private transaction")
