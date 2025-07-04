from django.core.management.base import BaseCommand
from users.models import CustomUser
from tracker.models import Transaction
from users.session_utils import get_logged_in_user
from django.db.models import Sum

class Command(BaseCommand):
    help = "View your transactions"

    def add_arguments(self, parser):
        parser.add_argument('--type', help="Filter by type: income or expense")
        parser.add_argument('--category', help="Filter by category name")

    def handle(self, *args, **options):
        username = get_logged_in_user()

        if not username:
            self.stdout.write(self.style.ERROR("Please login first!"))
            return
        
        user = CustomUser.objects.get(username=username)

        transactions = Transaction.objects.filter(user=user)

        if options['type']:
            transactions = transactions.filter(type=options['type'].lower())

        if options['category']:
            transactions = transactions.filter(category__iexact=options['category'])

        transactions = transactions.order_by('-date')

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

