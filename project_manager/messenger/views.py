from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .serializers import MessageSerializer
from .models import Message


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sender', 'state']
    search_fields = ['sender', 'state', 'text']

    def get_queryset(self):
        return Message.objects.filter(receivers=self.request.user)

    @extend_schema(
        description='List all messages for the authenticated user (user is the receiver of the message)',
        responses={200: MessageSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        description='Create a new message',
        request=MessageSerializer,
        responses={201: MessageSerializer},
        examples=[
            OpenApiExample('Example 1', summary='Create a message', value={
                'sender': 1, 'receivers': [1, 2], 'text': 'test_message'}),
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
