import json
import httpx
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("HS2CharEdit Agent")

API_URL = "http://127.0.0.1:5050/api/properties"

def get_property_metadata(key: str) -> Dict[str, Any]:
    """Infers min/max and description based on the key name."""
    meta = {"type": "number", "min": 0, "max": 100, "description": "Generic value (0-100)"}
    
    # Colors
    if "Red" in key or "Green" in key or "Blue" in key or "Shine" in key or "Glow" in key:
        meta = {"type": "color_channel", "min": 0, "max": 255, "description": "Color/Shine channel (0-255)"}
    elif "Alpha" in key:
        meta = {"type": "opacity", "min": 0, "max": 100, "description": "Alpha/Opacity (0-100)"}
    # Hex ID fields (types)
    elif "Type" in key or "ID" in key or "Skin" in key or "Contour" in key:
        meta = {"type": "hex_id", "min": None, "max": None, "description": "Hexadecimal ID string"}
    # Known negative allowed fields
    elif key in ["txt_waistWidth", "txt_pelvisWidth", "txt_areolaDepth", "txt_nippleDepth"]:
        meta = {"type": "body_shape", "min": -100, "max": 100, "description": "Body shape (-100 to 100)"}
    else:
        # Default for body shapes and others
        meta = {"type": "shape_val", "min": -100, "max": 100, "description": "Shape or positional value (-100 to 100)"}
        
    return meta

def validate_value(key: str, value: str) -> tuple[bool, str]:
    """Validates a value against the schema."""
    meta = get_property_metadata(key)
    
    if meta["type"] == "hex_id":
        return True, ""
        
    try:
        num = float(value)
    except ValueError:
        return False, f"Value '{value}' is not a valid number."
        
    if meta["min"] is not None and num < meta["min"]:
        return False, f"Value {num} is below the minimum of {meta['min']}."
    if meta["max"] is not None and num > meta["max"]:
        return False, f"Value {num} is above the maximum of {meta['max']}."
        
    return True, ""

@mcp.tool()
def get_schema(property_name: str = None) -> str:
    """Returns the constraints (min, max, description) for a specific property, or for all properties if None."""
    try:
        response = httpx.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if property_name:
                if property_name in data:
                    return json.dumps({property_name: get_property_metadata(property_name)}, indent=4)
                return f"Property {property_name} not found."
            
            schema = {k: get_property_metadata(k) for k in data.keys()}
            return json.dumps(schema, indent=4)
        return f"Failed to get properties: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error connecting to HS2CharEdit app: {e}"

@mcp.tool()
def get_all_properties() -> str:
    """Returns a summary of all editable character properties directly from the active HS2CharEdit application."""
    try:
        response = httpx.get(API_URL)
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4)
        return f"Failed to get properties: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error connecting to HS2CharEdit app (is it running?): {e}"

@mcp.tool()
def get_property(property_name: str) -> str:
    """Gets a specific character property value directly from the active application."""
    try:
        response = httpx.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if property_name in data:
                return f"{property_name}: {data[property_name]}"
            return f"Property {property_name} not found."
        return f"Failed to get properties: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error connecting to HS2CharEdit app: {e}"

@mcp.tool()
def set_property(property_name: str, value: str) -> str:
    """Sets a specific character property value. Validates bounds before applying."""
    is_valid, error_msg = validate_value(property_name, value)
    if not is_valid:
        return f"Validation Error for {property_name}: {error_msg}"
        
    try:
        response = httpx.post(API_URL, json={property_name: str(value)}, timeout=30.0)
        if response.status_code == 200:
            return f"Changed {property_name} to {value}."
        return f"Failed to set property: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error connecting to HS2CharEdit app: {e}"

@mcp.tool()
def bulk_update_properties(updates: dict) -> str:
    """Bulk update multiple properties at once. Validates all bounds before applying."""
    valid_updates = {}
    errors = []
    
    for key, val in updates.items():
        is_valid, error_msg = validate_value(key, str(val))
        if is_valid:
            valid_updates[key] = str(val)
        else:
            errors.append(f"{key}: {error_msg}")
            
    if not valid_updates:
        return f"No properties were updated due to validation errors:\n" + "\n".join(errors)
        
    try:
        response = httpx.post(API_URL, json=valid_updates, timeout=60.0)
        if response.status_code == 200:
            res_msg = f"Bulk updated {len(valid_updates)} properties successfully."
            if errors:
                res_msg += "\nHowever, the following were rejected due to limits:\n" + "\n".join(errors)
            return res_msg
        return f"Failed to bulk update: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error connecting to HS2CharEdit app: {e}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
