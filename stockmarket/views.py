from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpRequest
from yahoo_fin.stock_info import *
from django.urls import reverse
from yahooquery import Ticker
from .tasks import update_stock_prices
from concurrent.futures import ThreadPoolExecutor

# Create your views here.


def stockpicker_post(request):
  stock_picker = tickers_nifty50()
  if request.method == 'POST':
    selected_stocks = request.POST.getlist('selected_stocks')
    # print(selected_stocks)
    request.session['selected_stocks'] = selected_stocks
    return redirect('stocktracker')

  #print(stock_picker)
  return render(request,'stock/stockpicker.html',{'stock_picker':stock_picker})


def stocktracker_post(request: HttpRequest):
  selected_stocks = request.session.get('selected_stocks', []) or []

  stock_data = []
  
  if selected_stocks:
    with ThreadPoolExecutor(max_workers=5) as executor:
      results = list(executor.map(fetch_data,selected_stocks))
      
    stock_data = [data for data in results if data]
    print(stock_data)

  return render(request, 'stock/stocktracker.html', {'stock_data': stock_data, 'room_name': 'track'})



def fetch_data(stock_symbol):
    try:
        stock = Ticker(stock_symbol)  # ✅ Initialize the ticker object
        price_data = stock.price.get(stock_symbol, {})  # ✅ Fetch price data using the symbol
        summary_data = stock.summary_detail.get(stock_symbol, {})

        return {
            'name': price_data.get('shortName', stock_symbol),  # ✅ Get the stock name correctly
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
        return None  # Return None if there's an error

