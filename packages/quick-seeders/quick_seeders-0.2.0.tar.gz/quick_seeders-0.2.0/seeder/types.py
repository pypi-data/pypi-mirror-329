import random
from typing import Any, Dict, List, Union
from datetime import datetime
from faker import Faker

fake = Faker("en_US")

def handle_probability(value, fallback, probability):
    sample = random.random()
    if sample < probability / 100:
        return value
    else:
        return fallback

'''
    @param name: The name of the column
    @param value: The possible fallback value if the column is not null. Can be another faked data type
    @param probability: The probability of the column being null
'''
class Null:
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


'''
    @param name: The name of the column
    @param value: The int value to be used. If not provided, a random int will be generated.
'''
class Int:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (value if value else random.randint(1, 99999999), self.name)
        
    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        return "Int()"

'''
    @param name: The name of the column
    @param value: The float or int value to be used. If not provided, a random int will be generated.
'''
class Number:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (value if value else random.randint(1, 99999999), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Number()"

'''
    @param name: The name of the column
    @param value: The bool value to be used. If not provided, a random bool will be generated.
'''
class Bool:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (value if value else random.choice([True, False]), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Bool()"

'''
    @param name: The name of the column
    @param value: The str value to be used. If not provided, an empty str will be generated.
    @param probability: The probability of the text being empty. Defaults to 0
'''
class Text:
    def __init__(self, name, value=None, probability=0):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (value if value else handle_probability(value, fake.sentence(nb_words=10), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Text()"

'''
    @param name: The name of the column
    @param value: The date value to be used. If not provided, the current date will be generated.
    @param probability: The probability of the date being today. Defaults to 0
'''
class Date:
    def __init__(self, name, value=None, probability=0):
        self.name = name
        self.value = value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if callable(self.value):
            value = self.value()[0]
        else:
            value = self.value
        return (value if value else handle_probability(value, str(datetime.now()), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Date()"

'''
    @param name: The name of the column
    @param symbol: The symbol of the currency. Defaults to $
    @param min_value: The minimum value of the currency. Defaults to 0
    @param max_value: The maximum value of the currency. Defaults to 1000
    @param probability: The probability of the currency being null. Defaults to 100
'''
class Currency:
    def __init__(self, name, symbol="$", min_value=0, max_value=1000, probability=0):
        self.name = name
        self.symbol = symbol
        self.min_value = min_value
        self.max_value = max_value
        self.probability = probability

    def __call__(self, *args, **kwargs):
        value = f"{self.symbol}{random.randint(self.min_value, self.max_value):.2f}"
        return (handle_probability(None, value, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Currency()"

'''
    @param name: The name of the column
    @param choices: The list of choices to be used. If not provided, an empty list will be generated.
    @param probability: The probability of the enum being null. Defaults to 0
'''
class Enum:
    def __init__(self, name, choices: List[Any], probability=0):
        if not choices:
            raise ValueError("Enum must have at least one choice.")
        self.name = name
        self.choices = choices
        self.probability = probability

    def __call__(self, *args, **kwargs):
        choices = [(choice() if callable(choice) else choice) for choice in self.choices]
        return (handle_probability(None, random.choice(choices), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Enum()"

'''
    @param name: The name of the column
    @param prefix: The prefix of the id. Defaults to an empty str
    @param probability: The probability of the id being null. Defaults to 0
'''
class ID:
    def __init__(self, name, prefix="", probability=0):
        self.name = name
        self.prefix = prefix
        self.probability = probability

    def __call__(self, *args, **kwargs):
        uuid = fake.uuid4()
        if len(self.prefix) > len(uuid):
            raise ValueError('Prefix cannot be longer than the id')
        id_value = self.prefix + uuid[len(self.prefix):]
        return (handle_probability(None, id_value, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "ID()"

'''
    @param name: The name of the column
    @param probability: The probability of the name being null. Defaults to 0
'''
class Name:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.name(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Name()"

'''
    @param name: The name of the column
    @param probability: The probability of the address being null. Defaults to 0
'''
class Address:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.address(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Address()"

'''
    @param name: The name of the column
    @param email_type: The type of the email. Defaults to random
    @param domain: The domain of the email. Defaults to None
    @param probability: The probability of the email being null. Defaults to 0
'''
class Email:
    def __init__(self, name, email_type="random", domain=None, probability=0):
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
        return (handle_probability(None, email, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Email()"

'''
    @param name: The name of the column
    @param probability: The probability of the phone being null. Defaults to 0
    @param locale: The locale of the phone. Defaults to None
'''
class Phone:
    def __init__(self, name, probability=0, locale=None):
        self.name = name
        self.probability = probability
        self.locale = locale
        if self.locale:
            try:
                Faker(self.locale)
            except AttributeError:
                raise ValueError(f"Invalid locale: {self.locale}")

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.phone_number(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Phone()"

'''
    @param name: The name of the column
    @param probability: The probability of the website being null. Defaults to 0
'''
class Website:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.url(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Website()"

'''
    @param name: The name of the column
    @param probability: The probability of the domain name being null. Defaults to 0
'''
class DomainName:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.domain_name(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "DomainName()"

'''
    @param name: The name of the column
    @param probability: The probability of the domain word being null. Defaults to 0
'''
class DomainWord:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.domain_word(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "DomainWord()"

'''
    @param name: The name of the column
    @param probability: The probability of the TLD being null. Defaults to 0
'''
class TLD:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.tld(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "TLD()"

'''
    @param name: The name of the column
    @param probability: The probability of the country being null. Defaults to 0
'''
class Country:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.country(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Country()"

'''
    @param name: The name of the column
    @param probability: The probability of the state being null. Defaults to 0
    @param state_abbr: Whether to return state abbreviation instead of full name. Defaults to False
'''
class State:
    def __init__(self, name, probability=0, state_abbr=False):
        self.name = name
        self.probability = probability
        self.state_abbr = state_abbr

    def __call__(self, *args, **kwargs):
        state = fake.state_abbr() if self.state_abbr else fake.state()
        return (handle_probability(None, state, self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "State()"

'''
    @param name: The name of the column
    @param probability: The probability of the city being null. Defaults to 0
'''
class City:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.city(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "City()"

'''
    @param name: The name of the column
    @param probability: The probability of the zip code being null. Defaults to 0
'''
class Zip:
    def __init__(self, name, probability=0):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        return (handle_probability(None, fake.postcode(), self.probability), self.name)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Zip()"

class Datetime:
    def __init__(self, name, start_date=datetime(1970, 1, 1), end_date="today", probability=100):
        self.name = name
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date != 'today' else datetime.now()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            # Convert 'today' to current datetime if specified
            end_date = datetime.now() if self.end_date == 'today' else self.end_date
            return (fake.date_time_between(
                start_date=self.start_date,
                end_date=end_date
            ).strftime('%Y-%m-%d %H:%M:%S'), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"Datetime(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', probability={self.probability})"

class Time:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.time(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"Time(name='{self.name}', probability={self.probability})"

class Timestamp:
    def __init__(self, name, start_date="1970-01-01", end_date="today", probability=100):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.date_time_between(start_date=self.start_date, end_date=self.end_date).timestamp(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"Timestamp(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', probability={self.probability})"

class TimeZone:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.timezone(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"TimeZone(name='{self.name}', probability={self.probability})"

class DayOfWeek:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.day_of_week(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"DayOfWeek(name='{self.name}', probability={self.probability})"

class UUID:
    def __init__(self, name, version=4, probability=100):
        self.name = name
        self.version = version
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.version == 4:
                return (fake.uuid4(), self.name)
            elif self.version == 1:
                return (fake.uuid1(), self.name)
            elif self.version == 3:
                return (fake.uuid3(), self.name)
            elif self.version == 5:
                return (fake.uuid5(), self.name)
            else:
                return (fake.uuid4(), self.name)  # Default to v4
        return (None, self.name)

    def __repr__(self):
        return f"UUID(name='{self.name}', version={self.version}, probability={self.probability})"

class Color:
    def __init__(self, name, color_type="name", probability=100):
        self.name = name
        self.color_type = color_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.color_type == "name":
                return (fake.color_name(), self.name)
            elif self.color_type == "hex":
                return (fake.hex_color(), self.name)
            elif self.color_type == "rgb":
                return (fake.rgb_color(), self.name)
            else:
                return (fake.color_name(), self.name)  # Default to color name
        return (None, self.name)

    def __repr__(self):
        return f"Color(name='{self.name}', color_type='{self.color_type}', probability={self.probability})"

class JobTitle:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.job(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"JobTitle(name='{self.name}', probability={self.probability})"

class CompanyDepartment:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.job(), self.name)  # Use job() as a temporary placeholder
        return (None, self.name)

    def __repr__(self):
        return f"CompanyDepartment(name='{self.name}', probability={self.probability})"

class FileExtension:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.file_extension(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"FileExtension(name='{self.name}', probability={self.probability})"

class SocialMediaHandle:
    def __init__(self, name, platform=None, probability=100):
        self.name = name
        self.platform = platform
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.platform:
                if self.platform.lower() == "twitter":
                    return (f"@{fake.user_name()}", self.name)
                elif self.platform.lower() == "instagram":
                    return (f"instagram_{fake.user_name()}", self.name)
                elif self.platform.lower() == "facebook":
                    return (f"{fake.user_name()}", self.name) 
                else:
                    return (f"{fake.user_name()}", self.name) 
            else:
                return (f"@{fake.user_name()}", self.name)  # Default to Twitter-like handle
        return (None, self.name)

    def __repr__(self):
        return f"SocialMediaHandle(name='{self.name}', platform='{self.platform}', probability={self.probability})"

class IPAddress:
    def __init__(self, name, version="ipv4", probability=100):
        self.name = name
        self.version = version.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.version == "ipv4":
                return (fake.ipv4(), self.name)
            elif self.version == "ipv6":
                return (fake.ipv6(), self.name)
            else:
                return (fake.ipv4(), self.name)  # Default to IPv4
        return (None, self.name)

    def __repr__(self):
        return f"IPAddress(name='{self.name}', version='{self.version}', probability={self.probability})"

class LatitudeLongitude:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (f'{fake.latitude()}, {fake.longitude()}', self.name)
        return (None, self.name)

    def __repr__(self):
        return f"LatitudeLongitude(name='{self.name}', probability={self.probability})"

class Version:
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
        if random.randint(1, 100) <= self.probability:
            major = random.randint(self.major_min, self.major_max)
            minor = random.randint(self.minor_min, self.minor_max)
            patch = random.randint(self.patch_min, self.patch_max)
            return (f"{major}.{minor}.{patch}", self.name) 
        return (None, self.name)

    def __repr__(self):
        return f"Version(name='{self.name}', major_min={self.major_min}, major_max={self.major_max}, minor_min={self.minor_min}, minor_max={self.minor_max}, patch_min={self.patch_min}, patch_max={self.patch_max}, probability={self.probability})"

class URL:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.url(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"URL(name='{self.name}', probability={self.probability})"

class Sentence:
    def __init__(self, name, nb_words=6, variable_nb_words=6, probability=100):
        self.name = name
        self.nb_words = nb_words
        self.variable_nb_words = variable_nb_words
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.sentence(nb_words=self.nb_words, variable_nb_words=self.variable_nb_words), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"Sentence(name='{self.name}', nb_words={self.nb_words}, variable_nb_words={self.variable_nb_words}, probability={self.probability})"

class Paragraph:
    def __init__(self, name, nb_sentences=3, variable_nb_sentences=3, nb_words=6, variable_nb_words=6, probability=100):
        self.name = name
        self.nb_sentences = nb_sentences
        self.variable_nb_sentences = variable_nb_sentences
        self.nb_words = nb_words
        self.variable_nb_words = variable_nb_words
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.paragraph(nb_sentences=self.nb_sentences, variable_nb_sentences=self.variable_nb_sentences, nb_words=self.nb_words, variable_nb_words=self.variable_nb_words), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"Paragraph(name='{self.name}', nb_sentences={self.nb_sentences}, variable_nb_sentences={self.variable_nb_sentences}, nb_words={self.nb_words}, variable_nb_words={self.variable_nb_words}, probability={self.probability})"

class LoremIpsum:
    def __init__(self, name, nb_sentences=3, variable_nb_sentences=3, nb_words=6, variable_nb_words=6, probability=100):
        self.name = name
        self.nb_sentences = nb_sentences
        self.variable_nb_sentences = variable_nb_sentences
        self.nb_words = nb_words
        self.variable_nb_words = variable_nb_words
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.text(nb_sentences=self.nb_sentences, variable_nb_sentences=self.variable_nb_sentences, nb_words=self.nb_words, variable_nb_words=self.variable_nb_words), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"LoremIpsum(name='{self.name}', nb_sentences={self.nb_sentences}, variable_nb_sentences={self.variable_nb_sentences}, nb_words={self.nb_words}, variable_nb_words={self.variable_nb_words}, probability={self.probability})"

class UserAgent:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.user_agent(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"UserAgent(name='{self.name}', probability={self.probability})"

class Hash:
    def __init__(self, name, hash_type="sha256", probability=100):
        self.name = name
        self.hash_type = hash_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.hash_type == "md5":
                return (fake.md5(), self.name)
            elif self.hash_type == "sha1":
                return (fake.sha1(), self.name)
            elif self.hash_type == "sha256":
                return (fake.sha256(), self.name)
            # Add more hash types as needed
            else:
                return (fake.sha256(), self.name)  # Default to SHA256
        return (None, self.name)

    def __repr__(self):
        return f"Hash(name='{self.name}', hash_type='{self.hash_type}', probability={self.probability})"

class ISBN:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.isbn10(), self.name) 
        return (None, self.name)

    def __repr__(self):
        return f"ISBN(name='{self.name}', probability={self.probability})"

class ISBN13:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.isbn13(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"ISBN13(name='{self.name}', probability={self.probability})"

class EAN:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.ean(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"EAN(name='{self.name}', probability={self.probability})"

class SKU:
    def __init__(self, name, prefix="", length=8, probability=100):
        self.name = name
        self.prefix = prefix
        self.length = length
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (self.prefix + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=self.length)), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"SKU(name='{self.name}', prefix='{self.prefix}', length={self.length}, probability={self.probability})"

class MACAddress:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)]), self.name) 
        return (None, self.name)

    def __repr__(self):
        return f"MACAddress(name='{self.name}', probability={self.probability})"

class CreditCardNumber:
    def __init__(self, name, card_type="visa", probability=100):
        self.name = name
        self.card_type = card_type.lower()
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.card_type == "visa":
                return (fake.credit_card_number(card_type="visa"), self.name)
            elif self.card_type == "mastercard":
                return (fake.credit_card_number(card_type="mastercard"), self.name)
            elif self.card_type == "amex":
                return (fake.credit_card_number(card_type="amex"), self.name)
            elif self.card_type == "discover":
                return (fake.credit_card_number(card_type="discover"), self.name)
            else:
                return (fake.credit_card_number(), self.name)  # Default to visa
        return (None, self.name)

    def __repr__(self):
        return f"CreditCardNumber(name='{self.name}', card_type='{self.card_type}', probability={self.probability})"

class IBAN:
    def __init__(self, name, country_code=None, probability=100):
        self.name = name
        self.country_code = country_code
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            if self.country_code:
                # Implement country-specific IBAN generation (requires more complex logic)
                return (f"{self.country_code}{fake.iban()}", self.name) 
            else:
                return (fake.iban(), self.name)
        return (None, self.name)

    def __repr__(self):
        return f"IBAN(name='{self.name}', country_code='{self.country_code}', probability={self.probability})"

class BIC:
    def __init__(self, name, probability=100):
        self.name = name
        self.probability = probability

    def __call__(self, *args, **kwargs):
        if random.randint(1, 100) <= self.probability:
            return (fake.swift(), self.name) 
        return (None, self.name)

    def __repr__(self):
        return f"BIC(name='{self.name}', probability={self.probability})"
