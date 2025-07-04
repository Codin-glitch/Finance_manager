from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from getpass import getpass
import os

SESSION_FILE = "session.txt"

class Command(BaseCommand):
    help = "Login using username and password"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("== Login =="))

        username = input("Enter Username: ")
        password = getpass("Enter password: ")

        user = authenticate(username=username, password=password)

        if user:
            with open(SESSION_FILE, 'w') as f:
                f.write(username)
            self.stdout.write(self.style.SUCCESS(f"Logged in as '{username}'"))
        else:
            self.stdout.write(self.style.ERROR("Invalid credentials! Please try again."))