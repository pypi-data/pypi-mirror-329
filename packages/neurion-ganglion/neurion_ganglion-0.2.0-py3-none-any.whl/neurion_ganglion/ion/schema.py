import json
from pydantic import BaseModel

def compact_json(json_str: str) -> str:
    """
    Compact a JSON string by removing extra spaces and newlines.

    Args:
        json_str (str): The JSON string to be compacted.

    Returns:
        str: The compacted JSON string.
    """
    try:
        parsed_json = json.loads(json_str)  # Parse JSON string
        return json.dumps(parsed_json, separators=(",", ":"))  # Compact and return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None  # Return None if input is invalid JSON

def convert_field(field_schema, schema_defs=None):
    """Convert a Pydantic schema field into the required output format."""
    if not field_schema:
        return "unknown"

    # Handle arrays FIRST before type checks
    if "type" in field_schema and field_schema["type"] == "array":
        item_schema = field_schema["items"]

        # If the array items reference another definition
        if isinstance(item_schema, dict) and "$ref" in item_schema:
            ref_key = item_schema["$ref"].split("/")[-1]
            if schema_defs and ref_key in schema_defs:
                return [process_properties(schema_defs[ref_key].get("properties", {}), schema_defs)]

        # If the array items are a direct object
        elif isinstance(item_schema, dict) and "properties" in item_schema:
            return [{key: convert_field(value, schema_defs) for key, value in item_schema["properties"].items()}]

        # If the array items are a primitive type
        elif isinstance(item_schema, dict) and "type" in item_schema:
            return [convert_field(item_schema, schema_defs)]

        return ["unknown"]

    # Handle object references (`$ref`)
    if "$ref" in field_schema:
        ref_key = field_schema["$ref"].split("/")[-1]
        if schema_defs and ref_key in schema_defs:
            return process_properties(schema_defs[ref_key].get("properties", {}), schema_defs)

    # Process explicitly defined dictionary objects (like `Telephone`)
    if "properties" in field_schema:
        return process_properties(field_schema["properties"], schema_defs)

    # Process basic types AFTER checking for arrays and objects
    if "type" in field_schema:
        if field_schema["type"] == "integer":
            return "int"
        if field_schema["type"] == "number":
            return "float"
        if field_schema["type"] == "string":
            if field_schema.get("format") == "binary":
                return "bytes"  # Properly classify bytes fields
            return "string"
        return field_schema["type"]

    return "unknown"


def process_properties(properties, schema_defs=None):
    """Process object properties recursively to extract types correctly."""
    processed = {}
    for key, value in properties.items():
        field_type = convert_field(value, schema_defs)

        # Ensure dictionaries (nested objects) are fully expanded
        if isinstance(field_type, dict):
            processed[key] = field_type
        elif isinstance(field_type, list) and isinstance(field_type[0], dict):
            processed[key] = field_type  # Handles nested lists properly
        else:
            processed[key] = field_type  # Primitive types or unknown values

    return processed


def pydantic_to_custom_schema(model: BaseModel):
    """Convert a Pydantic model's JSON schema to the required output format."""
    model_schema = model.model_json_schema()
    definitions = model_schema.get("$defs", {})  # Extract references if any
    properties = model_schema.get("properties", {})

    return json.dumps(process_properties(properties, definitions), indent=4)

def schema_string_for_model(model: BaseModel)->str:
    """Convert a Pydantic model to a JSON schema string."""
    return compact_json(pydantic_to_custom_schema(model))
