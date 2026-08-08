from django.contrib import admin
from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'account_holder_name', 'balance')
    search_fields = ('account_number', 'account_holder_name', 'user__username', 'user__email')
    ordering = ('-account_number',)
