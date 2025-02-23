'''
    Types are the data types that can be used to generate fake data.
'''
import random
from typing import Any, List
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_US")

def handle_probability(value, fallback, probability):
    """
    Handles probability logic for all types.

    @param value: The value to potentially return
    @param fallback: The fallback value (usually None)
    @param probability: The probability (0-100) of returning the value
    @return: Either the value or the fallback based on probability
    """
    if probability == 100:
        return value

    sample = random.random() * 100  # Convert to percentage
    return value if sample < probability else fallback

class Null:
    '''
        @param name: The name of the column
        @param value: The possible fallback value if the column is not null. Can be another faked data type
        @param probability: The probability of the column being null
    '''
    def __init__(self, name, value=None, probability=100):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Null()"

class Int:
    '''
        @param name: The name of the column
        @param value: The int value to be used. If not provided, a random int will be generated.
    '''
    def __init__(self, name, value=random.randint(1, 99999999), probability=100):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Int()"

class Number:
    '''
        @param name: The name of the column
        @param value: The float or int value to be used. If not provided, a random int will be generated.
    '''
    def __init__(self, name, value=random.randint(1, 99999999), probability=100):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Number()"

class Bool:
    '''
        @param name: The name of the column
        @param value: The bool value to be used. If not provided, a random bool will be generated.
    '''
    def __init__(self, name, value=random.choice([True, False]), probability=100):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Bool()"

class Text:
    '''
        @param name: The name of the column
        @param value: The str value to be used. If not provided, an empty str will be generated.
        @param probability: The probability of the text being empty. Defaults to 100
    '''
    def __init__(self, name, value=fake.sentence(nb_words=10), probability=100):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = str(self.value()[0])
        else:
            value = str(self.value)
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Text()"

class Date:
    """
    Generates date values between specified start and end dates.

    Accepts dates in multiple formats:
    - ISO format: "2024-03-14"
    - "today", "now" keywords
    - datetime objects
    - Relative times: "+1d", "-2d", etc.
    - No arguments: defaults to between 1970-01-01 and now

    @param name: The name of the column
    @param start_date: The start date (inclusive). Defaults to "1970-01-01"
    @param end_date: The end date (inclusive). Defaults to "now"
    @param probability: The probability of the date being null
    """
    def __init__(self, name, start_date=None, end_date=None, probability=100):
        self.name = name
        self.probability = probability

        # Set default values if None
        start_date = start_date or "1970-01-01"
        end_date = end_date or "now"

        # Parse dates
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)

        # Validate date range
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")

    def _parse_date(self, date_value):
        """Parse various date input formats"""
        if date_value is None:
            return datetime.now().date()

        if isinstance(date_value, datetime):
            return date_value.date()

        if isinstance(date_value, str):
            # Handle keywords
            if date_value.lower() in ['today', 'now']:
                return datetime.now().date()

            # Handle relative times
            if date_value.startswith(('+', '-')):
                return self._parse_relative_time(date_value).date()

            # Try parsing different formats
            try:
                # Try ISO format first
                return datetime.fromisoformat(date_value).date()
            except ValueError:
                pass

            try:
                # Try date-only format
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            except ValueError as e:
                raise ValueError(f"Unsupported date format: {date_value}") from e

        raise ValueError(f"Unsupported date type: {type(date_value)}")

    def _parse_relative_time(self, relative_time):
        """Parse relative time strings like +1d, -2d"""
        if not relative_time[1:].isalnum():
            raise ValueError(f"Invalid relative time format: {relative_time}")

        # Get the number and unit
        number = int(relative_time[:-1])
        unit = relative_time[-1].lower()

        if unit != 'd':
            raise ValueError("Only days ('d') are supported for relative dates")

        # Get current date as base
        base_time = datetime.now()
        delta = timedelta(days=number)

        return base_time + delta if relative_time.startswith('+') else base_time - delta

    def __call__(self, *args, **kwargs):
        result = fake.date_between(
            start_date=self.start_date,
            end_date=self.end_date
        )
        return (handle_probability(result.strftime('%Y-%m-%d'), None, self.probability), self.name)

    def __repr__(self):
        return f"Date(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', probability={self.probability})"

