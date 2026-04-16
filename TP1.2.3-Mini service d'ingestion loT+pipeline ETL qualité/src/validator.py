from datetime import datetime


def parse_datetime(value: str):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def normalize_irrigation(value):
    if value is None:
        return None
    v = str(value).strip().upper()
    mapping = {
        "ON": "ON",
        "OFF": "OFF",
        "OUI": "ON",
        "NON": "OFF",
        "TRUE": "ON",
        "FALSE": "OFF",
        "1": "ON",
        "0": "OFF"
    }
    return mapping.get(v)


def validate_message(data: dict):
    errors = []
    normalized = data.copy()

    required_fields = [
        "request_id", "sensor_id", "site_id",
        "timestamp", "temperature", "humidity", "irrigation"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            errors.append(f"Missing or empty field: {field}")

    if errors:
        return False, errors, normalized

    dt = parse_datetime(str(data["timestamp"]))
    if not dt:
        errors.append("Invalid timestamp format")
    else:
        normalized["timestamp"] = dt.isoformat(sep=" ")

    try:
        normalized["temperature"] = float(data["temperature"])
        if normalized["temperature"] < -50 or normalized["temperature"] > 70:
            errors.append("Temperature out of realistic range")
    except Exception:
        errors.append("Temperature must be convertible to float")

    try:
        normalized["humidity"] = float(data["humidity"])
        if normalized["humidity"] < 0 or normalized["humidity"] > 100:
            errors.append("Humidity must be between 0 and 100")
    except Exception:
        errors.append("Humidity must be convertible to float")

    irrigation = normalize_irrigation(data["irrigation"])
    if irrigation is None:
        errors.append("Invalid irrigation value")
    else:
        normalized["irrigation"] = irrigation

    optional_numeric_fields = ["pm25", "pm10", "ozone", "no2", "battery"]
    for field in optional_numeric_fields:
        if field in data and data[field] not in [None, ""]:
            try:
                normalized[field] = float(data[field])
            except Exception:
                errors.append(f"{field} must be convertible to float")
        else:
            normalized[field] = None

    if normalized.get("battery") is not None:
        if normalized["battery"] < 0 or normalized["battery"] > 100:
            errors.append("Battery must be between 0 and 100")

    return len(errors) == 0, errors, normalized