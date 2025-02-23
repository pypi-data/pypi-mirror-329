import copy
import csv
from io import StringIO
import json
from typing import AsyncGenerator
import aiohttp
from salesmanago_toolkit.utils.util_funcs import repair_phone, sanitize_and_add_fields, sanitize_value, validate_name, validate_phone


async def get_file(url: str) -> bytes:
    """Downloading a file from the specified URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(detail="Failed to upload file")
            return await response.read()


async def process_data_to_csv(
    content: bytes, logger, without_phone: bool = False,
) -> AsyncGenerator[str, None]:
    """Processing the file settings and creating a CSV file as strings."""
    try:
        data = json.loads(content.decode("utf-8"))
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["email", "domain", "first_name", "last_name"])  # Заголовки CSV

        for item in data:
            for contact_id, contact_info in item.items():
                logger.info(f"CONTACT_INFO: {contact_info}")
                phone = contact_info["contactData"].get("phone", "")
                if without_phone and phone:
                    logger.info(f"PHONE FOUND: {phone}")
                    continue
                email = contact_info["contactData"].get("email", "")
                domain = (contact_info["contactData"].get("email", "")).split("@")[1]
                first_name = (contact_info["contactData"].get("name", "")).split()[0]
                last_name = " ".join(
                    (contact_info["contactData"].get("name", "")).split()[1:]
                )
                writer.writerow([email, domain, first_name, last_name])

        # Вернуться в начало буфера
        csv_buffer.seek(0)
        yield csv_buffer.getvalue()
    except json.JSONDecodeError:
        raise ValueError("JSON decoding error")


async def create_import_payload(row, tags, logger):
    """Helper function to create import payload."""
    tags = copy.deepcopy(tags)
    logger.info(f"TAGS IN create_import_payload: {tags}")

    email = sanitize_value(row.get("Email"))
    contact_payload = {"email": email}
    address = {}

    # Validate phone and add tags
    processed_phone = str(sanitize_value(row.get("Phone", None)))
    repaired_phone = repair_phone(processed_phone)
    if validate_phone(repaired_phone):
        logger.info(f"PHONE VALIDATED: {repaired_phone}")
        contact_payload["phone"] = repaired_phone
        tags.append("COGNISM_PHONE")
    else:
        logger.info(
            f"PHONE DID NOT VALIDATE. INPUT PHONE FROM FILE {processed_phone}. PHONE AFTER REPAIR FUNCTION: {repaired_phone}",
        )
        tags.append("COGNISM_NO_PHONE")
    logger.info(f"TAGS AFTER PHONE VALIDATION: {tags}")

    # Address fields
    sanitize_and_add_fields(row, ["Country", "City"], address)
    if address:
        contact_payload["address"] = address

    # Optional name field
    name = sanitize_value(row.get("Name", None))
    if name and validate_name(name):
        contact_payload["name"] = name
    else:
        logger.info(f"Invalid name: {name}")

    # Properties
    properties = row.get("properties", {})

    logger.info(f"ROW: {row}")

    # Upsert payload
    upsert_payload = {
        "contact": contact_payload,
        "newEmail": email,
        "forceOptIn": True,
        "forceOptOut": False,
        "forcePhoneOptIn": True,
        "forcePhoneOptOut": False,
        "tags": tags,
        "properties": properties,
    }

    logger.info(f"UPSERT DATA: {upsert_payload}")
    
    return {"upsertDetails": [upsert_payload]}