class Currency:
    '''
        @param name: The name of the column
        @param symbol: The symbol of the currency. Defaults to $
        @param min_value: The minimum value of the currency. Defaults to 0
        @param max_value: The maximum value of the currency. Defaults to 1000
        @param probability: The probability of the currency being null. Defaults to 100
    '''
    def __init__(self, name, symbol="$", min_value=0, max_value=1000, probability=100):
        self.name = name
        self.symbol = symbol
        self.min_value = min_value
        self.max_value = max_value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        value = f"{self.symbol}{random.randint(self.min_value, self.max_value):.2f}"
        return (handle_probability(value, None, self.probability), self.name)

    def __str__(self):
        return f'Currency(name={self.name}, symbol={self.symbol}, min_value={self.min_value}, max_value={self.max_value}, probability={self.probability})'

    def __repr__(self):
        return "Currency()"

class Enum:
    '''
        @param name: The name of the column
        @param choices: The list of choices to be used. If not provided, an empty list will be generated.
        @param probability: The probability of the enum being null. Defaults to 100
    '''
    def __init__(self, name, choices: List[Any], probability=100):
        if not choices:
            raise ValueError("Enum must have at least one choice.")
        self.name = name
        self.choices = choices
        self.probability = probability

    def __call__(self, *args, **kwargs):
        choices = [(choice() if callable(choice) else choice) for choice in self.choices]
        return (handle_probability(random.choice(choices), None, self.probability), self.name)

    def __str__(self):
        return f'Enum(name={self.name}, choices={self.choices}, probability={self.probability})'

    def __repr__(self):
        return "Enum()"

class ID:
    '''
        @param name: The name of the column
        @param prefix: The prefix of the id. Defaults to an empty str
        @param probability: The probability of the id being null. Defaults to 100
    '''
    def __init__(self, name, prefix="", probability=100):
        self.name = name
        self.prefix = prefix
        self.probability = probability

    def __call__(self, *args, **kwargs):
        uuid = fake.uuid4()
        if len(self.prefix) > len(uuid):
            raise ValueError('Prefix cannot be longer than the id')
        id_value = self.prefix + uuid[len(self.prefix):]
        return (handle_probability(id_value, None, self.probability), self.name)

    def __str__(self):
        return f'ID(name={self.name}, prefix={self.prefix}, probability={self.probability})'

    def __repr__(self):
        return "ID()"

class Name:
    '''
        @param name: The name of the column
        @param probability: The probability of the name being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.name(), None, self.probability), self.name)

    def __str__(self):
        return f'Name(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "Name()"

class Address:
    '''
        @param name: The name of the column
        @param probability: The probability of the address being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.address(), None, self.probability), self.name)

    def __str__(self):
        return f'Address(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "Address()"

class Email:
    '''
        @param name: The name of the column
        @param email_type: The type of the email. Defaults to random
        @param domain: The domain of the email. Defaults to None
        @param probability: The probability of the email being null. Defaults to 100
    '''
    def __init__(self, name, email_type="random", domain=None, probability=100):
        self.name = name
        self.email_type = email_type.lower()
        self.domain = domain
        self.probability = probability
        if self.email_type not in ("random", "safe", "free", "company", "specific"):
            raise ValueError("Invalid email type. Must be one of: random, safe, free, company, specific")
        if self.email_type == "specific" and self.domain is None:
            raise ValueError("Domain must be specified when email_type is 'specific'")

    def __call__(self, *args, **kwargs):
        if self.email_type == "random":
            email = fake.email()
        elif self.email_type == "safe":
            email = fake.safe_email()
        elif self.email_type == "free":
            email = fake.free_email()
        elif self.email_type == "company":
            email = fake.company_email()
        else:  # specific
            email = fake.email(domain=self.domain)
        return (handle_probability(email, None, self.probability), self.name)

    def __str__(self):
        return f'Email(name={self.name}, email_type={self.email_type}, domain={self.domain}, probability={self.probability})'

    def __repr__(self):
        return "Email()"

