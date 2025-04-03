import json

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # parse querySTring
        query_params = parse_qs(self.scope['query-string'].decode())
        
        await self.accept()
        
    def addToCeleryBeat(self,stockpicker):
        task = PeriodicTask.objects.filter(name='every-10-seconds')
        if len(task)> 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            
        
        
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "Stock_update", "message": message}
        )

    # Receive message from room group
    async def Stock_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
        
        
