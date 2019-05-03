from django.db import models
from django.core.exceptions import ValidationError
import uuid

def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty/invalid',
            code='invalid',
            params={'content': content},
        )

class ChatRoom(models.Model):
    id = models.TextField(primary_key=True, unique=True)

    def last_50_messages(self):
        return Message.objects.filter(chatgroup=self.id).order_by('-created_at').all()[:50]


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        null=False,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    chatgroup = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

