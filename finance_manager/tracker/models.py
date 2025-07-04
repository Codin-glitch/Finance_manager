from django.db import models
from users.models import CustomUser


class Transaction(models.Model):
    TRANSACTION_TYPES = {
        ('income', 'Income'),
        ('expense', 'Expense'),
    }

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50)
    description = models.CharField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} - {self.user.preferred_currency} {self.amount} ({self.category})"
