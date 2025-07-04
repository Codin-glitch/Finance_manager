import os

def get_logged_in_user():
    if os.path.exists("session.txt"):
        with open('session.txt','r') as f:
            return f.read().strip()
    return None