from channels.generic.websocket import AsyncWebsocketConsumer
import json
from . import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_name = f"chat-id_{self.chat_id}"
        print(f"Получен chat_id={self.chat_id}")

        # присединиться к группе
        await self.channel_layer.group_add(self.chat_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # покинуть группу
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'message':
            # если это сообщение, засылаем его в тот чат, канал которого открыт по ссылке
            await self.channel_layer.group_send(
                self.chat_name, {"type": "chat.message", "message": data}
            )
        elif data['type'] == 'chat':
            # а если это чат, рассылаем его по всем группам, где зарегистрированы пользователи, входящие в этот чат
            # сначала отправить в группу открытого чата
            await self.channel_layer.group_send(
                self.chat_name, {"type": "chat.message", "message": data}
            )
            # другие пользователи могут находиться в разных чатах, поэтому рассылка в группы
            # всех чатов, в которых зарегистрированы пользователи этого
            async for chat in models.Chat.objects.filter(members__in=data['parcel']['members']).values('id').distinct():
                chatName = f"chat-id_{chat['id']}"
                await self.channel_layer.group_send(
                    chatName, {"type": "chat.message", "message": data}
                )

    # метод отправки события в группу. соответствует вызываемому методу, указанному в свойстве "type"? с заменой "." на "_" в наименовании
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))