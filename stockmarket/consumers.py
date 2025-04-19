import json
import copy
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from stockmarket.models import StockDetails
from django.db import transaction

class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        task = PeriodicTask.objects.filter(name="every-10-seconds").first()
        if task:
            try:
                args = json.loads(task.args)
                if isinstance(args, list) and args and isinstance(args[0], list):
                    args = args[0]
                else:
                    args = []
            except Exception as e:
                print("Error loading task args:", e)
                args = []

            for x in stockpicker:
                if x not in args:
                    args.append(x)

            task.args = json.dumps(args)
            task.save()
        else:
            schedule, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                interval=schedule,
                name='every-10-seconds',
                task="stockmarket.tasks.update_stock_prices",
                args=json.dumps(stockpicker)
            )

    @sync_to_async
    def addToStockDetail(self, stockpicker):
        user = self.scope["user"]
        for stock in stockpicker:
            stock_obj, _ = StockDetails.objects.get_or_create(stock=stock)
            stock_obj.user.add(user)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'stock_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        query_params = parse_qs(self.scope["query_string"].decode())
        stockpicker = query_params.get('stockpicker', [])

        # Validate stock names (simple alphanumeric)
        stockpicker = [s.upper() for s in stockpicker if s.isalnum()]

        if stockpicker:
            try:
                await self.addToCeleryBeat(stockpicker)
                await self.addToStockDetail(stockpicker)
            except Exception as e:
                print("Error during connect setup:", e)

        await self.accept()

    @sync_to_async
    def helper_func(self):
        user = self.scope["user"]
        stocks = StockDetails.objects.filter(user__id=user.id)

        with transaction.atomic():
            task = PeriodicTask.objects.filter(name="every-10-seconds").first()
            if not task:
                return

            try:
                args = json.loads(task.args)
                if isinstance(args, list) and args and isinstance(args[0], list):
                    args = args[0]
                else:
                    args = []
            except Exception as e:
                print("Error loading task args during disconnect:", e)
                args = []

            for stock in stocks:
                stock.user.remove(user)
                if stock.user.count() == 0 and stock.stock in args:
                    args.remove(stock.stock)
                    stock.delete()

            if not args:
                task.delete()
            else:
                task.args = json.dumps([args])
                task.save()

    async def disconnect(self, close_code):
        await self.helper_func()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', {})

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stock_update',  # Fixed event name
                'message': message
            }
        )

    @sync_to_async
    def selectUserStocks(self):
        user = self.scope["user"]
        return list(user.stockdetail_set.values_list('stock', flat=True))

    async def stock_update(self, event):
        message = copy.deepcopy(event['message'])
        user_stocks = await self.selectUserStocks()

        filtered_message = {k: v for k, v in message.items() if k in user_stocks}

        await self.send(text_data=json.dumps(filtered_message))

