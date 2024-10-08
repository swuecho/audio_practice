from django.contrib.auth import get_user_model
import pytest

# Assuming the User model has been created as shown above,
# this example assumes its structure for demonstration purposes.

User = get_user_model()  # Get a reference to the user model (replace with your actual user model).

@pytest.mark.django_db
def test_user_creation():
    """Test if creating a new User instance is successful."""
    
    # Create a new user and save it to the database
    new_user = User.objects.create(email='test@example.com', first_name='Test', last_name='User')
    
    assert new_user is not None  # Assert that an instance of User was created successfully.

@pytest.mark.django_db
def test_user_creation_with_password():
    """Test if creating a new User instance with a password is successful."""
    
    # Create a new user with a password and save it to the database
    new_user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
    
    assert new_user is not None  # Assert that an instance of User was created successfully.
    assert new_user.check_password('testpassword')  # Assert that the password is correct.
    
    # Verify the user exists in the database
    saved_user = User.objects.get(username='testuser')
    assert saved_user is not None
    assert saved_user.email == 'test@example.com'
    
@pytest.mark.django_db
def test_superuser_role():
    """test if the superuser has the superuser role"""
    # Create a superuser for testing if it doesn't exist
    superuser, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_superuser': True,
            'is_staff': True
        }
    )
    if created:
        superuser.set_password('adminpassword')
        superuser.save()

    assert User.objects.all().count() >= 1
    superuser = User.objects.get(username='admin')
    assert superuser is not None
    assert superuser.check_password('adminpassword')
    assert superuser.is_superuser
    assert superuser.is_staff


