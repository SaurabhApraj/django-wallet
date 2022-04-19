from django.contrib import admin
from .models import User, TransactionHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','transaction_amount','created_at']
    search_fields = ['user']