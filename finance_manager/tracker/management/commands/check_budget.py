from django.core.management.base import BaseCommand
from tracker.models import Transaction, Budget
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from django.db.models import Sum
from datetime import date

class Command(BaseCommand):
    help = "Check remaining budget for a specific category"

    def add_arguments(self, parser):
        parser.add_argument('--category', required=True, help="Category to check (e.g., Food, Rent)")

    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)
        category = options['category'].strip().title()
        today = date.today()
        month_start = today.replace(day=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)

        # Get budget entry
        budget = Budget.objects.filter(
            user=user,
            category=category,
            month__year=today.year,
            month__month=today.month
        ).first()

        if not budget:
            self.stdout.write(self.style.WARNING(f"No budget found for {category} this month."))
            return

        # Get total expense
        total_expense = Transaction.objects.filter(
            user=user,
            type='expense',
            category=category,
            date__gte=month_start,
            date__lt=next_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        remaining = budget.amount - total_expense
        currency = user.preferred_currency

        self.stdout.write(self.style.SUCCESS(f"\nBudget for {category} ({today.strftime('%B %Y')}):"))
        self.stdout.write(f"  Set Budget:    {currency}{budget.amount}")
        self.stdout.write(f"  Spent So Far:  {currency}{total_expense}")

        if remaining >= 0:
            self.stdout.write(self.style.SUCCESS(f"  Remaining:     {currency}{remaining}"))
        else:
            self.stdout.write(self.style.WARNING(f"  Over Budget By: {currency}{abs(remaining)}"))
