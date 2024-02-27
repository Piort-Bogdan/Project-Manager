import pytest
from django.contrib.auth.models import User


class TestUserAPI:

    @pytest.mark.django_db
    def test_create_user(self, api_client):
        """ Test create user """
        response = api_client.post('/auth/register/',
                                   {'username': 'test_user', 'email': 'test_user@mail.ru', 'password': 'test_password'})
        print('RESPONSE_USER', response.data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_logout_user(self, api_client, get_token):
        """ Test logout user """
        response = api_client.post('/auth/logout/', {'refresh_token': get_token['refresh']},
                                   HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')

        print('LOGOUT', User.objects.all().values('id'))
        assert response.status_code == 204
        assert response.data == {'refresh_token': get_token['refresh']}