class Phone:
    '''
        @param name: The name of the column
        @param probability: The probability of the phone being null. Defaults to 100
        @param locale: The locale of the phone. Defaults to None
    '''
    def __init__(self, name, probability=100, locale=None):
        self.name = name
        self.probability = probability
        self.locale = locale
        if self.locale:
            try:
                Faker(self.locale)
            except AttributeError as e:
                raise ValueError(f"Invalid locale: {self.locale}") from e

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.phone_number(), None, self.probability), self.name)

    def __str__(self):
        return f'Phone(name={self.name}, probability={self.probability}, locale={self.locale})'

    def __repr__(self):
        return "Phone()"

class Website:
    '''
        @param name: The name of the column
        @param probability: The probability of the website being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.url(), None, self.probability), self.name)

    def __str__(self):
        return f'Website(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "Website()"

class DomainName:
    '''
        @param name: The name of the column
        @param probability: The probability of the domain name being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.domain_name(), None, self.probability), self.name)

    def __str__(self):
        return f'DomainName(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "DomainName()"

class DomainWord:
    '''
        @param name: The name of the column
        @param probability: The probability of the domain word being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.domain_word(), None, self.probability), self.name)

    def __str__(self):
        return f'DomainWord(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "DomainWord()"

class TLD:
    '''
        @param name: The name of the column
        @param probability: The probability of the TLD being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.tld(), None, self.probability), self.name)

    def __str__(self):
        return f'TLD(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "TLD()"

class Country:
    '''
        @param name: The name of the column
        @param probability: The probability of the country being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.country(), None, self.probability), self.name)

    def __str__(self):
        return f'Country(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "Country()"

class State:
    '''
        @param name: The name of the column
        @param probability: The probability of the state being null. Defaults to 100
        @param state_abbr: Whether to return state abbreviation instead of full name. Defaults to False
    '''
    def __init__(self, name, probability=100, state_abbr=False):
        self.name = name
        self.probability = probability
        self.state_abbr = state_abbr

    def __call__(self, *args, **kwargs):
        state = fake.state_abbr() if self.state_abbr else fake.state()
        return (handle_probability(state, None, self.probability), self.name)

    def __str__(self):
        return f'State(name={self.name}, probability={self.probability}, state_abbr={self.state_abbr})'

    def __repr__(self):
        return "State()"

class City:
    '''
        @param name: The name of the column
        @param probability: The probability of the city being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.city(), None, self.probability), self.name)

    def __str__(self):
        return f'City(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "City()"

