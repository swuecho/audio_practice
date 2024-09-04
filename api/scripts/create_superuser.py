import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../admin_backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(username, email, password):
    try:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser created successfully: {username}")
    except Exception as e:
        print(f"Error creating superuser: {str(e)}")

def run():
    username = "admin"
    email = "admin@example.com"
    password = "adminpassword"
    create_superuser(username, email, password)