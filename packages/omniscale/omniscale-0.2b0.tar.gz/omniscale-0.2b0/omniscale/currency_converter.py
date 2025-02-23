import requests
import json
import os

class CurrencyConverter:
    """Handles real-time currency conversion with offline support."""

    API_URL = "https://open.er-api.com/v6/latest/"
    CACHE_FILE = "currency_cache.json"

    def __init__(self, base_currency="USD"):
        self.base_currency = base_currency
        self.rates = self.load_rates()

    def fetch_rates(self):
        """Fetch latest exchange rates from API."""
        try:
            response = requests.get(f"{self.API_URL}{self.base_currency}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("rates", {})
        except (requests.exceptions.RequestException, KeyError):
            print("⚠️ No internet. Using last known exchange rates.")
            return self.load_rates()

    def load_rates(self):
        """Load exchange rates from cache file."""
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_rates(self, rates):
        """Save exchange rates to cache file."""
        with open(self.CACHE_FILE, "w") as file:
            json.dump(rates, file, indent=4)

    def convert(self, amount, target_currency):
        """Convert from base currency to target currency."""
        if target_currency not in self.rates:
            raise ValueError(f"Invalid currency: {target_currency}")

        result = round(amount * self.rates[target_currency], 2)
        print(f"💱 {amount} {self.base_currency} = {result} {target_currency}")
        return result

    def update_rates(self):
        """Update rates and save to cache."""
        new_rates = self.fetch_rates()
        if new_rates:
            self.rates = new_rates
            self.save_rates(new_rates)
            print("✅ Exchange rates updated.")

# Example Usage
if __name__ == "__main__":
    converter = CurrencyConverter("EUR")  # Default: USD, you can change
    converter.update_rates()
    converter.convert(100, "USD")
    converter.convert(50, "GBP")