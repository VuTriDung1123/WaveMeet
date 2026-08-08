import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        user = self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous'

        if action:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'signaling_message',
                    'data': data,
                    'sender': user
                }
            )

    # Receive message from room group
    async def signaling_message(self, event):
        data = event['data']
        sender = event['sender']
        action = data.get('action')
        
        # Don't send back to the original sender unless it's a chat message
        # Actually for simplicity, we just send to everyone and client ignores its own messages
        
        await self.send(text_data=json.dumps({
            'action': action,
            'data': data,
            'sender': sender
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        self.user = self.scope['user']
        self.user_group_name = f'user_{self.user.id}'
        self.presence_group_name = 'global_presence'

        # Join personal group (for private invites)
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        # Join global presence group
        await self.channel_layer.group_add(
            self.presence_group_name,
            self.channel_name
        )

        await self.accept()

        # Update DB and broadcast online
        await self.set_online_status(True)
        await self.channel_layer.group_send(
            self.presence_group_name,
            {
                'type': 'presence_update',
                'user_id': self.user.id,
                'status': 'online'
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, 'user'):
            await self.set_online_status(False)
            await self.channel_layer.group_send(
                self.presence_group_name,
                {
                    'type': 'presence_update',
                    'user_id': self.user.id,
                    'status': 'offline'
                }
            )
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
            await self.channel_layer.group_discard(self.presence_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'invite_friend':
            target_id = data.get('target_id')
            room_id = data.get('room_id')
            if target_id and room_id:
                await self.channel_layer.group_send(
                    f'user_{target_id}',
                    {
                        'type': 'room_invite',
                        'sender_name': self.user.username,
                        'room_id': room_id
                    }
                )

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'action': 'presence_update',
            'user_id': event['user_id'],
            'status': event['status']
        }))

    async def room_invite(self, event):
        await self.send(text_data=json.dumps({
            'action': 'room_invite',
            'sender_name': event['sender_name'],
            'room_id': event['room_id']
        }))

    @database_sync_to_async
    def set_online_status(self, is_online):
        self.user.is_online = is_online
        self.user.save(update_fields=['is_online'])
