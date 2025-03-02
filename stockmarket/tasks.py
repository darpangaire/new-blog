from celery import shared_task
from yahooquery import Ticker
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_stock_prices(selected_stocks=None, *args, **kwargs):
    if not selected_stocks:
        return "No stocks selected"

    stock_data = {}
    missing_stocks = []  # To track stocks that need API calls

    # First, get cached data and identify missing stocks
    for stock in selected_stocks:
        cached_data = cache.get(f"stock_{stock}")
        if cached_data:
            stock_data[stock] = cached_data
        else:
            missing_stocks.append(stock)  # Only fetch if not in cache

    if missing_stocks:
        try:
            stock_info = Ticker(missing_stocks)

            # Log raw responses for debugging
            raw_price_info = stock_info.price
            raw_summary_info = stock_info.summary_detail
            logger.info(f"Raw price info: {raw_price_info}")
            logger.info(f"Raw summary info: {raw_summary_info}")

            for stock in missing_stocks:
                try:
                    price_info = raw_price_info.get(stock, {})
                    summary_info = raw_summary_info.get(stock, {})

                    stock_details = {
                        'name': price_info.get('shortName', stock),
                        'price': price_info.get('regularMarketPrice', 'N/A'),
                        'previous_close': price_info.get('regularMarketPreviousClose', 'N/A'),
                        'open': price_info.get('regularMarketOpen', 'N/A'),
                        'day_high': price_info.get('regularMarketDayHigh', 'N/A'),
                        'day_low': price_info.get('regularMarketDayLow', 'N/A'),
                        'market_cap': summary_info.get('marketCap', 'N/A'),
                        'volume': price_info.get('regularMarketVolume', 'N/A'),
                    }

                    # Store result in cache for 5 minutes (300 seconds)
                    stock_data[stock] = stock_details
                    cache.set(f"stock_{stock}", stock_details, timeout=300)

                except Exception as e:
                    logger.error(f"Error processing stock {stock}: {e}")

        except Exception as e:
            logger.error(f"Error fetching stock data from API: {e}")
            return f"API error: {e}"

    return f"Updated prices for {len(stock_data)} stocks"

