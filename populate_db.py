import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_management.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import BankAccount
from transactions.models import Transaction

def create_sample_data():
    print("Resetting database and populating with fresh realistic sample data...")
    
    # 0. Clean full database (completely wipe all data for a fresh start)
    from django.core.management import call_command
    call_command('flush', interactive=False)

    # 1. Create Superuser (Admin)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created Superuser: admin")

    now = timezone.now()

    # Define User Profiles
    users_data = [
        {
            'username': 'arka_karmoker',
            'first_name': 'Arka',
            'last_name': 'Karmoker',
            'email': 'arka@example.com',
            'password': 'Password123',
            'account_number': '1002003004',
            'base_salary': Decimal('5500.00'),
            'transaction_count': 50
        },
        {
            'username': 'john_doe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123',
            'account_number': '1002948192',
            'base_salary': Decimal('4500.00'),
            'transaction_count': 35
        },
        {
            'username': 'jane_smith',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'password': 'Password123',
            'account_number': '9876543210',
            'base_salary': Decimal('3800.00'),
            'transaction_count': 25
        }
    ]

    deposit_desc = [
        "Freelance Client Payment", "Stock Dividend", "Cashback Reward", 
        "Sold Old Laptop", "Birthday Gift", "Consulting Fee", "Tax Refund"
    ]
    
    withdraw_desc = [
        "Supermarket Groceries", "Apartment Rent", "Electric & Water Bill",
        "Restaurant Dinner", "Netflix Subscription", "Gym Membership",
        "Spotify Premium", "Uber Ride", "Coffee Shop", "Amazon Purchase",
        "Internet Bill", "Car Maintenance", "Pharmacy"
    ]

    for u_data in users_data:
        # Create User
        user, created = User.objects.get_or_create(
            username=u_data['username'],
            defaults={
                'first_name': u_data['first_name'],
                'last_name': u_data['last_name'],
                'email': u_data['email']
            }
        )
        if created:
            user.set_password(u_data['password'])
            user.save()

        # Create Bank Account
        acc, _ = BankAccount.objects.get_or_create(
            user=user,
            defaults={
                'account_number': u_data['account_number'],
                'account_holder_name': f"{u_data['first_name']} {u_data['last_name']}",
                'balance': Decimal('0.00')
            }
        )
        
        # Clear existing transactions for this user
        Transaction.objects.filter(account=acc).delete()

        running_balance = Decimal('0.00')
        transactions_to_create = []

        # Generate Transactions over the last 90 days
        for i in range(u_data['transaction_count'], 0, -1):
            days_ago = i * (90 / u_data['transaction_count']) # spread over 90 days
            tx_date = now - timedelta(days=days_ago)
            
            # Every ~10th transaction is a salary deposit
            if i % 10 == 0 or i == u_data['transaction_count']:
                tx_type = 'DEPOSIT'
                amount = u_data['base_salary']
                desc = "Monthly Salary Credit"
            else:
                # 30% chance deposit, 70% chance withdrawal
                is_deposit = random.random() < 0.3
                
                if is_deposit:
                    tx_type = 'DEPOSIT'
                    amount = Decimal(random.randint(50, 500)) + Decimal(random.randint(0, 99)) / 100
                    desc = random.choice(deposit_desc)
                else:
                    tx_type = 'WITHDRAWAL'
                    amount = Decimal(random.randint(15, 200)) + Decimal(random.randint(0, 99)) / 100
                    desc = random.choice(withdraw_desc)
                    
                    # Prevent overdraft during generation
                    if running_balance - amount < 0:
                        continue # Skip this transaction to avoid negative balance

            if tx_type == 'DEPOSIT':
                running_balance += amount
            else:
                running_balance -= amount

            transactions_to_create.append({
                'account': acc,
                'transaction_type': tx_type,
                'amount': amount,
                'balance_after_transaction': running_balance,
                'description': desc,
                'timestamp': tx_date
            })

        # Save all transactions in chronological order
        for tx_data in transactions_to_create:
            tx = Transaction.objects.create(
                account=tx_data['account'],
                transaction_type=tx_data['transaction_type'],
                amount=tx_data['amount'],
                balance_after_transaction=tx_data['balance_after_transaction'],
                description=tx_data['description']
            )
            # We must set timestamp after creation because auto_now_add might override it on initial save
            Transaction.objects.filter(id=tx.id).update(timestamp=tx_data['timestamp'])

        # Update final balance
        acc.balance = running_balance
        acc.save()

        print(f"Generated {len(transactions_to_create)} transactions for {u_data['first_name']} {u_data['last_name']}. Final Balance: ${running_balance}")

    print("\nDatabase seeded successfully!")
    print("Demo Users:")
    print("1. Username: arka_karmoker | Password: Password123")
    print("2. Username: john_doe | Password: Password123")
    print("3. Username: jane_smith | Password: Password123")

if __name__ == '__main__':
    create_sample_data()
