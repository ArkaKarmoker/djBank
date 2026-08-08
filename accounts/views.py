from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserLoginForm
from .models import BankAccount
from transactions.models import Transaction

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                account_num = BankAccount.generate_account_number()
                holder_name = f"{user.first_name} {user.last_name}".strip() or user.username
                initial_deposit = form.cleaned_data.get('initial_deposit') or 0

                account = BankAccount.objects.create(
                    user=user,
                    account_number=account_num,
                    account_holder_name=holder_name,
                    balance=initial_deposit
                )

                if initial_deposit > 0:
                    Transaction.objects.create(
                        account=account,
                        transaction_type='DEPOSIT',
                        amount=initial_deposit,
                        balance_after_transaction=initial_deposit,
                        description="Initial Account Deposit"
                    )

            login(request, user)
            messages.success(request, f"Welcome {holder_name}! Your bank account (#{account_num}) was successfully created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')
