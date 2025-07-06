import json
from django.core.management.base import BaseCommand
from tracker.models import Transaction, Budget
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from datetime import datetime

class Command(BaseCommand):
    help = "Restore transactions and budgets from backup.json"

    def handle(self, *args, **kwargs):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)

        try:
            with open("backup.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("No backup file found."))
            return

        # Restore Transactions
        for t in data.get("transactions", []):
            Transaction.objects.get_or_create(
            user=user,
            type=t['type'],
            amount=t['amount'],
            category=t['category'],
            description=t.get('description', ''),
            date=datetime.fromisoformat(t['date'])
        )

        # Restore Budgets
        for b in data.get("budgets", []):
            Budget.objects.update_or_create(
                user=user,
                category=b['category'],
                month=datetime.fromisoformat(b['month']),
                defaults={'amount': b['amount']}
            )

        self.stdout.write(self.style.SUCCESS("Data restored from backup.json"))
