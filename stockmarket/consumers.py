import json

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from asgiref.sync import sync_to_async
import asyncio

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # get the room name which is in routing.py.
        # self.scope is a dictionary Django Channels gives you     
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        # Add the group into that channels
        self.channel_layer.group_add(self.room_group_name,self.channel_name)
        
        #this is for later use.
        query_params = parse_qs(self.scope['query_string'].decode())
        
        await self.accept()
        
     
    @sync_to_async   
    def addToCeleryBeat(self,stockpicker):
        task = PeriodicTask.objects.filter(name="every-10-seconds")
        if task.exists:
            task = task.first()
            try:
                args = json.loads(task.args)
            except json.JSONDecodeError:
                args=[]
                
            if not isinstance(args,list):
                args = [args]
                
                
            if stockpicker not in args:
                args.append(stockpicker)
                task.args = json.dumps(args)
                task.save()
                
        else:
            schedule,_ = IntervalSchedule.objects.get_or_create(every=10,
                                                                period = IntervalSchedule.SECONDS)
            
            PeriodicTask.objects.create(
                interval = schedule,
                name='every-10-seconds',
                task='stockmarket.tasks.update_stock_prices',
                args = json.dumps([stockpicker])
            )
            
            
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)
        
        
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.addToCeleryBeat(message)
        
        await self.channel_layer.group_send(self.room_group_name,{"type":"stock_update","message":message})
        
        
    async def stock_update(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({"message":message}))
        
    
            
        
        
             
