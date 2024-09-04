import pytest
from admin_backend.models import Role
import time

@pytest.mark.django_db
def test_preload_data(django_db_setup):
    assert Role.objects.all().count() >= 1
    assert Role.objects.get(name='ADMIN') is not None
    assert Role.objects.get(name='ADMIN').name == 'ADMIN'
    assert Role.objects.get(name='ADMIN').code== 'ADMIN'