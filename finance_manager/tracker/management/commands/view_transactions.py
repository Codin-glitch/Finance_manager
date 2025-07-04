from django.core.management.base import BaseCommand
from users.models import CustomUser
from tracker.models import Transaction
from users.session_utils import get_logged_in_user
from django.db.models import Sum

class Command(BaseCommand):
    help = "View your transactions"

    def handle(self, *args, **kwargs):
        username = get_logged_in_user()

        if not username:
            self.stdout.write(self.style.ERROR("Please login first!"))
            return
        
        user = CustomUser.objects.get(username=username)

        transactions = Transaction.objects.filter(user=user).order_by("-date")

        if not transactions.exists():
            self.stdout.write(self.style.WARNING("No transactions found!"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"\n Transactions for {username}:\n"))
        
        for t in transactions:
            currency = user.preferred_currency
            self.stdout.write(f"[{t.date}] {t.type.title()} - {currency}{t.amount} ({t.category})")

        income_total = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_total = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        savings = income_total - expense_total

        self.stdout.write("\n--- Summary ---")
        self.stdout.write(f"Total Income:  {user.preferred_currency}{income_total}")
        self.stdout.write(f"Total Expense: {user.preferred_currency}{expense_total}")
        self.stdout.write(f"Savings:       {user.preferred_currency}{savings}")

