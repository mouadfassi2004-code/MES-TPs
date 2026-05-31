from dataclasses import dataclass, field
from typing import List

from models import SensorReading, ValidationError


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
        }


class Validator:
    def validate(self, reading: SensorReading) -> List[ValidationError]:
        raise NotImplementedError


class RequiredFieldsValidator(Validator):
    def validate(self, reading: SensorReading) -> List[ValidationError]:
        errors = []

        required_fields = {
            "timestamp": reading.timestamp,
            "site_id": reading.site_id,
            "sensor_id": reading.sensor_id,
        }

        for field_name, value in required_fields.items():
            if value is None or (isinstance(value, str) and value.strip() == ""):
                errors.append(
                    ValidationError(
                        field=field_name,
                        code="MISSING",
                        message=f"Le champ '{field_name}' est obligatoire."
                    )
                )

        return errors


class RangeValidator(Validator):
    def validate(self, reading: SensorReading) -> List[ValidationError]:
        errors = []

        if not (-50.0 <= reading.temperature_c <= 60.0):
            errors.append(
                ValidationError(
                    field="temperature_c",
                    code="OUT_OF_RANGE",
                    message=f"temperature_c hors plage [-50, 60] : {reading.temperature_c}"
                )
            )

        if not (0.0 <= reading.humidity_pct <= 100.0):
            errors.append(
                ValidationError(
                    field="humidity_pct",
                    code="OUT_OF_RANGE",
                    message=f"humidity_pct hors plage [0, 100] : {reading.humidity_pct}"
                )
            )

        if reading.soil_moisture is not None and not (0.0 <= reading.soil_moisture <= 1.0):
            errors.append(
                ValidationError(
                    field="soil_moisture",
                    code="OUT_OF_RANGE",
                    message=f"soil_moisture hors plage [0, 1] : {reading.soil_moisture}"
                )
            )

        if reading.irrigation_l_min < 0.0:
            errors.append(
                ValidationError(
                    field="irrigation_l_min",
                    code="OUT_OF_RANGE",
                    message=f"irrigation_l_min doit être >= 0 : {reading.irrigation_l_min}"
                )
            )

        return errors


class ConsistencyValidator(Validator):
    def validate(self, reading: SensorReading) -> List[ValidationError]:
        errors = []

        pump = str(reading.pump_status).strip().lower()

        if pump not in {"on", "off"}:
            errors.append(
                ValidationError(
                    field="pump_status",
                    code="INVALID_VALUE",
                    message=f"pump_status invalide : {reading.pump_status}"
                )
            )

        if pump == "on" and reading.irrigation_l_min <= 0:
            errors.append(
                ValidationError(
                    field="irrigation_l_min",
                    code="INCONSISTENT",
                    message="Si pump_status == 'on', irrigation_l_min doit être > 0."
                )
            )

        if pump == "off" and reading.irrigation_l_min > 0:
            errors.append(
                ValidationError(
                    field="irrigation_l_min",
                    code="INCONSISTENT",
                    message="Si pump_status == 'off', irrigation_l_min doit être 0."
                )
            )

        return errors


def run_validators(reading: SensorReading, validators: List[Validator]) -> ValidationResult:
    errors = []
    for validator in validators:
        errors.extend(validator.validate(reading))

    return ValidationResult(
        is_valid=(len(errors) == 0),
        errors=errors,
    )