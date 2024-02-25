from django.db import models


class Message(models.Model):
    """ Model for creating messages"""
    MESSAGE_STATE = (
        (1, 'Unread'),
        (2, 'Read'),
        (3, 'Deleted'),
    )

    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='senders', verbose_name='Sender')
    receiver = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='receivers',
                                  verbose_name='Receivers')
    text = models.TextField(verbose_name="Message text")
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.SmallIntegerField(default=1, choices=MESSAGE_STATE, verbose_name="Message state")

    def __str__(self):
        return f'{self.sender.username}, {self.receiver.username}'