class Zip:
    '''
        @param name: The name of the column
        @param probability: The probability of the zip code being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.postcode(), None, self.probability), self.name)

    def __str__(self):
        return f'Zip(name={self.name}, probability={self.probability})'

    def __repr__(self):
        return "Zip()"

class Datetime:
    """
        Generates datetime values between specified start and end dates/times.

        Accepts dates/times in multiple formats:
        - ISO format: "2024-03-14T15:30:00"
        - Date only: "2024-03-14" (assumes 00:00:00)
        - "today", "now" keywords
        - datetime objects
        - Relative times: "+1d", "-2h", etc.
        - No arguments: defaults to between 1970-01-01 and now

        @param name: The name of the column
        @param start_date: The start date/time (inclusive). Defaults to "1970-01-01"
        @param end_date: The end date/time (inclusive). Defaults to "today"
        @param probability: The probability of the datetime being null. Defaults to 100
    """
    def __init__(self, name, start_date=None, end_date=None, probability=100):
        self.name = name
        self.probability = probability

        # Set default values if None
        start_date = start_date or "1970-01-01"
        end_date = end_date or "now"

        # Parse dates
        self.start_date = self._parse_datetime(start_date)
        self.end_date = self._parse_datetime(end_date)

        # Validate date range
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")

    def _parse_datetime(self, dt_value):
        """Parse various datetime input formats"""
        if dt_value is None:
            return datetime.now()

        if isinstance(dt_value, datetime):
            return dt_value

        if isinstance(dt_value, str):
            # Handle keywords
            if dt_value.lower() in ['today', 'now']:
                return datetime.now()

            # Handle relative times
            if dt_value.startswith(('+', '-')):
                return self._parse_relative_time(dt_value)
            # Try parsing different formats
            try:
                # Try ISO format first
                return datetime.fromisoformat(dt_value)
            except ValueError:
                pass
            try:
                # Try date-only format
                return datetime.strptime(dt_value, '%Y-%m-%d')
            except ValueError:
                pass
            try:
                # Try with seconds
                return datetime.strptime(dt_value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
            try:
                # Try without seconds
                return datetime.strptime(dt_value, '%Y-%m-%d %H:%M')
            except ValueError as e:
                raise ValueError(f"Unsupported datetime format: {dt_value}") from e

        raise ValueError(f"Unsupported datetime type: {type(dt_value)}")

    def _parse_relative_time(self, relative_time):
        """Parse relative time strings like +1d, -2h, etc."""
        if not relative_time[1:].isalnum():
            raise ValueError(f"Invalid relative time format: {relative_time}")

        # Get the number and unit
        number = int(relative_time[:-1])
        unit = relative_time[-1].lower()

        # Get current time as base
        base_time = datetime.now()

        # Calculate delta based on unit
        if unit == 'd':
            delta = timedelta(days=number)
        elif unit == 'h':
            delta = timedelta(hours=number)
        elif unit == 'm':
            delta = timedelta(minutes=number)
        elif unit == 's':
            delta = timedelta(seconds=number)
        else:
            raise ValueError(f"Unsupported time unit: {unit}")

        return base_time + delta if relative_time.startswith('+') else base_time - delta

    def __call__(self, *args, **kwargs):
        result = fake.date_time_between(
            start_date=self.start_date,
            end_date=self.end_date
        )
        return (handle_probability(result.strftime('%Y-%m-%d %H:%M:%S'), None, self.probability), self.name)

    def __str__(self):
        return f'Datetime(name={self.name}, start_date={self.start_date}, end_date={self.end_date}, probability={self.probability})'

    def __repr__(self):
        return f"Datetime(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', probability={self.probability})"


class Time:
    """
        Generates time values between specified start and end times.

        Accepts times in multiple formats:
        - 24-hour format: "15:30:00", "15:30"
        - "now" keyword
        - datetime objects
        - Relative times: "+1h", "-2h", etc.
        - No arguments: defaults to between 00:00:00 and 23:59:59

        @param name: The name of the column
        @param start_time: The start time (inclusive). Defaults to "00:00:00"
        @param end_time: The end time (inclusive). Defaults to "23:59:59"
        @param probability: The probability of the time being null
    """
    def __init__(self, name, start_time=None, end_time=None, probability=100):
        self.name = name
        self.probability = probability

        # Set default values if None
        start_time = start_time or "00:00:00"
        end_time = end_time or "23:59:59"

        # Parse times
        self.start_time = self._parse_time(start_time)
        self.end_time = self._parse_time(end_time)

        # Validate time range
        if self.start_time > self.end_time:
            raise ValueError("start_time must be before end_time")

    def _parse_time(self, time_value):
        """Parse various time input formats"""
        if time_value is None:
            return datetime.now().time()

        if isinstance(time_value, datetime):
            return time_value.time()

        if isinstance(time_value, str):
            # Handle keywords
            if time_value.lower() == 'now':
                return datetime.now().time()

            # Handle relative times
            if time_value.startswith(('+', '-')):
                return self._parse_relative_time(time_value).time()

            # Try parsing different formats
            try:
                # Try with seconds
                return datetime.strptime(time_value, '%H:%M:%S').time()
            except ValueError:
                pass
            try:
                # Try without seconds
                return datetime.strptime(time_value, '%H:%M').time()
            except ValueError as e:
                raise ValueError(f"Unsupported time format: {time_value}") from e

        raise ValueError(f"Unsupported time type: {type(time_value)}")

    def _parse_relative_time(self, relative_time):
        """Parse relative time strings like +1h, -2h"""
        if not relative_time[1:].isalnum():
            raise ValueError(f"Invalid relative time format: {relative_time}")

        # Get the number and unit
        number = int(relative_time[:-1])
        unit = relative_time[-1].lower()

        if unit not in ['h', 'm', 's']:
            raise ValueError("Only hours ('h'), minutes ('m'), or seconds ('s') are supported for relative times")

        # Get current time as base
        base_time = datetime.now()

        # Calculate delta based on unit
        if unit == 'h':
            delta = timedelta(hours=number)
        elif unit == 'm':
            delta = timedelta(minutes=number)
        else:  # seconds
            delta = timedelta(seconds=number)

        return base_time + delta if relative_time.startswith('+') else base_time - delta

    def __call__(self, *args, **kwargs):
        # Generate a datetime between today's start_time and end_time
        today = datetime.now().date()
        start_dt = datetime.combine(today, self.start_time)
        end_dt = datetime.combine(today, self.end_time)

        result = fake.date_time_between(
            start_date=start_dt,
            end_date=end_dt
        )
        return (handle_probability(result.strftime('%H:%M:%S'), None, self.probability), self.name)

    def __repr__(self):
        return f"Time(name='{self.name}', start_time='{self.start_time}', end_time='{self.end_time}', probability={self.probability})"

    def __str__(self):
        return f'Time(name={self.name}, probability={self.probability})'

class Timestamp:
    """
        Generates Unix timestamp values between specified start and end dates/times.

        Accepts dates/times in multiple formats:
        - ISO format: "2024-03-14T15:30:00"
        - Date only: "2024-03-14" (assumes 00:00:00)
        - "today", "now" keywords
        - datetime objects
        - Relative times: "+1d", "-2h", etc.
        - No arguments: defaults to between 1970-01-01 and now

        @param name: The name of the column
        @param start_date: The start date/time (inclusive). Defaults to "1970-01-01"
        @param end_date: The end date/time (inclusive). Defaults to "now"
        @param probability: The probability of the timestamp being null
    """
    def __init__(self, name, start_date=None, end_date=None, probability=100):
        self.name = name
        self.probability = probability

        # Set default values if None
        start_date = start_date or "1970-01-01"
        end_date = end_date or "now"

        # Parse dates using Datetime's parser
        datetime_parser = Datetime(name)
        self.start_date = datetime_parser._parse_datetime(start_date)
        self.end_date = datetime_parser._parse_datetime(end_date)

        # Validate date range
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")

    def __call__(self, *args, **kwargs):
        result = fake.date_time_between(
            start_date=self.start_date,
            end_date=self.end_date
        )
        return (handle_probability(int(result.timestamp()), None, self.probability), self.name)

    def __repr__(self):
        return f"Timestamp(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', probability={self.probability})"

    def __str__(self):
        return f'Timestamp(name={self.name}, probability={self.probability})'

class TimeZone:
    '''
        @param name: The name of the column
        @param probability: The probability of the timezone being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.timezone(), None, self.probability), self.name)

    def __repr__(self):
        return f"TimeZone(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'TimeZone(name={self.name}, probability={self.probability})'

