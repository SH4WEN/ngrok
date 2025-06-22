import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        if user.is_authenticated:
            chat_message = ChatMessage.objects.create(
                user=user,
                message=message
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'timestamp': chat_message.timestamp.isoformat(),
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))