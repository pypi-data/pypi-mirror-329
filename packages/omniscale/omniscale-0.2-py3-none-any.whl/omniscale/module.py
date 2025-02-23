class Converter:
    """Base Converter Class"""
    
    def validate_input(self, value):
        """Ensure the input is a valid number."""
        if not isinstance(value, (int, float)):
            raise ValueError("Input must be a number.")
        return value


class TemperatureConverter(Converter):
    """Handles temperature conversions."""

    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit."""
        celsius = self.validate_input(celsius)
        return round((celsius * 9 / 5) + 32, 2)

    def fahrenheit_to_celsius(self, fahrenheit):
        """Convert Fahrenheit to Celsius."""
        fahrenheit = self.validate_input(fahrenheit)
        return round((fahrenheit - 32) * 5 / 9, 2)


class DistanceConverter(Converter):
    """Handles distance conversions."""

    def meters_to_feet(self, meters):
        """Convert meters to feet."""
        meters = self.validate_input(meters)
        return round(meters * 3.28084, 2)

    def feet_to_meters(self, feet):
        """Convert feet to meters."""
        feet = self.validate_input(feet)
        return round(feet / 3.28084, 2)


class WeightConverter(Converter):
    """Handles weight conversions."""

    def kg_to_pounds(self, kg):
        """Convert kilograms to pounds."""
        kg = self.validate_input(kg)
        return round(kg * 2.20462, 2)

    def pounds_to_kg(self, pounds):
        """Convert pounds to kilograms."""
        pounds = self.validate_input(pounds)
        return round(pounds / 2.20462, 2)


class SpeedConverter(Converter):
    """Handles speed conversions."""

    def kmh_to_mph(self, kmh):
        """Convert kilometers per hour to miles per hour."""
        kmh = self.validate_input(kmh)
        return round(kmh * 0.621371, 2)

    def mph_to_kmh(self, mph):
        """Convert miles per hour to kilometers per hour."""
        mph = self.validate_input(mph)
        return round(mph / 0.621371, 2)


class TimeConverter(Converter):
    """Handles time conversions."""

    def minutes_to_seconds(self, minutes):
        """Convert minutes to seconds."""
        minutes = self.validate_input(minutes)
        return minutes * 60

    def seconds_to_minutes(self, seconds):
        """Convert seconds to minutes."""
        seconds = self.validate_input(seconds)
        return round(seconds / 60, 2)


class BatchConverter:
    """Handles batch conversions for multiple values."""
    
    @staticmethod
    def batch_convert(converter, func_name, values):
        """
        Apply a conversion function to a list or tuple of values.
        
        Example:
            BatchConverter.batch_convert(TemperatureConverter(), "celsius_to_fahrenheit", [0, 100, 37])
        """
        if not hasattr(converter, func_name):
            raise ValueError(f"Invalid function: {func_name}")
        
        func = getattr(converter, func_name)
        if isinstance(values, (list, tuple)):
            return [func(value) for value in values]
        else:
            return func(values)


# Example Usage
if __name__ == "__main__":
    temp = TemperatureConverter()
    print(temp.celsius_to_fahrenheit(100))  # Output: 212.0

    dist = DistanceConverter()
    print(dist.meters_to_feet(1))  # Output: 3.28

    weight = WeightConverter()
    print(weight.kg_to_pounds(10))  # Output: 22.05

    speed = SpeedConverter()
    print(speed.kmh_to_mph(100))  # Output: 62.14

    time = TimeConverter()
    print(time.minutes_to_seconds(5))  # Output: 300

    # Batch Conversion Example
    print(BatchConverter.batch_convert(temp, "celsius_to_fahrenheit", [0, 100, 37]))  # Output: [32.0, 212.0, 98.6]