class DayOfWeek:
    '''
        @param name: The name of the column
        @param probability: The probability of the day of week being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.day_of_week(), None, self.probability), self.name)

    def __repr__(self):
        return f"DayOfWeek(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'DayOfWeek(name={self.name}, probability={self.probability})'

class UUID:
    '''
        @param name: The name of the column
        @param probability: The probability of the UUID being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.uuid4(), None, self.probability), self.name)  # Default to v4

    def __repr__(self):
        return f"UUID(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'UUID(name={self.name}, probability={self.probability})'

class Color:
    '''
        @param name: The name of the column
        @param color_type: The type of color to generate. Defaults to "name"
        @param probability: The probability of the color being null. Defaults to 100
    '''
    def __init__(self, name, color_type="name", probability=100):
        self.name = name
        self.color_type = color_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.color_type == "name":
            return (handle_probability(fake.color_name(), None, self.probability), self.name)
        if self.color_type == "hex":
            return (handle_probability(fake.hex_color(), None, self.probability), self.name)
        if self.color_type == "rgb":
            return (handle_probability(fake.rgb_color(), None, self.probability), self.name)
        return (handle_probability(fake.color_name(), None, self.probability), self.name)  # Default to color name

    def __repr__(self):
        return f"Color(name='{self.name}', color_type='{self.color_type}', probability={self.probability})"

    def __str__(self):
        return f'Color(name={self.name}, color_type={self.color_type}, probability={self.probability})'

