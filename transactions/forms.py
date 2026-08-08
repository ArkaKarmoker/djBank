from django import forms
from decimal import Decimal

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal('0.01'), required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter deposit amount (e.g. 100.00)',
            'step': '0.01',
            'min': '0.01'
        })
    )
    description = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional note/description (e.g. Salary, Gift)'
        })
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= Decimal('0.00'):
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal('0.01'), required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter withdrawal amount (e.g. 50.00)',
            'step': '0.01',
            'min': '0.01'
        })
    )
    description = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional note/description (e.g. Rent, Grocery)'
        })
    )

    def __init__(self, *args, account=None, **kwargs):
        self.account = account
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= Decimal('0.00'):
            raise forms.ValidationError("Withdrawal amount must be greater than zero.")

        if self.account and amount > self.account.balance:
            raise forms.ValidationError(
                f"Insufficient funds! Available balance is ${self.account.balance:,.2f}."
            )

        return amount


class TransactionFilterForm(forms.Form):
    TYPE_CHOICES = (
        ('', 'All Types'),
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    )

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filter-input', 'placeholder': 'Search description...'})
    )
    transaction_type = forms.ChoiceField(
        choices=TYPE_CHOICES, required=False,
        widget=forms.Select(attrs={'class': 'form-select filter-select'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control filter-input', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control filter-input', 'type': 'date'})
    )
