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

class Budget(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text="Enter any date from the month (e.g., 2024-06-01)")

    class Meta:
        unique_together = ('user', 'category', 'month')

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.month.strftime('%B %Y')})"
