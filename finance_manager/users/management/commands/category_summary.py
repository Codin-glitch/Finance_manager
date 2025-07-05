from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from django.db.models import Sum

class Command(BaseCommand):
    help = "Show category-wise summary of income and expenses"

    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR(" Please login first."))
            return

        user = CustomUser.objects.get(username=username)
        transactions = Transaction.objects.filter(user=user)

        if not transactions.exists():
            self.stdout.write(self.style.WARNING("No transactions to summarize."))
            return

        currency = user.preferred_currency

        self.stdout.write(self.style.SUCCESS(f"\n Category-wise Summary for {username}:\n"))

        # Expense Summary
        expense_summary = transactions.filter(type='expense') \
            .values('category') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')

        if expense_summary:
            self.stdout.write("Expense by Category:")
            for item in expense_summary:
                self.stdout.write(f"{item['category']:<12} {currency}{item['total']}")
        else:
            self.stdout.write("No expenses recorded.")

        # Income Summary
        income_summary = transactions.filter(type='income') \
            .values('category') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')

        if income_summary:
            self.stdout.write("\nIncome by Category:")
            for item in income_summary:
                self.stdout.write(f"{item['category']:<12} {currency}{item['total']}")
        else:
            self.stdout.write("No income recorded.")
