from django.test import TestCase
from django.core.management import call_command
from users.models import CustomUser
from tracker.models import Transaction, Budget
from io import StringIO
import os
import json
from unittest.mock import patch

class RemainingTrackerCommandTests(TestCase):
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

        Transaction.objects.create(user=self.user, type="income", amount=5000, category="Salary")
        Transaction.objects.create(user=self.user, type="expense", amount=1000, category="Food")
        Budget.objects.create(user=self.user, category="Food", category_limit=1500)

    def tearDown(self):
        if os.path.exists("session.txt"):
            os.remove("session.txt")
        if os.path.exists("backup.json"):
            os.remove("backup.json")

    def test_backup_data_command(self):
        out = StringIO()
        call_command("backup_data", stdout=out)
        self.assertTrue(os.path.exists("backup.json"))
        self.assertIn("Backup completed successfully", out.getvalue())

    def test_restore_data_command(self):
        call_command("backup_data")
        Transaction.objects.all().delete()
        Budget.objects.all().delete()

        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Budget.objects.count(), 0)

        out = StringIO()
        call_command("restore_data", stdout=out)
        self.assertGreater(Transaction.objects.count(), 0)
        self.assertGreater(Budget.objects.count(), 0)
        self.assertIn("Data restored successfully", out.getvalue())

    def test_check_budget_command(self):
        out = StringIO()
        call_command("check_budget", stdout=out)
        self.assertIn("Category-wise Budget Check", out.getvalue())
        self.assertIn("Food", out.getvalue())

    @patch("builtins.input", side_effect=["Food", "1200"])
    def test_set_budget_command(self, mock_input):
        out = StringIO()
        call_command("set_budget", stdout=out)
        self.assertTrue(Budget.objects.filter(user=self.user, category="Food").exists())
        self.assertIn("Budget set for category 'Food'", out.getvalue())

    def test_monthly_report_command(self):
        out = StringIO()
        call_command("monthly_report", stdout=out)
        self.assertIn("Monthly Financial Report", out.getvalue())

    def test_yearly_report_command(self):
        out = StringIO()
        call_command("yearly_report", stdout=out)
        self.assertIn("Yearly Financial Report", out.getvalue())
