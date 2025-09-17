import os

def generate_flask_key(): 
    return os.urandom(24)