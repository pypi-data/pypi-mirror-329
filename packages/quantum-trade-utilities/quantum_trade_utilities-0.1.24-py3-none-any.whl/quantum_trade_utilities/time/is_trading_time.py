from datetime import datetime, time
import pytz

def is_trading_time():
    # Get current time in Eastern Time
    et_timezone = pytz.timezone('US/Eastern')
    now = datetime.now(et_timezone)
    
    # Define market hours (9:30 AM to 4:00 PM Eastern)
    market_start = time(9, 30)
    market_end = time(16, 0)
    
    # Check if it's a weekday (Monday = 0, Sunday = 6)
    is_weekday = now.weekday() < 5
    
    # Check if current time is within market hours
    current_time = now.time()
    during_market_hours = market_start <= current_time <= market_end
    
    return is_weekday and during_market_hours