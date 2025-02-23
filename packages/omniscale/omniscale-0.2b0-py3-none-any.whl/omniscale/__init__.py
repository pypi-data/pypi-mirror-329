# Import classes
from .module import TemperatureConverter
from .module import DistanceConverter
from .module import WeightConverter
from .module import SpeedConverter
from .module import TimeConverter
from .currency_converter import CurrencyConverter
from .module import BatchConverter

__all__ = [
    # Function-based conversions
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "meters_to_feet",
    "feet_to_meters",
    "kg_to_pounds",
    "pounds_to_kg",
    "kmh_to_mph",
    "mph_to_kmh",
    "minutes_to_seconds",
    "seconds_to_minutes",

    # Class-based conversions
    "TemperatureConverter",
    "DistanceConverter",
    "WeightConverter",
    "SpeedConverter",
    "TimeConverter",
    "CurrencyConverter",
    "BatchConverter"
]