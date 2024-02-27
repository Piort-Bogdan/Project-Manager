from rest_framework import status

from messenger.models import Message
from tests.test_setup import TestSetUp


class TestMessageApi(TestSetUp):

    def test_create_message(self):
        """ Test create message """
        data = {
            'text': 'test_message',
            'receivers': [self.user.objects.all().first().id],
            'sender': self.user.objects.all().first().id
        }
        response = self.client.post(self.message_url, data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_list(self):
        """ Test message list """
        message = Message.objects.create(text='test_message', sender=self.user.objects.all().first())
        message.receivers.set(self.user.objects.all())
        response = self.client.get(self.message_url,
                                   HTTP_AUTHORIZATION=f'Bearer {self.token["access"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
