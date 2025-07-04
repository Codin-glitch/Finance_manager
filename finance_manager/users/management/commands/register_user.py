from django.core.management.base import BaseCommand
from users.models import CustomUser
from getpass import getpass

class Command(BaseCommand):
    help = "Register a new user"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("=== User Registration ==="))

        username = input("Enter username: ")

        while True:
            password = getpass("Enter password: ")
            confirm = getpass("Confirm password: ")
            if password == confirm:
                break
            self.stdout.write(self.style.WARNING("Passwords do not match. Try again."))
        
        while True:
            monthly_budget = input("Enter monthly budget: ")
            try:
                monthly_budget = float(monthly_budget)
                if monthly_budget < 0:
                    self.stdout.write(self.style.WARNING("Budget cannot be negative. Try again."))
                    continue
                break
            except ValueError:
                self.stdout.write(self.style.WARNING("Invalid input. Please enter a number."))
            

        currency = input("Enter preferred currency (e.g., INR): ")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                monthly_budget=monthly_budget,
                preferred_currency=currency
            )
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))

