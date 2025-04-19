# stockmarket/tasks.py
from celery import shared_task
from stockmarket.models import StockDetails
from yahooquery import Ticker
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User

@shared_task
def update_stock_prices():
    user_ids = StockDetails.objects.values_list('user', flat=True).distinct()
    
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        selected_stocks = StockDetails.objects.filter(user=user).values_list('stock', flat=True)

        result = {}
        for stock in selected_stocks:
            try:
                t = Ticker(stock)
                price_data = t.price.get(stock, {})
                summary_data = t.summary_detail.get(stock, {})

                result[stock] = {
                    'name': price_data.get('shortName', stock),
                    'price': price_data.get('regularMarketPrice', 'N/A'),
                    'previous_close': price_data.get('regularMarketPreviousClose', 'N/A'),
                    'open': price_data.get('regularMarketOpen', 'N/A'),
                    'day_high': price_data.get('regularMarketDayHigh', 'N/A'),
                    'day_low': price_data.get('regularMarketDayLow', 'N/A'),
                    'market_cap': summary_data.get('marketCap', 'N/A'),
                    'volume': price_data.get('regularMarketVolume', 'N/A'),
                }
            except Exception as e:
                print(f"Error fetching stock {stock}: {e}")
        
        if result:
            group_name = f"stock_{user.id}"
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type":"stock_update",
                    "message":result 
                }
            )
