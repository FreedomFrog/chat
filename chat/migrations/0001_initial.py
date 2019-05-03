# Generated by Django 2.1.5 on 2019-05-03 03:12

import chat.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(validators=[chat.models.validate_message_content])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chatgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.ChatRoom')),
            ],
        ),
    ]
