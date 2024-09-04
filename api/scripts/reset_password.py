import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../admin_backend.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password(email, new_password):
    try:
        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        print(f"Password reset successfully for user: {email}")
    except User.DoesNotExist:
        print(f"User with email {email} not found")

def run():
    email = input("Enter user email: ")
    new_password = input("Enter new password: ")
    reset_password(email, new_password)
