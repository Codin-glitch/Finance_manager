from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferred_currency = models.CharField(max_length=5, default='INR')

    def __str__(self):
        return self.username
    
