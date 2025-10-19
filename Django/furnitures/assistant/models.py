from django.db import models
from django.utils import timezone


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id}"

    class Meta:
        ordering = ['-created_at']


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(
        max_length=10,
        choices=[("user", "User"), ("bot", "Bot")],
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.session.session_id}] {self.sender}: {self.message[:50]}"

    class Meta:
        ordering = ['timestamp']
