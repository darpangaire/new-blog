from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from yahoo_fin.stock_info import tickers_nifty50
from yahooquery import Ticker
from concurrent.futures import ThreadPoolExecutor
from asgiref.sync import sync_to_async
from django.utils.decorators import sync_and_async_middleware
import asyncio

# ---------------------------
# Sync to Async Helper
# ---------------------------

@sync_to_async
def check_authenticated(request):
    return request.user.is_authenticated


# ---------------------------
# Sync View: Stock Picker
# ---------------------------

def stockpicker_post(request):
    stock_picker = tickers_nifty50()
    if request.method == 'POST':
        selected_stocks = request.POST.getlist('selected_stocks')
        request.session['selected_stocks'] = selected_stocks
        return redirect('stocktracker')
    
    return render(request, 'stock/stockpicker.html', {'stock_picker': stock_picker})


# ---------------------------
# Async View: Stock Tracker
# ---------------------------

async def stocktracker_post(request: HttpRequest):
    is_logged_in = await check_authenticated(request)
    if not is_logged_in:
        return HttpResponse("Login first to access the stock tracker.")

    selected_stocks = request.session.get('selected_stocks', []) or []
    stock_data = []

    if selected_stocks:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = await loop.run_in_executor(executor, lambda: list(map(fetch_data, selected_stocks)))
            stock_data = [data for data in results if data]

    room_name = str(request.user.id)  # safer unique room

    return render(request, 'stock/stocktracker.html', {
        'stock_data': stock_data,
        'room_name': room_name,
        'stockpicker': selected_stocks  # pass to JS
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

