import json
def recursive_json_decode(obj):
        """Recursively check if values are JSON strings and decode them."""
        if isinstance(obj, dict):  # If obj is a dictionary, process each key-value pair
            for key, value in obj.items():
                if isinstance(value, str):
                    try:
                        decoded_value = json.loads(value)  # Try decoding JSON
                        obj[key] = recursive_json_decode(decoded_value)  # Recursively decode
                    except json.JSONDecodeError:
                        pass  # If decoding fails, keep original value
                elif isinstance(value, dict) or isinstance(value, list):
                    obj[key] = recursive_json_decode(value)  # Process nested dict or list
        elif isinstance(obj, list):  # If obj is a list, process each element
            for i in range(len(obj)):
                if isinstance(obj[i], str):
                    try:
                        decoded_value = json.loads(obj[i])  # Try decoding JSON
                        obj[i] = recursive_json_decode(decoded_value)  # Recursively decode
                    except json.JSONDecodeError:
                        pass  # If decoding fails, keep original value
                elif isinstance(obj[i], dict) or isinstance(obj[i], list):
                    obj[i] = recursive_json_decode(obj[i])  # Process nested dict or list
        return obj  # Return fully decoded object