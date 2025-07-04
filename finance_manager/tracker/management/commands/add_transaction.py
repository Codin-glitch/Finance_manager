from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user

class Command(BaseCommand):
    help = "Add an income or expense transaction"

    def handle(self, *args, **kwargs):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)

        type = input("Enter type (income/expense): ").lower()
        if type not in ['income', 'expense']:
            self.stdout.write(self.style.ERROR("Invalid type. Must be 'income' or 'expense'."))
            return

        try:
            amount = float(input("Amount: "))
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid amount. Must be a number."))
            return

        category = input("Category (e.g., Food, Salary, Rent): ").capitalize()
        description = input("Description (optional): ")

        Transaction.objects.create(
            user=user,
            type=type,
            amount=amount,
            category=category,
            description=description
        )

        self.stdout.write(self.style.SUCCESS(f"{type.title()} of {user.preferred_currency}{amount} added."))
