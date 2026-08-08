from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'transaction_type', 'amount', 'balance_after_transaction', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('account__account_number', 'account__account_holder_name', 'description')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
