from django.db import models
from account.models import Account


class Message(models.Model):
    sender = models.ForeignKey(
        Account, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        Account, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.message}'