class JobTitle:
    '''
        @param name: The name of the column
        @param probability: The probability of the job title being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.job(), None, self.probability), self.name)

    def __repr__(self):
        return f"JobTitle(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'JobTitle(name={self.name}, probability={self.probability})'

class CompanyDepartment:
    '''
        @param name: The name of the column
        @param probability: The probability of the company department being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.job(), None, self.probability), self.name)

    def __repr__(self):
        return f"CompanyDepartment(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'CompanyDepartment(name={self.name}, probability={self.probability})'

class FileExtension:
    '''
        @param name: The name of the column
        @param probability: The probability of the file extension being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.file_extension(), None, self.probability), self.name)

    def __repr__(self):
        return f"FileExtension(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'FileExtension(name={self.name}, probability={self.probability})'

class SocialMediaHandle:
    '''
        @param name: The name of the column
        @param platform: The platform of the social media handle. Defaults to None
        @param probability: The probability of the social media handle being null. Defaults to 100
    '''
    def __init__(self, name, platform=None, probability=100):
        self.name = name
        self.platform = platform
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.platform:
            if self.platform.lower() == "twitter":
                return (handle_probability(f"@{fake.user_name()}", None, self.probability), self.name)
            if self.platform.lower() == "instagram":
                return (handle_probability(f"instagram_{fake.user_name()}", None, self.probability), self.name)
            if self.platform.lower() == "facebook":
                return (handle_probability(f"{fake.user_name()}", None, self.probability), self.name)
            return (handle_probability(f"{fake.user_name()}", None, self.probability), self.name)
        return (handle_probability(f"@{fake.user_name()}", None, self.probability), self.name)  # Default to Twitter-like handle

    def __repr__(self):
        return f"SocialMediaHandle(name='{self.name}', platform='{self.platform}', probability={self.probability})"

    def __str__(self):
        return f'SocialMediaHandle(name={self.name}, platform={self.platform}, probability={self.probability})'

class IPAddress:
    '''
        @param name: The name of the column
        @param version: The version of the IP address. Defaults to "ipv4"
        @param probability: The probability of the IP address being null. Defaults to 100
    '''
    def __init__(self, name, version="ipv4", probability=100):
        self.name = name
        self.version = version.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.version == "ipv4":
            return (handle_probability(fake.ipv4(), None, self.probability), self.name)
        if self.version == "ipv6":
            return (handle_probability(fake.ipv6(), None, self.probability), self.name)
        return (handle_probability(fake.ipv4(), None, self.probability), self.name)  # Default to IPv4

    def __repr__(self):
        return f"IPAddress(name='{self.name}', version='{self.version}', probability={self.probability})"

    def __str__(self):
        return f'IPAddress(name={self.name}, version={self.version}, probability={self.probability})'

class LatitudeLongitude:
    '''
        @param name: The name of the column
        @param probability: The probability of the latitude and longitude being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(f'{fake.latitude()}, {fake.longitude()}', None, self.probability), self.name)

    def __repr__(self):
        return f"LatitudeLongitude(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'LatitudeLongitude(name={self.name}, probability={self.probability})'

