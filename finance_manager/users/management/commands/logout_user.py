from django.core.management.base import BaseCommand
import os

SESSION_FILE = "session.txt"

class Command(BaseCommand):
    help = "Logout the currently logged-in user"

    def handle(self, *args, **kwargs):
        
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            self.stdout.write(self.style.SUCCESS("Successfully logged out!"))
        else:
            self.stdout.write(self.style.ERROR("No user is currently logged in."))
