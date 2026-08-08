import csv
import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.core.paginator import Paginator

from accounts.models import BankAccount
from .models import Transaction
from .forms import DepositForm, WithdrawForm, TransactionFilterForm

def get_user_account(user):
    """Utility function to ensure user has a BankAccount object."""
    account, created = BankAccount.objects.get_or_create(
        user=user,
        defaults={
            'account_number': BankAccount.generate_account_number(),
            'account_holder_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'balance': Decimal('0.00')
        }
    )
    return account

@login_required
def dashboard_view(request):
    account = get_user_account(request.user)
    transactions_qs = Transaction.objects.filter(account=account)

    total_deposits = transactions_qs.filter(transaction_type='DEPOSIT').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_withdrawals = transactions_qs.filter(transaction_type='WITHDRAWAL').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_transactions_count = transactions_qs.count()

    recent_transactions = transactions_qs[:5]

    # Monthly Summary Breakdown
    monthly_summary = (
        transactions_qs
        .annotate(month=TruncMonth('timestamp'))
        .values('month', 'transaction_type')
        .annotate(total_amount=Sum('amount'), count=Count('id'))
        .order_by('-month')
    )

    # Process monthly data for table display
    summary_dict = {}
    for entry in monthly_summary:
        month_str = entry['month'].strftime('%B %Y')
        if month_str not in summary_dict:
            summary_dict[month_str] = {'deposits': Decimal('0.00'), 'withdrawals': Decimal('0.00')}
        if entry['transaction_type'] == 'DEPOSIT':
            summary_dict[month_str]['deposits'] = entry['total_amount']
        elif entry['transaction_type'] == 'WITHDRAWAL':
            summary_dict[month_str]['withdrawals'] = entry['total_amount']

    # Visual chart data: last 10 transactions in chronological order for balance trend line chart
    trend_transactions = list(transactions_qs.order_by('timestamp')[:10])
    chart_dates = [t.timestamp.strftime('%b %d %H:%M') for t in trend_transactions]
    chart_balances = [float(t.balance_after_transaction) for t in trend_transactions]

    context = {
        'account': account,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_transactions_count': total_transactions_count,
        'recent_transactions': recent_transactions,
        'monthly_summary': summary_dict,
        'chart_dates': json.dumps(chart_dates),
        'chart_balances': json.dumps(chart_balances),
    }
    return render(request, 'dashboard.html', context)

@login_required
def deposit_view(request):
    account = get_user_account(request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description') or "Deposit"

            with db_transaction.atomic():
                # Lock row to prevent race conditions
                acc = BankAccount.objects.select_for_update().get(id=account.id)
                acc.balance += amount
                acc.save()

                Transaction.objects.create(
                    account=acc,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    balance_after_transaction=acc.balance,
                    description=description
                )

            messages.success(request, f"Successfully deposited ${amount:,.2f}! Your new balance is ${acc.balance:,.2f}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to complete deposit. Please check input values.")
    else:
        form = DepositForm()

    return render(request, 'transactions/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw_view(request):
    account = get_user_account(request.user)

    if request.method == 'POST':
        form = WithdrawForm(request.POST, account=account)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description') or "Withdrawal"

            with db_transaction.atomic():
                acc = BankAccount.objects.select_for_update().get(id=account.id)

                if amount > acc.balance:
                    messages.error(request, f"Overdraft prevented! Your current balance is ${acc.balance:,.2f}.")
                    return redirect('withdraw')

                acc.balance -= amount
                acc.save()

                Transaction.objects.create(
                    account=acc,
                    transaction_type='WITHDRAWAL',
                    amount=amount,
                    balance_after_transaction=acc.balance,
                    description=description
                )

            messages.success(request, f"Successfully withdrew ${amount:,.2f}! Your remaining balance is ${acc.balance:,.2f}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to complete withdrawal. Please correct the errors below.")
    else:
        form = WithdrawForm(account=account)

    return render(request, 'transactions/withdraw.html', {'form': form, 'account': account})

@login_required
def transaction_history_view(request):
    account = get_user_account(request.user)
    transactions_qs = Transaction.objects.filter(account=account)

    filter_form = TransactionFilterForm(request.GET)
    if filter_form.is_valid():
        search_query = filter_form.cleaned_data.get('search')
        tx_type = filter_form.cleaned_data.get('transaction_type')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')

        if search_query:
            clean_q = search_query.strip().lstrip('#')
            if clean_q.isdigit():
                transactions_qs = transactions_qs.filter(
                    Q(description__icontains=search_query) | Q(id=clean_q)
                )
            else:
                transactions_qs = transactions_qs.filter(
                    description__icontains=search_query
                )
        if tx_type:
            transactions_qs = transactions_qs.filter(transaction_type=tx_type)
        if start_date:
            transactions_qs = transactions_qs.filter(timestamp__date__gte=start_date)
        if end_date:
            transactions_qs = transactions_qs.filter(timestamp__date__lte=end_date)

    paginator = Paginator(transactions_qs, 8)  # 8 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Clean query parameters by removing 'page' to prevent parameter duplication
    get_copy = request.GET.copy()
    get_copy.pop('page', None)
    clean_query_params = get_copy.urlencode()

    context = {
        'account': account,
        'page_obj': page_obj,
        'filter_form': filter_form,
        'query_params': clean_query_params,
    }
    return render(request, 'transactions/history.html', context)

@login_required
def export_csv_view(request):
    account = get_user_account(request.user)
    transactions_qs = Transaction.objects.filter(account=account)

    search_query = request.GET.get('search')
    tx_type = request.GET.get('transaction_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if search_query:
        clean_q = search_query.strip().lstrip('#')
        if clean_q.isdigit():
            transactions_qs = transactions_qs.filter(
                Q(description__icontains=search_query) | Q(id=clean_q)
            )
        else:
            transactions_qs = transactions_qs.filter(
                description__icontains=search_query
            )
    if tx_type:
        transactions_qs = transactions_qs.filter(transaction_type=tx_type)
    if start_date:
        transactions_qs = transactions_qs.filter(timestamp__date__gte=start_date)
    if end_date:
        transactions_qs = transactions_qs.filter(timestamp__date__lte=end_date)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename=statement_{account.account_number}.csv'

    writer = csv.writer(response)
    writer.writerow(['Transaction ID', 'Date & Time', 'Type', 'Amount ($)', 'Balance After ($)', 'Description'])

    for tx in transactions_qs:
        writer.writerow([
            tx.id,
            tx.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            tx.transaction_type,
            f"{tx.amount:.2f}",
            f"{tx.balance_after_transaction:.2f}",
            tx.description or ''
        ])

    return response
