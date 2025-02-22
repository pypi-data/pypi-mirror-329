# Quick-Seeders

A Python utility for generating large amounts of realistic fake data for testing and development. Quick-Seeders allows you to define data schemas and generate data based on various built-in data types, including names, addresses, emails, phone numbers, currencies, and more.

## Features

*   **Schema-based data generation:** Define your data structure using simple JSON or Python dictionaries.
*   **Built-in data types:** Supports a wide range of data types, including:
    *   Text (with configurable length)
    *   Currency (with symbol, min/max values)
    *   Enums (with predefined choices)
    *   IDs (with prefix and length)
    *   Names
    *   Addresses
    *   Emails (with different types: random, safe, free, company, specific domain)
    *   Phone Numbers (with locale support)
    *   Websites, Domain Names, Domain Words, TLDs
    *   Countries, States (with abbreviations), Cities, Zip codes
    *   Booleans
*   **Probability control:** Set the probability of generating a value for each field.
*   **SQL output:** Easily write generated data to `.sql` files with `INSERT` statements and optional `CREATE TABLE` statements.
*   **Easy to use:** Simple API for generating data with minimal code.
*   **Extensible:** Easily add custom data types or generators.

## Installation

```bash
pip install quick-seeders
```

## Usage

### Example using a list of generators

```python
from quick_seeders.seeder import ID, Name, Address, Currency, Boolean, Text, Enum, seed
import json

generators = [
    ID(prefix="USER-"),
    Name(),
    Address(),
    Currency(symbol="£"),
    Boolean(),
    Text(max_length=100),
    Enum(['Small', 'Medium', 'Large'])
]

generated_data = seed(generators, num_records=3)
print(json.dumps(generated_data, indent=2))
```

### Example using named generators (for explicit field names):

```python
from quick_seeders.seeder import ID, Name, Address, Currency, Boolean, Text, Enum, seed_with_names
import json

named_generators = {
    "user_id": ID(prefix="USER-"),
    "full_name": Name(),
    "home_address": Address(),
    "account_balance": Currency(symbol="€"),
    "is_active": Boolean(),
    "description": Text(max_length=100),
    "size": Enum(['Small', 'Medium', 'Large'])
}

named_generated_data = seed_with_names(named_generators, num_records=3)
print(json.dumps(named_generated_data, indent=2))
```

### Writing to SQL

```python
from quick_seeders.seeder import ID, Name, seed, write_to_sql

generators = [ID(), Name()]
generated_data = seed(generators, num_records=5)
write_to_sql(generated_data, "users", "users.sql")
```

This will create a `users.sql` file containing the generated data as SQL `INSERT` commands.

## Defining Schemas (Alternative to generator lists/dicts)

You can define schemas in JSON format and use the `Seeder` class:

```JSON
{
  "schema_name": "product",
  "fields": [
    {"name": "id", "type": "integer", "min": 1, "max": 1000},
    {"name": "name", "type": "text", "max_length": 50},
    {"name": "price", "type": "currency", "symbol": "$", "min_value": 10, "max_value":100},
    {"name": "in_stock", "type": "boolean"}
  ]
}
```

Then in Python:

```python
from quick_seeders.seeder import Seeder
import json

seeder = Seeder()
try:
    with open("schema.json", "r") as f:
        schema = json.load(f)
    data = seeder.seed(schema, 5)
    print(json.dumps(data, indent=2))
except FileNotFoundError:
    print("Schema file not found")
except json.JSONDecodeError:
    print("Invalid JSON in schema file")
except (ValueError, TypeError, AttributeError) as e:
    print(f"Error seeding data: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is open-sourced under the MIT License - see the LICENSE file for details.