class Version:
    '''
        @param name: The name of the column
        @param major_min: The minimum major version. Defaults to 0
        @param major_max: The maximum major version. Defaults to 10
        @param minor_min: The minimum minor version. Defaults to 0
        @param minor_max: The maximum minor version. Defaults to 10
        @param patch_min: The minimum patch version. Defaults to 0
        @param patch_max: The maximum patch version. Defaults to 10
        @param probability: The probability of the version being null. Defaults to 100
    '''
    def __init__(self, name, major_min=0, major_max=10, minor_min=0, minor_max=10, patch_min=0, patch_max=10, probability=100):
        self.name = name
        self.major_min = major_min
        self.major_max = major_max
        self.minor_min = minor_min
        self.minor_max = minor_max
        self.patch_min = patch_min
        self.patch_max = patch_max
        self.probability = probability

    def __call__(self, *args, **kwargs):
        major = random.randint(self.major_min, self.major_max)
        minor = random.randint(self.minor_min, self.minor_max)
        patch = random.randint(self.patch_min, self.patch_max)
        return (handle_probability(f"{major}.{minor}.{patch}", None, self.probability), self.name)

    def __repr__(self):
        return f"Version(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'Version(name={self.name}, probability={self.probability})'

class URL:
    '''
        @param name: The name of the column
        @param probability: The probability of the URL being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.url(), None, self.probability), self.name)

    def __repr__(self):
        return f"URL(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'URL(name={self.name}, probability={self.probability})'

class Sentence:
    '''
        @param name: The name of the column
        @param nb_words: The number of words in the sentence. Defaults to 6
        @param variable_nb_words: The number of words in the sentence. Defaults to 6
        @param probability: The probability of the sentence being null. Defaults to 100
    '''
    def __init__(self, name, nb_words=6, variable_nb_words=6, probability=100):
        self.name = name
        self.nb_words = nb_words
        self.variable_nb_words = variable_nb_words
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.sentence(nb_words=self.nb_words, variable_nb_words=self.variable_nb_words), None, self.probability), self.name)

    def __repr__(self):
        return f"Sentence(name='{self.name}', nb_words={self.nb_words}, variable_nb_words={self.variable_nb_words}, probability={self.probability})"

    def __str__(self):
        return f'Sentence(name={self.name}, probability={self.probability})'

class Paragraph:
    '''
        @param name: The name of the column
        @param nb_sentences: The number of sentences in the paragraph. Defaults to 3
        @param variable_nb_sentences: The number of sentences in the paragraph. Defaults to 3
        @param nb_words: The number of words in the paragraph. Defaults to 6
        @param variable_nb_words: The number of words in the paragraph. Defaults to 6
        @param probability: The probability of the paragraph being null. Defaults to 100
    '''
    def __init__(self, name, nb_sentences=3, variable_nb_sentences=3, probability=100):
        self.name = name
        self.nb_sentences = nb_sentences
        self.variable_nb_sentences = variable_nb_sentences
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.paragraph(nb_sentences=self.nb_sentences, variable_nb_sentences=self.variable_nb_sentences), None, self.probability), self.name)

    def __repr__(self):
        return f"Paragraph(name='{self.name}', nb_sentences={self.nb_sentences}, variable_nb_sentences={self.variable_nb_sentences}, probability={self.probability})"

    def __str__(self):
        return f'Paragraph(name={self.name}, probability={self.probability})'

class UserAgent:
    '''
        @param name: The name of the column
        @param probability: The probability of the user agent being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.user_agent(), None, self.probability), self.name)

    def __repr__(self):
        return f"UserAgent(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'UserAgent(name={self.name}, probability={self.probability})'

class Hash:
    '''
        @param name: The name of the column
        @param hash_type: The type of hash to generate. Defaults to "sha256"
        @param probability: The probability of the hash being null. Defaults to 100
    '''
    def __init__(self, name, hash_type="sha256", probability=100):
        self.name = name
        self.hash_type = hash_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.hash_type == "md5":
            return (handle_probability(fake.md5(), None, self.probability), self.name)
        if self.hash_type == "sha1":
            return (handle_probability(fake.sha1(), None, self.probability), self.name)
        if self.hash_type == "sha256":
            return (handle_probability(fake.sha256(), None, self.probability), self.name)
        return (handle_probability(fake.sha256(), None, self.probability), self.name)  # Default to SHA256

    def __repr__(self):
        return f"Hash(name='{self.name}', hash_type='{self.hash_type}', probability={self.probability})"

    def __str__(self):
        return f'Hash(name={self.name}, hash_type={self.hash_type}, probability={self.probability})'

