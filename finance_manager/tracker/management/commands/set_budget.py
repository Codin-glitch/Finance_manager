from django.core.management.base import BaseCommand
from tracker.models import Budget
from users.models import CustomUser
from users.session_utils import get_logged_in_user
from datetime import datetime

class Command(BaseCommand):
    help = "Set monthly budget for a category"

    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)

        category = input("Enter category: ").strip().title()
        amount_input = input("Enter monthly budget amount: ").strip()

        try:
            amount = float(amount_input)
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid amount"))
            return

        month_input = input("Enter month (YYYY-MM): ").strip()
        try:
            month = datetime.strptime(month_input + "-01", "%Y-%m-%d").date()
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid month format. Use YYYY-MM"))
            return

        budget, created = Budget.objects.update_or_create(
            user=user,
            category=category,
            month=month,
            defaults={'amount': amount}
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Budget created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS("Budget updated successfully."))
