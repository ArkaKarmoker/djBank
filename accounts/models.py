import random
from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=10, unique=True)
    account_holder_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_holder_name} ({self.account_number}) - ${self.balance}"

    @staticmethod
    def generate_account_number():
        """Generates a unique 10-digit account number."""
        while True:
            account_num = str(random.randint(1000000000, 9999999999))
            if not BankAccount.objects.filter(account_number=account_num).exists():
                return account_num
