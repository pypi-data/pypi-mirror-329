'''
    Seeder is the main class for generating fake data.
'''
import json
import os
import csv
import random
from typing import Any, Dict, List, Union
from pathlib import Path

from seeder.types import (
    Null,
    Int,
    Number,
    Bool,
    Date,
    Datetime,
    Time,
    Timestamp,
    TimeZone,
    DayOfWeek,
    UUID,
    Color,
    JobTitle,
    CompanyDepartment,
    FileExtension,
    SocialMediaHandle,
    IPAddress,
    LatitudeLongitude,
    Version,
    Sentence,
    Paragraph,
    UserAgent,
    Hash,
    ISBN,
    ISBN13,
    EAN,
    SKU,
    MACAddress,
    CreditCardNumber,
    IBAN,
    Enum,
    BIC,
    Text,
    Currency,
    Email,
    Phone,
    Website,
    DomainName,
    DomainWord,
    TLD,
    Country,
    State,
    City,
    Zip,
    Address,
    Name,
    ID,
)

class Seeder:
    '''
        Main seeder class
    '''
    def __init__(self):
        self.data = {}
        self.export_path = self.make_export_dir()

    def seed(self, schema: Union[List[Any], List[Dict[str, Any]]], count: int = 1) -> List[Dict[str, Any]]:
        """
        Generate seed data based on schema

        Args:
            schema: Either a list of generators or a schema definition list
            count: Number of records to generate

        Returns:
            List of generated records
        """
        # Convert schema to generators if it's a schema definition
        if schema and isinstance(schema[0], dict):
            generators = self.schema_to_generators(schema)
        else:
            generators = schema

        result = []
        for _ in range(count):
            seed = {}
            for i in range(len(generators)):
                new = generators[i]()
                seed[new[1]] = new[0]
                del new

            result.append(seed)

        self.data = result
        return result

    def to_sql(self, filename: str, table: str) -> str:
        '''
            Export the data to a SQL file

            @param filename: The name of the file to export to
            @param table: The name of the table to export to
            @returns: The path to the exported file
        '''
        if self.data == {}:
            raise FileNotFoundError("No data to export")
        with open(self.format_filename(filename) + '.sql', 'w', encoding='utf-8') as f:
            columns = ', '.join(self.data[0].keys())
            sql_str = f"INSERT INTO {table} ({columns}) VALUES "
            for row in self.data:
                values = ', '.join(f"'{value}'" for value in row.values())
                sql_str += f"({values}), "
            sql_str = sql_str[:-2] + ';'
            f.write(sql_str)

            return os.getcwd() + '/' + filename + '.sql'

    def to_json(self, filename: str) -> str:
        '''
            Export the data to a JSON file

            @param filename: The name of the file to export to
            @returns: The path to the exported file
        '''
        if self.data == {}:
            raise FileNotFoundError("No data to export")
        with open(self.format_filename(filename) + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

            return os.getcwd() + '/' + filename + '.json'

    def to_csv(self, filename: str) -> str:
        '''
            Export the data to a CSV file

            @param filename: The name of the file to export to
            @returns: The path to the exported file
        '''
        if self.data == {}:
            raise FileNotFoundError("No data to export")
        with open(self.format_filename(filename) + '.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.data[0].keys())
            for row in self.data:
                writer.writerow(row.values())

            return os.getcwd() + '/' + filename + '.csv'

    def make_export_dir(self):
        '''
            Create the exports directory if it doesn't exist

            @returns: The path to the exports directory
        '''
        try:
            Path('exports').mkdir(parents=True, exist_ok=True)
            return os.getcwd() + '/exports'
        except Exception as e:
            raise FileNotFoundError("Failed to create exports directory") from e

    def format_filename(self, filename: str) -> str:
        '''
            Format the filename to include the exports directory

            @param filename: The name of the file to format
            @returns: The formatted filename
        '''
        return self.export_path + '/' + filename

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return "Seeder()"

    def schema_to_generators(self, schema_json: List[Dict[str, Any]]) -> List[Any]:
        '''
            Convert a schema to a list of generators

            @param schema_json: The schema to convert to generators
            @returns: A list of generators

            @example [
                {
                    "type": "integer",
                    "name": "id",
                    "min": 1,
                    "max": 100
                },
                {
                    "type": "text",
                    "name": "name",
                    "probability": 50
                },
                {
                    "type": "enum",
                    "name": "status",
                    "choices": ["active", "inactive"],
                    "probability": 50
                },
                {
                    "type": "date",
                    "name": "created_at",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-31",
                    "probability": 50
                },
                {
                    "type": "email",
                    "name": "email",
                    "probability": 50
                }
            ]
        '''
        type_mapping = {
            'integer': Int,
            'text': Text,
            'currency': Currency,
            'enum': Enum,
            'boolean': Bool,
            'string': Text,
            'float': Number,
            'number': Number,
            'date': Date,
            'datetime': Datetime,
            'email': Email,
            'phone': Phone,
            'address': Address,
            'url': Website,
            'id': ID,
            'name': Name,
            'country': Country,
            'state': State,
            'city': City,
            'zip': Zip,
            'time': Time,
            'timestamp': Timestamp,
            'timezone': TimeZone,
            'dayofweek': DayOfWeek,
            'color': Color,
            'jobtitle': JobTitle,
            'department': CompanyDepartment,
            'fileextension': FileExtension,
            'socialmedia': SocialMediaHandle,
            'ipaddress': IPAddress,
            'latlng': LatitudeLongitude,
            'version': Version,
            'sentence': Sentence,
            'paragraph': Paragraph,
            'useragent': UserAgent,
            'hash': Hash,
            'isbn': ISBN,
            'isbn13': ISBN13,
            'ean': EAN,
            'sku': SKU,
            'macaddress': MACAddress,
            'creditcard': CreditCardNumber,
            'iban': IBAN,
            'bic': BIC,
            'null': Null,
            'uuid': UUID,
            'domainname': DomainName,
            'domainword': DomainWord,
            'tld': TLD,
        }

        generators = []
        for field in schema_json:
            field_type = field['type'].lower()
            field_name = field['name']

            if field_type not in type_mapping:
                raise ValueError(f"Unsupported field type: {field_type}")

            generator_class = type_mapping[field_type]
            # Handle special cases with additional parameters
            if field_type == 'currency':
                generators.append(Currency(
                    name=field_name,
                    symbol=field.get('symbol', '$'),
                    min_value=field.get('min_value', 0),
                    max_value=field.get('max_value', 1000)
                ))
            elif field_type == 'integer':
                generators.append(Int(
                    name=field_name,
                    value=random.randint(field.get('min', 1), field.get('max', 99999))
                ))
            elif field_type == 'datetime':
                generators.append(Datetime(
                    name=field_name,
                    start_date=field.get('start_date', '1970-01-01'),
                    end_date=field.get('end_date', 'today'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'timestamp':
                generators.append(Timestamp(
                    name=field_name,
                    start_date=field.get('start_date', '1970-01-01'),
                    end_date=field.get('end_date', 'today'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'color':
                generators.append(Color(
                    name=field_name,
                    color_type=field.get('color_type', 'name'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'version':
                generators.append(Version(
                    name=field_name,
                    major_min=field.get('major_min', 0),
                    major_max=field.get('major_max', 10),
                    minor_min=field.get('minor_min', 0),
                    minor_max=field.get('minor_max', 10),
                    patch_min=field.get('patch_min', 0),
                    patch_max=field.get('patch_max', 10),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'sentence':
                generators.append(Sentence(
                    name=field_name,
                    nb_words=field.get('nb_words', 6),
                    variable_nb_words=field.get('variable_nb_words', 6),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'paragraph':
                generators.append(Paragraph(
                    name=field_name,
                    nb_sentences=field.get('nb_sentences', 3),
                    variable_nb_sentences=field.get('variable_nb_sentences', 3),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'hash':
                generators.append(Hash(
                    name=field_name,
                    hash_type=field.get('hash_type', 'sha256'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'creditcard':
                generators.append(CreditCardNumber(
                    name=field_name,
                    card_type=field.get('card_type', 'visa'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'iban':
                generators.append(IBAN(
                    name=field_name,
                    country_code=field.get('country_code'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'sku':
                generators.append(SKU(
                    name=field_name,
                    prefix=field.get('prefix', ''),
                    length=field.get('length', 8),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'socialmedia':
                generators.append(SocialMediaHandle(
                    name=field_name,
                    platform=field.get('platform'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'ipaddress':
                generators.append(IPAddress(
                    name=field_name,
                    version=field.get('version', 'ipv4'),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'enum':
                generators.append(Enum(
                    name=field_name,
                    choices=field.get('choices', []),
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'latlng':
                generators.append(LatitudeLongitude(
                    name=field_name,
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'timezone':
                generators.append(TimeZone(
                    name=field_name,
                    probability=field.get('probability', 100)
                ))
            elif field_type == 'user_agent':
                generators.append(UserAgent(
                    name=field_name,
                    probability=field.get('probability', 100)
                ))
            else:
                # For simple types that only need name parameter
                generators.append(generator_class(name=field_name))

        return generators