class ISBN:
    '''
        @param name: The name of the column
        @param probability: The probability of the ISBN being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.isbn10(), None, self.probability), self.name)

    def __repr__(self):
        return f"ISBN(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'ISBN(name={self.name}, probability={self.probability})'

class ISBN13:
    '''
        @param name: The name of the column
        @param probability: The probability of the ISBN13 being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.isbn13(), None, self.probability), self.name)

    def __repr__(self):
        return f"ISBN13(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'ISBN13(name={self.name}, probability={self.probability})'

class EAN:
    '''
        @param name: The name of the column
        @param probability: The probability of the EAN being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.ean(), None, self.probability), self.name)

    def __repr__(self):
        return f"EAN(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'EAN(name={self.name}, probability={self.probability})'

class SKU:
    '''
        @param name: The name of the column
        @param prefix: The prefix of the SKU. Defaults to ""
        @param length: The length of the SKU. Defaults to 8
        @param probability: The probability of the SKU being null. Defaults to 100
    '''
    def __init__(self, name, prefix="", length=8, probability=100):
        self.name = name
        self.prefix = prefix
        self.length = length
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(self.prefix + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=self.length)), None, self.probability), self.name)

    def __repr__(self):
        return f"SKU(name='{self.name}', prefix='{self.prefix}', length={self.length}, probability={self.probability})"

    def __str__(self):
        return f'SKU(name={self.name}, probability={self.probability})'

class MACAddress:
    '''
        @param name: The name of the column
        @param probability: The probability of the MAC address being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(':'.join([f'{random.randint(0, 255)}' for _ in range(6)]), None, self.probability), self.name)

    def __repr__(self):
        return f"MACAddress(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'MACAddress(name={self.name}, probability={self.probability})'

class CreditCardNumber:
    '''
        @param name: The name of the column
        @param card_type: The type of credit card to generate. Defaults to "visa"
        @param probability: The probability of the credit card number being null. Defaults to 100
    '''
    def __init__(self, name, card_type="visa", probability=100):
        self.name = name
        self.card_type = card_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.card_type == "visa":
            return (handle_probability(fake.credit_card_number(card_type="visa"), None, self.probability), self.name)
        if self.card_type == "mastercard":
            return (handle_probability(fake.credit_card_number(card_type="mastercard"), None, self.probability), self.name)
        if self.card_type == "amex":
            return (handle_probability(fake.credit_card_number(card_type="amex"), None, self.probability), self.name)
        if self.card_type == "discover":
            return (handle_probability(fake.credit_card_number(card_type="discover"), None, self.probability), self.name)
        return (handle_probability(fake.credit_card_number(), None, self.probability), self.name)

    def __repr__(self):
        return f"CreditCardNumber(name='{self.name}', card_type='{self.card_type}', probability={self.probability})"

    def __str__(self):
        return f'CreditCardNumber(name={self.name}, probability={self.probability})'

class IBAN:
    '''
    @param name: The name of the column
    @param country_code: The country code of the IBAN. Defaults to None
    @param probability: The probability of the IBAN being null. Defaults to 100
'''
    def __init__(self, name, country_code=None, probability=100):
        self.name = name
        self.country_code = country_code
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if self.country_code:
            # Implement country-specific IBAN generation (requires more complex logic)
            return (handle_probability(f"{self.country_code}{fake.iban()}", None, self.probability), self.name)
        return (handle_probability(fake.iban(), None, self.probability), self.name)

    def __repr__(self):
        return f"IBAN(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'IBAN(name={self.name}, probability={self.probability})'

class BIC:
    '''
        @param name: The name of the column
        @param probability: The probability of the BIC being null. Defaults to 100
    '''
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(fake.swift(), None, self.probability), self.name)

    def __repr__(self):
        return f"BIC(name='{self.name}', probability={self.probability})"

    def __str__(self):
        return f'BIC(name={self.name}, probability={self.probability})'
