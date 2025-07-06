import json
from django.core.management.base import BaseCommand
from tracker.models import Transaction, Budget
from users.models import CustomUser
from users.session_utils import get_logged_in_user

class Command(BaseCommand):
    help = "Backup user transactions and budgets to backup.json"

    def handle(self, *args, **kwargs):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)

        transactions = list(Transaction.objects.filter(user=user).values())
        budgets = list(Budget.objects.filter(user=user).values())

        data = {
            "transactions": transactions,
            "budgets": budgets
        }

        with open("backup.json", "w") as f:
            json.dump(data, f, indent=4, default=str)

        self.stdout.write(self.style.SUCCESS("Backup completed successfully! File: backup.json"))
