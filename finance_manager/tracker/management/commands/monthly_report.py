from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from django.db.models import Sum
from django.db.models.functions import TruncMonth

class Command(BaseCommand):
    help = "Show monthly financial report"

    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)
        transactions = Transaction.objects.filter(user=user)

        if not transactions.exists():
            self.stdout.write(self.style.WARNING("No transactions found."))
            return

        currency = user.preferred_currency

        self.stdout.write(self.style.SUCCESS(f"\nMonthly Report for {username}:\n"))

        monthly_summary = transactions.annotate(month=TruncMonth('date')) \
            .values('month', 'type') \
            .annotate(total=Sum('amount')) \
            .order_by('month')

        report = {}

        for entry in monthly_summary:
            month = entry['month'].strftime('%B %Y')
            if month not in report:
                report[month] = {'income': 0, 'expense': 0}
            report[month][entry['type']] = entry['total']

        for month, totals in report.items():
            income = totals.get('income', 0)
            expense = totals.get('expense', 0)
            savings = income - expense
            self.stdout.write(f"{month}")
            self.stdout.write(f"  Income:  {currency}{income}")
            self.stdout.write(f"  Expense: {currency}{expense}")
            self.stdout.write(f"  Savings: {currency}{savings}\n")
