import pytest

from django.core.management import call_command
from django.contrib.auth import get_user_model
from admin_backend import settings

# @pytest.fixture(scope='session')
# def set_test_db():
#     settings.DATABASES['default'] = {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': settings.BASE_DIR / 'db.sqlite3',
#         }
    

User = get_user_model()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='adminpassword', email='admin@admin.com')
        call_command('loaddata', 'data/role.json')
        call_command('loaddata', 'data/permission.json')
        call_command('loaddata', 'data/role_permission.json')
        call_command('loaddata', 'data/user_roles_role.json')