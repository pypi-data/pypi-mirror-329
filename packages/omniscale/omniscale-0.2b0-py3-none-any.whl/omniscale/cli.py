import argparse
from omniscale.currency_converter import CurrencyConverter

def main():
    parser = argparse.ArgumentParser(description="Unit Conversion & Currency Exchange Tool")
    parser.add_argument("value", type=float, help="Value to convert")
    parser.add_argument("base_currency", type=str, help="Base currency (e.g., USD, EUR)")
    parser.add_argument("target_currency", type=str, help="Target currency (e.g., GBP, JPY)")

    args = parser.parse_args()

    converter = CurrencyConverter(args.base_currency.upper())
    converter.update_rates()
    converter.convert(args.value, args.target_currency.upper())

if __name__ == "__main__":
    main()