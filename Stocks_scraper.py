import pandas as pd
import yfinance as yf
from datetime import datetime
import time
import logging
from pathlib import Path

class StockScraper:
    def __init__(self, symbols=None):
        """
        Initialize the stock scraper with a list of stock symbols.
        If no symbols provided, uses default tech stocks.
        """
        self.symbols = symbols or ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
        
        # Create necessary directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / 'data'
        self.logs_dir = self.base_dir / 'logs'
        
        # Create directories if they don't exist
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
        """
        Get current stock data for a single symbol using yfinance.
        """
        try:
            # Add delay to avoid rate limiting
            time.sleep(0.5)
            
            # Get stock info
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Extract relevant data with error checking
            data = {
                'symbol': symbol,
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                'market_cap': info.get('marketCap', 'N/A'),
                'volume': info.get('volume', info.get('regularMarketVolume', 'N/A')),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Validate data
            if data['current_price'] == 'N/A':
                raise ValueError(f"Could not fetch price for {symbol}")
                
            # Format market cap to billions
            if isinstance(data['market_cap'], (int, float)):
                data['market_cap'] = f"${data['market_cap'] / 1_000_000_000:.2f}B"
                
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def scrape_all_stocks(self):
        """
        Scrape data for all configured stock symbols and save to CSV.
        """
        self.logger.info("Starting stock data collection...")
        stock_data = []
        
        for symbol in self.symbols:
            self.logger.info(f"Fetching data for {symbol}")
            data = self.get_stock_data(symbol)
            if data:
                stock_data.append(data)
        
        # Convert to DataFrame and save
        if stock_data:
            df = pd.DataFrame(stock_data)
            output_file = self.data_dir / 'stocks.csv'
            df.to_csv(output_file, index=False)
            self.logger.info(f"Successfully saved data for {len(stock_data)} stocks to {output_file}")
            return df
        else:
            self.logger.error("No stock data collected")
            return None
        
    

if __name__ == "__main__":
    # Example usage
    scraper = StockScraper([
    # Global Tech Giants
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NFLX',  
    'NVDA', 'AMD', 'INTC', 'IBM', 'ORCL', 'CSCO', 'ADBE',  
  
]
)
    data = scraper.scrape_all_stocks()
    if data is not None:
        print("\nCollected Stock Data:")
        print(data)