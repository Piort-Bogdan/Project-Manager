from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        extra_kwargs.update({
            'sender': {'help_text': 'The sender of the message'},
            'receiver': {'help_text': 'The receiver of the message'},
        })
        return extra_kwargs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sender'] = instance.sender.username
        data['receiver'] = instance.receiver.username
        return data
