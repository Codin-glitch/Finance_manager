from django.core.management.base import BaseCommand
from tracker.models import Transaction, Budget
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from django.db.models import Sum
from datetime import date

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

        category = input("Category (e.g., Food, Salary, Rent): ").strip().title()
        description = input("Description (optional): ")

        transaction = Transaction.objects.create(
            user=user,
            type=type,
            amount=amount,
            category=category,
            description=description
        )

        self.stdout.write(self.style.SUCCESS(f"{type.title()} of {user.preferred_currency}{amount} added."))

        # Budget limit checker
        if type == 'expense':
            today = date.today()
            month_start = today.replace(day=1)
            if today.month == 12:
                next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                next_month = today.replace(month=today.month + 1, day=1)

            monthly_expense = Transaction.objects.filter(
                user=user,
                type='expense',
                category=category,
                date__gte=month_start,
                date__lt=next_month
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            budget = Budget.objects.filter(
                user=user,
                category=category,
                month__year=today.year,
                month__month=today.month
            ).first()

            if budget:
                if monthly_expense > budget.amount:
                    self.stdout.write(self.style.WARNING(
                        f"You've exceeded your budget for {category}! Limit: {user.preferred_currency}{budget.amount}"
                    ))
                else:
                    remaining = budget.amount - monthly_expense
                    self.stdout.write(self.style.SUCCESS(
                        f"You're within budget for {category}. Remaining: {user.preferred_currency}{remaining}"
                    ))
