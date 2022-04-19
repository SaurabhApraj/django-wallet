from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=50)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits = 7, decimal_places = 2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = "user"


class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user_transactionhistory')
    transaction_amount = models.DecimalField(max_digits = 7, decimal_places = 2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, max_length=50, related_name='addedby_transactionhistory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TransactionHistory'
        verbose_name_plural = 'Transaction Histories'
        db_table = "transaction_history"