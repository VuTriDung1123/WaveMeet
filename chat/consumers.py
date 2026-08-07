import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
