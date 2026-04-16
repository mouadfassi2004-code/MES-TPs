from typing import List
from models import SensorReading, ValidationError


def validate_reading(reading: SensorReading) -> List[ValidationError]:
    errors: List[ValidationError] = []

    if not reading.sensor_id.strip():
        errors.append(
            ValidationError(
                field="sensor_id",
                code="MISSING",
                message="sensor_id est obligatoire"
            )
        )

    if not reading.timestamp.strip():
        errors.append(
            ValidationError(
                field="timestamp",
                code="MISSING",
                message="timestamp est obligatoire"
            )
        )

    if reading.type not in {"temperature", "humidity", "rainfall", "irrigation"}:
        errors.append(
            ValidationError(
                field="type",
                code="INVALID_TYPE",
                message=f"type invalide : {reading.type}"
            )
        )

    if reading.type == "temperature":
        if not (-50.0 <= reading.value <= 60.0):
            errors.append(
                ValidationError(
                    field="value",
                    code="OUT_OF_RANGE",
                    message=f"température hors plage [-50, 60] : {reading.value}"
                )
            )
        if reading.unit != "°C":
            errors.append(
                ValidationError(
                    field="unit",
                    code="INVALID_UNIT",
                    message="temperature doit être en °C"
                )
            )

    elif reading.type == "humidity":
        if not (0.0 <= reading.value <= 100.0):
            errors.append(
                ValidationError(
                    field="value",
                    code="OUT_OF_RANGE",
                    message=f"humidité hors plage [0,100] : {reading.value}"
                )
            )
        if reading.unit != "%":
            errors.append(
                ValidationError(
                    field="unit",
                    code="INVALID_UNIT",
                    message="humidity doit être en %"
                )
            )

    elif reading.type == "rainfall":
        if reading.value < 0:
            errors.append(
                ValidationError(
                    field="value",
                    code="OUT_OF_RANGE",
                    message=f"rainfall doit être >= 0 : {reading.value}"
                )
            )
        if reading.unit != "mm":
            errors.append(
                ValidationError(
                    field="unit",
                    code="INVALID_UNIT",
                    message="rainfall doit être en mm"
                )
            )

    elif reading.type == "irrigation":
        if reading.value < 0:
            errors.append(
                ValidationError(
                    field="value",
                    code="OUT_OF_RANGE",
                    message=f"irrigation doit être >= 0 : {reading.value}"
                )
            )
        if reading.unit != "mm":
            errors.append(
                ValidationError(
                    field="unit",
                    code="INVALID_UNIT",
                    message="irrigation doit être en mm"
                )
            )

        pump = (reading.pump_status or "").lower().strip()
        irrigation_mm = reading.irrigation_mm if reading.irrigation_mm is not None else 0.0

        if pump not in {"on", "off"}:
            errors.append(
                ValidationError(
                    field="pump_status",
                    code="INVALID_VALUE",
                    message=f"pump_status invalide : {reading.pump_status}"
                )
            )
        elif pump == "on" and irrigation_mm <= 0:
            errors.append(
                ValidationError(
                    field="irrigation_mm",
                    code="INCONSISTENT",
                    message="si pump_status == on, irrigation_mm doit être > 0"
                )
            )

    return errors