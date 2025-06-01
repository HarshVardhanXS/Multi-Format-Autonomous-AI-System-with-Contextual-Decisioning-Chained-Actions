import json
import os
from datetime import datetime
from memory.memory_store import write_to_memory

REQUIRED_SCHEMA = {
    "event_type": str,
    "timestamp": str,
    "user_id": int,
    "payload": dict
}

def validate_json(data):
    anomalies = []

    for key, expected_type in REQUIRED_SCHEMA.items():
        if key not in data:
            anomalies.append(f"Missing required field: '{key}'")
        elif not isinstance(data[key], expected_type):
            anomalies.append(
                f"Type mismatch for '{key}': expected {expected_type.__name__}, got {type(data[key]).__name__}"
            )

    return anomalies

def process_json_webhook(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return {"error": f"Invalid JSON: {e}"}

    anomalies = validate_json(data)

    result = {
        "source": os.path.basename(file_path),
        "timestamp": datetime.now().isoformat(),
        "status": "anomalies_detected" if anomalies else "valid",
        "anomalies": anomalies,
        "data": data
    }

    write_to_memory(result)

    print("\n📩 JSON Agent Output:")
    for k, v in result.items():
        print(f"{k}: {v}")

    if anomalies:
        print("🚨 Anomalies found and logged.")
    else:
        print("✅ JSON schema validated successfully.")

    return result
