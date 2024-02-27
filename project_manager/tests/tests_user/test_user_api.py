from rest_framework import status

from tests.test_setup import TestSetUp


class TestUserAPI(TestSetUp):

    def test_create_user(self):
        """ Test create user """
        data = {
            'username': 'test_user',
            'email': 'test@test.com',
            'password': 'password'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout_user(self):
        """ Test logout user """
        response = self.client.post(self.logout_url, {'refresh_token': self.token['refresh']},
                                    HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
