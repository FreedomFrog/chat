from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from .models import Message, ChatRoom


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message':message
#         }))

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return str(obj)
        return super().default(obj)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(ChatRoom.objects.get_or_create(
            id=self.room_group_name))

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def get_messages(self, groupname):
        return ChatRoom.objects.get(id=groupname).last_50_messages()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        data = text_data_json['data']
        command = text_data_json['command']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'data': data,
            }
        )

        if command == 'fetch_messages':
            group = ChatRoom.objects.get(id=self.room_group_name)
            # print(group)
            # messages = serialize('json', group.last_50_messages(), cls=LazyEncoder)
            list_messages = group.last_50_messages()
            messages = [message.content for message in list_messages]
            # result = []
            # for message in messages:
            #     result.append(message)

            # print(f'messages: {messages}')
            # print(result)

            # json_message = json.dumps(result)

            # await self.send(text_data=json_message)
            # testing
            await self.send(text_data=json.dumps({
                "type": "chat_message",
                'message': 'chat_fetch',
                'user': user,
                # 'data': serialize('json', messages, fields=('content',))
                'data': json.dumps(messages)
            }))
        else:
            group = ChatRoom.objects.get(id=self.room_group_name)
            async_to_sync(Message.objects.create(chatgroup=group, content=text_data_json))


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        data = event['data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'data': data,
        }))

    # async def send_message(self, message):
    #     print(message)
    #     await self.send(text_data=message)
    #
    # async def messages_to_json(self, messages):
    #     return {
    #         'data': message['data'],
    #         'message': message['message'],
    #         'user': message['user']
    #     }