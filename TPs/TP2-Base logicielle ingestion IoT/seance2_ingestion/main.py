"""main.py — Point d'entrée du service d'ingestion IoT (TP Séance 2)."""

import json
import uuid
from datetime import datetime, timezone

from logger_config import get_logger
from models import SensorReading, IngestRequest, IngestResponse, ValidationError
from validators import (
    Validator,
    RangeValidator,
    ConsistencyValidator,
    RequiredFieldsValidator,
    run_validators,
)

logger = get_logger("ingestion")


def sanitize_for_log(value: str, max_len: int = 200) -> str:
    if value is None:
        return ""
    sanitized = str(value).replace("\n", " ").replace("\r", " ").replace("\t", " ")
    return sanitized[:max_len] + "...[TRONQUÉ]" if len(sanitized) > max_len else sanitized


def mask_api_key(key: str) -> str:
    if not key:
        return "****"
    key = str(key)
    if len(key) <= 4:
        return "****"
    return "****" + key[-4:]


def load_sample_readings(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_request(raw_readings: list[dict]) -> IngestRequest:
    valid_objects = []

    for item in raw_readings:
        try:
            valid_objects.append(SensorReading.from_dict(item))
        except ValueError as e:
            logger.warning(
                "Lecture rejetée au constructeur | sensor_id=%s | erreur=%s",
                sanitize_for_log(item.get("sensor_id", "")),
                sanitize_for_log(str(e)),
            )

    return IngestRequest(
        request_id=str(uuid.uuid4()),
        api_key="sk-abcdef1234",
        readings=valid_objects,
        sent_at=datetime.now(timezone.utc).isoformat(),
    )


def process_request(request: IngestRequest) -> IngestResponse:
    validators: list[Validator] = [
        RequiredFieldsValidator(),
        RangeValidator(),
        ConsistencyValidator(),
    ]

    all_errors: list[ValidationError] = []
    accepted_count = 0
    rejected_count = 0

    logger.info(
        "Début traitement request_id=%s | api_key=%s | nb_readings=%d",
        request.request_id,
        mask_api_key(request.api_key),
        len(request.readings),
    )

    for reading in request.readings:
        result = run_validators(reading, validators)

        if result.is_valid:
            accepted_count += 1
            logger.info(
                "Lecture acceptée | request_id=%s | sensor_id=%s | site_id=%s",
                request.request_id,
                sanitize_for_log(reading.sensor_id),
                sanitize_for_log(reading.site_id),
            )
        else:
            rejected_count += 1
            all_errors.extend(result.errors)
            logger.warning(
                "Lecture rejetée | request_id=%s | sensor_id=%s | nb_erreurs=%d",
                request.request_id,
                sanitize_for_log(reading.sensor_id),
                len(result.errors),
            )
            for err in result.errors:
                logger.warning(
                    "Erreur validation | field=%s | code=%s | msg=%s",
                    sanitize_for_log(err.field),
                    sanitize_for_log(err.code),
                    sanitize_for_log(err.message),
                )

    if rejected_count == 0:
        status = "ok"
    elif accepted_count > 0:
        status = "partial"
    else:
        status = "error"

    return IngestResponse(
        status=status,
        accepted_count=accepted_count,
        rejected_count=rejected_count,
        errors=all_errors,
    )


def main():
    raw_readings = load_sample_readings("data/sample_readings.json")

    request = build_request(raw_readings)
    response = process_request(request)

    logger.info("Réponse finale : %s", response.to_dict())

    reading_ok = SensorReading(
        timestamp="2026-02-16T08:00:00Z",
        site_id="site-alpha",
        sensor_id="sensor-test",
        temperature_c=22.0,
        humidity_pct=60.0,
        soil_moisture=0.4,
        pump_status="off",
        irrigation_l_min=0.0,
    )
    reading_roundtrip = SensorReading.from_dict(reading_ok.to_dict())
    assert reading_ok.to_dict() == reading_roundtrip.to_dict()

    ok = False
    try:
        SensorReading(
            timestamp="2026-02-16T08:00:00Z",
            site_id="site-x",
            sensor_id="",
            temperature_c=20.0,
            humidity_pct=50.0,
        )
    except ValueError:
        ok = True
    assert ok

    second = SensorReading.from_dict(raw_readings[1])
    result_second = run_validators(
        second,
        [RequiredFieldsValidator(), RangeValidator(), ConsistencyValidator()],
    )
    assert any(err.code == "OUT_OF_RANGE" for err in result_second.errors)

    assert mask_api_key("sk-abcdef1234") == "****1234"

    logger.info("Tous les asserts de vérification sont passés avec succès.")


if __name__ == "__main__":
    main()