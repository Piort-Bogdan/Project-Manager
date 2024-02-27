import pytest
from django.contrib.auth.models import User


class TestMessageApi:

    @pytest.mark.django_db
    def test_create_message(self, api_client, get_token):
        """ Test create message """
        response = api_client.post('/api/messages/',
                                   {'text': 'test_message', 'receivers': [1, 2], 'sender': 1},
                                   HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        a = User.objects.all().values('id')
        print('AA_AA', a)
        print('RESPONSE___', response.data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_message_list(self, api_client, get_token):
        """ Test message list """
        response = api_client.get('/api/messages/',
                                  HTTP_AUTHORIZATION=f'Bearer {get_token["access"]}')
        print('USER', User.objects.all().values('id'))
        print('RESPONSE__|', response.status_code)
        print('RESPONSE__|', response.data)
        assert response.status_code == 200
        assert len(response.data) == 1
