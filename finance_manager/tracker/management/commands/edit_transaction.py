from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user

class Command(BaseCommand):
    help = "Edit an existing transaction by ID"

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='Transaction ID to edit')

    def handle(self, *args, **options):
        username = get_logged_in_user()
        if not username:
            self.stdout.write(self.style.ERROR("Please login first."))
            return

        user = CustomUser.objects.get(username=username)
        transaction_id = options['id']

        if not transaction_id:
            self.stdout.write(self.style.ERROR("Please provide a transaction ID using --id"))
            return

        try:
            transaction = Transaction.objects.get(id=transaction_id, user=user)
        except Transaction.DoesNotExist:
            self.stdout.write(self.style.ERROR("Transaction not found or not yours."))
            return

        self.stdout.write(f"Editing: {transaction}")

        new_type = input(f"New type (income/expense) [{transaction.type}]: ") or transaction.type
        new_amount = input(f"New amount [{transaction.amount}]: ") or transaction.amount
        new_category = input(f"New category [{transaction.category}]: ") or transaction.category

        transaction.type = new_type.lower()
        transaction.amount = float(new_amount)
        transaction.category = new_category
        transaction.save()

        self.stdout.write(self.style.SUCCESS("Transaction updated successfully!"))
