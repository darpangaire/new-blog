from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from yahoo_fin.stock_info import tickers_nifty50
from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
from asgiref.sync import sync_to_async
from django.utils.decorators import sync_and_async_middleware
import asyncio
from stockmarket.models import StockDetails
# ---------------------------
# Sync to Async Helper
# ---------------------------
def check_authenticated(request):
    if request.user.is_authenticated:
        return True
    
    else:
        return False

# ---------------------------
# Sync View: Stock Picker
# ---------------------------

def stockpicker_post(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    stock_picker = tickers_nifty50()
    if request.method == 'POST':
        selected_stocks = request.POST.getlist('selected_stocks')
        request.session['selected_stocks'] = selected_stocks
        StockDetails.objects.filter(user=request.user).delete()  # clear old
        for stock in selected_stocks:
            StockDetails.objects.create(user=request.user, stock=stock)

        return redirect('stocktracker')
    
    
    return render(request, 'stock/stockpicker.html', {'stock_picker': stock_picker})


# ---------------------------
# Async View: Stock Tracker
# ---------------------------

from asgiref.sync import sync_to_async

async def stocktracker_post(request: HttpRequest):
    get_selected_stocks = sync_to_async(lambda: request.session.get('selected_stocks', []) or [])
    selected_stocks = await get_selected_stocks()

    # Wrap access to request.user.id
    get_user_id = sync_to_async(lambda: str(request.user.id))
    room_name = await get_user_id()

    stock_data = []

    if selected_stocks:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = await loop.run_in_executor(executor, lambda: list(map(fetch_data, selected_stocks)))
            stock_data = [data for data in results if data]

    return render(request, 'stock/stocktracker.html', {
        'stock_data': stock_data,
        'room_name': room_name,
        'stockpicker': selected_stocks
    })



# ---------------------------
# Stock Fetch Helper (Sync)
# ---------------------------

def fetch_data(stock_symbol):
    try:
        stock = Ticker(stock_symbol)
        price_data = stock.price.get(stock_symbol, {})
        summary_data = stock.summary_detail.get(stock_symbol, {})

        return {
            'name': price_data.get('shortName', stock_symbol),
            'price': price_data.get('regularMarketPrice', 'N/A'),
            'previous_close': price_data.get('regularMarketPreviousClose', 'N/A'),
            'open': price_data.get('regularMarketOpen', 'N/A'),
            'day_high': price_data.get('regularMarketDayHigh', 'N/A'),
            'day_low': price_data.get('regularMarketDayLow', 'N/A'),
            'market_cap': summary_data.get('marketCap', 'N/A'),
            'volume': price_data.get('regularMarketVolume', 'N/A'),
        }

    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None

