import os
from io import StringIO
from unittest.mock import patch
from django.test import TestCase
from django.core.management import call_command
from tracker.models import Transaction
from users.models import CustomUser

class TrackerCommandTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            preferred_currency="₹",
            monthly_budget=10000
        )
        os.makedirs("users", exist_ok=True)
        with open("session.txt", "w") as f:
            f.write("testuser")

        # Common test transactions
        Transaction.objects.create(user=self.user, type="income", amount=5000, category="Salary")
        Transaction.objects.create(user=self.user, type="income", amount=3000, category="Freelance")
        Transaction.objects.create(user=self.user, type="expense", amount=1200, category="Food")
        Transaction.objects.create(user=self.user, type="expense", amount=800, category="Rent")

        # For edit test
        self.transaction = Transaction.objects.create(
            user=self.user,
            type="expense",
            amount=400,
            category="Misc"
        )

    def tearDown(self):
        if os.path.exists("session.txt"):
            os.remove("session.txt")

    def test_category_summary_command(self):
        out = StringIO()
        call_command("category_summary", stdout=out)
        output = out.getvalue()

        self.assertIn("Category-wise Summary for testuser", output)
        self.assertIn("Salary", output)
        self.assertIn("Freelance", output)
        self.assertIn("Food", output)
        self.assertIn("Rent", output)
        self.assertIn("₹5000", output)
        self.assertIn("₹1200", output)

    def test_view_transactions_command(self):
        out = StringIO()
        call_command("view_transactions", stdout=out)
        output = out.getvalue()

        self.assertIn("Transactions for testuser", output)
        self.assertIn("Salary", output)
        self.assertIn("Freelance", output)
        self.assertIn("Food", output)
        self.assertIn("Rent", output)

    def test_view_transactions_filter_type_income(self):
        out = StringIO()
        call_command("view_transactions", '--type=income', stdout=out)
        output = out.getvalue()

        self.assertIn("Salary", output)
        self.assertIn("Freelance", output)
        self.assertNotIn("Food", output)
        self.assertNotIn("Rent", output)

    def test_view_transactions_filter_type_expense(self):
        out = StringIO()
        call_command("view_transactions", '--type=expense', stdout=out)
        output = out.getvalue()

        self.assertIn("Food", output)
        self.assertIn("Rent", output)
        self.assertNotIn("Salary", output)

    def test_view_transactions_filter_category_food(self):
        out = StringIO()
        call_command("view_transactions", '--category=Food', stdout=out)
        output = out.getvalue()

        self.assertIn("Food", output)
        self.assertNotIn("Rent", output)
        self.assertNotIn("Salary", output)

    
    # Editing transaction
    @patch("builtins.input", side_effect=["income", "1000", "Salary"])
    def test_edit_transaction_command(self, mock_input):
        out = StringIO()
        call_command("edit_transaction", f"--id={self.transaction.id}", stdout=out)

        updated = Transaction.objects.get(id=self.transaction.id)
        self.assertEqual(updated.type, "income")
        self.assertEqual(updated.amount, 1000)
        self.assertEqual(updated.category, "Salary")
        self.assertIn("Transaction updated successfully!", out.getvalue())


    # Deleting transaction
    @patch("builtins.input", side_effect=["y"])
    def test_delete_transaction(self, mock_input):
        txn = Transaction.objects.create(user=self.user, type="expense", amount=1200, category="Food")

        self.assertTrue(Transaction.objects.filter(id=txn.id).exists())

        out = StringIO()
        call_command("delete_transaction", f"--id={txn.id}", stdout=out)

        self.assertFalse(Transaction.objects.filter(id=txn.id).exists())
        self.assertIn("Transaction deleted successfully", out.getvalue())
