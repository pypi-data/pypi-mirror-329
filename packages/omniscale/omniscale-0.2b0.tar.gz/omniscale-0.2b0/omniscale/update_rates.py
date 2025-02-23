import time
from omniscale.currency_converter import CurrencyConverter

def auto_update(interval=3600):
    """Update exchange rates every X seconds (default: 1 hour)."""
    converter = CurrencyConverter()
    while True:
        converter.update_rates()
        print(f"🔄 Rates updated. Next update in {interval // 60} minutes.")
        time.sleep(interval)

if __name__ == "__main__":
    auto_update()