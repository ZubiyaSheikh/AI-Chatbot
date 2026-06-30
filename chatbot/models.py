

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):

    # User who owns this chat
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Chat title
    title = models.CharField(
        max_length=200
    )

    # Date and time when chat is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Display chat title in Django Admin
    def __str__(self):
        return self.title
    
    #sender choices
    SENDER_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

class Message(models.Model):
        # Chat to which this message belongs
        chat = models.ForeignKey(
            Chat,
            on_delete=models.CASCADE,
            related_name='messages'
        )

        # Sender of the message (user or assistance)
        sender = models.CharField(
            max_length=20,
            choices=Chat.SENDER_CHOICES
        )

        # Content of the message
        content = models.TextField()

        # Date and time when message is created
        created_at = models.DateTimeField(
            auto_now_add=True
        )

        # Display message content in Django Admin
        def __str__(self):
            return f"{self.sender}: {self.content[:50]}..."