import pandas as pd
import requests
from datetime import datetime
import time
import logging
from pathlib import Path
import random

class StockScraper:
    def __init__(self, symbols=None):
        """
        Initialize the stock scraper with Alpha Vantage API.
        """
        self.symbols = symbols or ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
        self.api_key = "Alpha Vantage api key"  # Your Alpha Vantage API key
        self.base_url = "https://www.alphavantage.co/query"
        
        # Create necessary directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / 'data'
        self.logs_dir = self.base_dir / 'logs'
        
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for the scraper"""
        log_file = self.logs_dir / 'stock_scraper.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_stock_data(self, symbol):
        """Get stock data from Alpha Vantage with retries."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Alpha Vantage rate limit: 5 requests/minute (free tier)
                time.sleep(15)  # 15s delay between requests (safe for free tier)
                
                # First get quote data
                quote_params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.api_key
                }
                quote_response = requests.get(self.base_url, params=quote_params).json()
                
                # Then get overview data (for sector, etc.)
                overview_params = {
                    "function": "OVERVIEW",
                    "symbol": symbol,
                    "apikey": self.api_key
                }
                overview_response = requests.get(self.base_url, params=overview_params).json()
                
                # Parse data
                quote_data = quote_response.get("Global Quote", {})
                overview_data = overview_response
                
                data = {
                    'symbol': symbol,
                    'current_price': quote_data.get("05. price", "N/A"),
                    'market_cap': overview_data.get("MarketCapitalization", "N/A"),
                    'volume': quote_data.get("06. volume", "N/A"),
                    'pe_ratio': overview_data.get("PERatio", "N/A"),
                    'company_name': overview_data.get("Name", "N/A"),
                    'sector': overview_data.get("Sector", "N/A"),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Format market cap to billions if numeric
                if data['market_cap'].replace('.', '').isdigit():
                    data['market_cap'] = f"${float(data['market_cap']) / 1_000_000_000:.2f}B"
                
                return data
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 30  # Exponential backoff
                    self.logger.warning(f"Retrying {symbol} in {wait_time}s... (Attempt {attempt + 1})")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
                    return None

    def scrape_all_stocks(self):
        """Scrape data for all symbols using Alpha Vantage."""
        self.logger.info("Starting stock data collection with Alpha Vantage...")
        stock_data = []
        
        for i, symbol in enumerate(self.symbols):
            if i > 0:
                time.sleep(15)  # Maintain 15s delay between requests
            
            data = self.get_stock_data(symbol)
            if data:
                stock_data.append(data)
            else:
                self.logger.warning(f"Skipping {symbol} due to data retrieval error.")
        
        if stock_data:
            df = pd.DataFrame(stock_data)
            output_file = self.data_dir / 'stocks.csv'
            df.to_csv(output_file, index=False)
            self.logger.info(f"Successfully saved data for {len(stock_data)} stocks")
            return df
        else:
            self.logger.error("No stock data collected")
            return None

if __name__ == "__main__":
    # Process in smaller batches (Alpha Vantage free tier allows 5 requests/minute)
    all_symbols = [
        'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NFLX',
        'NVDA', 'AMD', 'INTC', 'IBM', 'ORCL', 'CSCO', 'ADBE'
    ]
    
    # Process in batches of 5 with 1-minute delays
    batch_size = 5
    all_data = []
    
    for i in range(0, len(all_symbols), batch_size):
        batch = all_symbols[i:i + batch_size]
        scraper = StockScraper(batch)
        data = scraper.scrape_all_stocks()
        if data is not None:
            all_data.append(data)
        
        # Wait 60 seconds between batches to stay under rate limits
        if i + batch_size < len(all_symbols):
            print(f"\nWaiting 60 seconds before next batch...")
            time.sleep(60)
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        output_file = Path('data') / 'stocks.csv'
        final_df.to_csv(output_file, index=False)
        print("\nFinal collected data:")
        print(final_df)
    else:
        print("\nNo data collected")
