from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import MessageSerializer
from .models import Message


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

    @swagger_auto_schema(
        operation_description='List of messages where current user is the receiver',
        responses={200: MessageSerializer, 400: 'Bad Request'},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a message',
        request_body=MessageSerializer,
        responses={201: MessageSerializer, 400: 'Bad Request'},
        exclude=['state']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
