# Quick-Seeders

A Python package for generating realistic test data with a simple, flexible API.

## Installation

```bash
pip install quick-seeders
```

## Features

- Generate realistic test data with minimal setup
- Support for 40+ data types including:
  - Basic types (text, numbers, booleans)
  - Personal data (names, emails, phones)
  - Dates and times (with flexible format support)
  - Geographic data (addresses, coordinates)
  - Financial data (currency, credit cards, IBANs)
  - Internet data (URLs, IPs, user agents)
  - And many more!
- Export to multiple formats (JSON, CSV, SQL)
- Probability-based null values
- Flexible date/time range specifications
- Schema-based or direct generator usage

## Quick Start

### Using Schema Definition

```python
from seeder import Seeder

# Define your schema
schema = [
    {
        "name": "id",
        "type": "integer",
        "min": 1,
        "max": 1000
    },
    {
        "name": "first_name",
        "type": "name"
    },
    {
        "name": "email",
        "type": "email",
        "email_type": "company"
    },
    {
        "name": "hire_date",
        "type": "datetime",
        "start_date": "2020-01-01",
        "end_date": "today"
    }
]

# Generate data
seeder = Seeder()
data = seeder.seed(schema, count=100)

# Export to different formats
seeder.to_json('employees')
seeder.to_csv('employees')
seeder.to_sql('insert_employees', 'employees')
```

### Using Direct Generators

```python
from seeder import Seeder
from seeder.types import ID, Name, Email, Date

seeder = Seeder()
data = seeder.seed([
    ID('id'),
    Name('first_name'),
    Email('email', email_type='company'),
    Date('hire_date', start_date='-30d', end_date='today')
], count=100)
```

## Advanced Features

### Date/Time Formatting

Support for multiple date/time formats and relative times:

```python
from seeder.types import Datetime, Date, Time

# ISO format
dt1 = Datetime('timestamp', "2024-03-14T09:00:00", "2024-03-14T17:00:00")

# Date only
dt2 = Date('date', "2024-03-14", "2024-03-15")

# Keywords
dt3 = Datetime('current', "today", "now")

# Relative times
dt4 = Datetime('recent', "-1h", "now")  # Last hour
dt5 = Date('past_week', "-7d", "today")  # Last 7 days
```

### Probability-Based Null Values

Control the probability of generating null values:

```python
from seeder.types import Text, Number

# 50% chance of being null
text = Text('description', probability=50)

# 80% chance of having a value
number = Number('score', probability=80)
```

## Available Types

### Basic Types
- Text
- Int
- Number
- Bool
- Null
- Enum

### Personal Information
- Name
- Email
- Phone
- Address

### Dates and Times
- Date
- Datetime
- Time
- Timestamp
- TimeZone
- DayOfWeek

### Geographic
- Country
- State
- City
- Zip
- LatitudeLongitude

### Internet
- Website
- URL
- IPAddress
- UserAgent
- SocialMediaHandle
- MACAddress

### Financial
- Currency
- CreditCardNumber
- IBAN
- BIC

### Identifiers
- ID
- UUID
- SKU
- ISBN
- ISBN13
- EAN
- Hash

### Text Content
- Sentence
- Paragraph
- LoremIpsum

### Business
- JobTitle
- CompanyDepartment

## Type Options

### Common Parameters
All types accept these basic parameters:
- `name`: The column name for the generated data
- `probability`: Chance of generating a value vs null (0-100)

### Type-Specific Parameters

#### Date/Time Types
```python
Datetime(name, start_date="1970-01-01", end_date="today")
Date(name, start_date="1970-01-01", end_date="today")
Time(name, start_time="00:00:00", end_time="23:59:59")
```

#### Text Types
```python
Text(name, min_length=10, max_length=100)
Sentence(name, nb_words=6, variable_nb_words=True)
Paragraph(name, nb_sentences=3, variable_nb_sentences=True)
```

#### Number Types
```python
Int(name, min_value=0, max_value=99999)
Currency(name, symbol="$", min_value=0, max_value=1000)
```

#### Email Types
```python
Email(name, email_type="safe")  # Types: safe, free, company
```

## Export Formats

### JSON Export
```python
seeder.to_json('filename')  # Creates filename.json
```

### CSV Export
```python
seeder.to_csv('filename')  # Creates filename.csv
```

### SQL Export
```python
seeder.to_sql('filename', 'table_name')  # Creates filename.sql
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

Would you like me to add any additional sections or make any adjustments to the formatting?