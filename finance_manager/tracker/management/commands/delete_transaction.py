from django.core.management.base import BaseCommand
from tracker.models import Transaction
from users.models import CustomUser
from users.session_utils import get_logged_in_user

class Command(BaseCommand):
    help = "Delete a user using id"

    def add_arguments(self, parser):
        return parser.add_argument('--id', type=int, help='Transaction id to delete')

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

        confirm = input(f"Are you sure you want to delete this transaction? (y/n): ")
        if confirm.lower() == 'y':
            transaction.delete()
            self.stdout.write(self.style.SUCCESS("Transaction deleted successfully!"))
        else:
            self.stdout.write(self.style.WARNING("Deletion cancelled."))