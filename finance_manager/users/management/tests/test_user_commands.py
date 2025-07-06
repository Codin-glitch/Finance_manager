import os
import builtins
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from users.models import CustomUser
from unittest.mock import patch

class UserCommandTests(TestCase):

    @patch("builtins.input", side_effect=["testuser", "10000", "INR"])
    @patch("getpass.getpass", side_effect=["pass123", "pass123"])
    def test_register_user(self, mock_getpass, mock_input):
        out = StringIO()
        call_command("register_user", stdout=out)

        self.assertIn("User 'testuser' created successfully!", out.getvalue())
        self.assertTrue(CustomUser.objects.filter(username="testuser").exists())

    @patch("getpass.getpass", return_value="testpass")
    def test_login_user(self, mock_getpass):
        CustomUser.objects.create_user(username="testuser", password="testpass")
        input_values = ["testuser"]

        def mock_input(_): return input_values.pop(0)

        original_input = builtins.input
        builtins.input = mock_input

        out = StringIO()
        call_command("login_user", stdout=out)

        builtins.input = original_input

        self.assertIn("Logged in as 'testuser'", out.getvalue())
        with open("session.txt", "r") as f:
            self.assertEqual(f.read().strip(), "testuser")

    def test_logout_user(self):
        with open("session.txt", "w") as f:
            f.write("testuser")

        out = StringIO()
        call_command("logout_user", stdout=out)

        self.assertIn("Successfully logged out!", out.getvalue())
        self.assertFalse(os.path.exists("session.txt"))
