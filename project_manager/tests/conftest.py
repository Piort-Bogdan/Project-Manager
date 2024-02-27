import pytest
from django.contrib.auth.models import User

from rest_framework.test import APIClient


@pytest.fixture(scope='function')
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope='function', autouse=True)
@pytest.mark.django_db
def create_user():
    print('CREATINGUSER')
    print(User.objects.all().values('id'))
    if not User.objects.filter(username='admin').exists():
        User.objects.create_user('admin', 'user@mail.ru,', 'admin')


@pytest.fixture(scope='function')
def get_token(api_client):
    response = api_client.post('/auth/login/', {'username': 'admin', 'password': 'admin'})
    return response.data
