import re
import pandas as pd

def sanitize_value(value):
    if pd.isna(value):
        return ''
    return value

def sanitize_and_filter_properties(row, fields):
    """Helper function to sanitize and filter properties."""
    return {field: sanitize_value(row.get(field)) for field in fields if sanitize_value(row.get(field))}

def add_phone_to_properties(row, phone_key, properties):
    """Sanitize, repair, and validate phone number, then add to properties."""
    phone = str(sanitize_value(row.get(phone_key, None)))
    repaired_phone = repair_phone(phone)
    if validate_phone(repaired_phone):
        properties[phone_key] = repaired_phone

def sanitize_and_add_fields(row, field_names, destination, sanitizer=sanitize_value):
    """Sanitize specified fields from row and add them to destination."""
    for field in field_names:
        value = sanitizer(row.get(field, None))
        if value:
            destination[field.lower()] = value

def validate_name(name: str) -> bool:
    """
    Validate the name field.
    - Name must be a string.
    - Name must be between 2 and 100 characters.
    - Name must not contain digits.
    - Allowed characters: letters, spaces, and hyphens.
    """
    if not isinstance(name, str):
        return False
    if not (2 <= len(name) <= 100):
        return False
    if any(char.isdigit() for char in name):
        return False
    if not all(char.isalpha() or char.isspace() or char == '-' for char in name):
        return False
    return True

def validate_phone(phone: str) -> bool:
    """
    Checks the validity of the entered phone number.

    :param phone: Phone number in string format.
    :return: True if the number is valid, otherwise False.
    """
    # Check that the input value is a string
    if not isinstance(phone, str):
        return False

    # Define a template for the phone
    phone_pattern = re.compile(r"^\+?[0-9\-\s()]{7,15}$")

    # Check if the number matches the pattern
    return bool(phone_pattern.match(phone))


def repair_phone(input_phone):
    """
    Repairs a phone number string to match the expected format: +380660132486.

    Parameters:
        phone (str): The input phone number as a string.

    Returns:
        str: The repaired phone number or None if input is invalid.
    """
    if not isinstance(input_phone, str):
        return None  # Return None if the input is not a string

    # Remove all non-digit characters except the '+' at the start
    phone = re.sub(r'[^\d+]', '', input_phone)

    # Add '+' at the beginning if it's missing
    if not phone.startswith('+'):
        phone = '+' + phone

    # Validate the result: Ensure it starts with '+' and only contains digits afterward
    if not re.fullmatch(r'\+\d+', phone):
        return None  # Invalid phone number format

    return phone