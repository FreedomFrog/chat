from django.apps import AppConfig
from django.contrib import admin
# from .models import ChatRoom, Message

class ChatConfig(AppConfig):
    name = 'chat'

# @admin.register(ChatRoom)
# class ChatRoomAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     pass