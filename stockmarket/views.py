from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpRequest
from yahoo_fin.stock_info import *
from django.urls import reverse
from yahooquery import Ticker

# Create your views here.
def stockpicker_post(request):
  stock_picker = tickers_nifty50()
  if request.method == 'POST':
    selected_stocks = request.POST.getlist('selected_stocks')
    request.session['selected_stocks'] = selected_stocks
    request.session.modified = True
    print(selected_stocks)
    return redirect(reverse('stocktracker'))
    
  #print(stock_picker)
  return render(request,'stock/stockpicker.html',{'stock_picker':stock_picker})

def stocktracker_post(request: HttpRequest):
  try:
      selected_stocks = request.session.get('selected_stocks', [])
  except:
      selected_stocks = []

  stock_data = []
  
  if selected_stocks:
      # Fetch data for all selected stocks in one API call
      stocks = Ticker(selected_stocks)
      price_data = stocks.price
      summary_data = stocks.summary_detail

      for stock in selected_stocks:
          try:
              stock_info = price_data.get(stock, {})
              summary_info = summary_data.get(stock, {})

              stock_details = {
                'name': stock_info.get('shortName', stock),  # Stock name
                'price': stock_info.get('regularMarketPrice', 'N/A'),  # Live price
                'previous_close':stock_info.get('regularMarketPreviousClose','N/A'),
                'open':stock_info.get('regularMarketPreviousClose','N/A'),
                'day_high': stock_info.get('regularMarketDayHigh', 'N/A'),  # Day high
                  'day_low': stock_info.get('regularMarketDayLow', 'N/A'),
                'market_cap': summary_info.get('marketCap', 'N/A'),  # Market cap
                'volume': stock_info.get('regularMarketVolume', 'N/A'),  # Trading volume
              }

              stock_data.append(stock_details)
          except Exception as e:
              print(f"Error fetching data for {stock}: {e}")

  return render(request, 'stock/stocktracker.html', {'stock_data': stock_data})






