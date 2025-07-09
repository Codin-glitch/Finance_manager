from django.test import TestCase
from django.core.management import call_command
from users.models import CustomUser
from tracker.models import Transaction, Budget
from io import StringIO
from unittest.mock import patch
from datetime import date
import re
import os

class TrackerCommandTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            preferred_currency="₹",
            monthly_budget=10000,
            
        )
        os.makedirs("users", exist_ok=True)
        with open("session.txt", "w") as f:
            f.write("testuser")

        Transaction.objects.create(user=self.user, type="income", amount=5000, category="Salary")
        Transaction.objects.create(user=self.user, type="expense", amount=1000, category="Food")
        Budget.objects.create(user=self.user, category="Food", amount=1500,month=date.today().replace(day=1))

    def tearDown(self):
        if os.path.exists("session.txt"):
            os.remove("session.txt")
        if os.path.exists("backup.json"):
            os.remove("backup.json")

    def test_backup_data_command(self):
        out = StringIO()
        call_command("backup_data", stdout=out)
        self.assertTrue(os.path.exists("backup.json"))
        self.assertIn("Backup completed successfully! File: backup.json", out.getvalue())

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
        self.assertIn("Data restored from backup.json", out.getvalue())

    @patch("builtins.input", side_effect=["Food", "1500", "2025-07"])
    def test_set_budget_command(self, mock_input):
        out = StringIO()
        call_command("set_budget", stdout=out)
        output = re.sub(r"\x1b\[[0-9;]*m", "", out.getvalue())

        self.assertIn("Budget updated successfully.\n", output)
        self.assertTrue(Budget.objects.filter(user=self.user, category="Food", month="2025-07-01").exists())


    def test_check_budget_command(self):
        out = StringIO()
        call_command("check_budget", "--category=Food", stdout=out)
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', out.getvalue())
        self.assertIn(f"Budget for Food", clean_output)
        self.assertIn("Set Budget:", clean_output)
        self.assertIn("Spent So Far:", clean_output)
        self.assertIn("Remaining:", clean_output)
        

    def test_monthly_report_command(self):
        out = StringIO()
        call_command("monthly_report", stdout=out)
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', out.getvalue())
        self.assertIn("Monthly Report for testuser", clean_output)

    def test_yearly_report_command(self):
        out = StringIO()
        call_command("yearly_report", stdout=out)
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', out.getvalue())
        self.assertIn(f"Yearly Report for {self.user.username}:", clean_output)
