import os
import numpy as np
import pandas as pd

from src.config import (
    DATA_FILE,
    CLEANED_FILE,
    ENRICHED_FILE,
    QUALITY_REPORT_FILE,
    ETL_LOG_FILE
)
from src.logger_setup import setup_logger


logger = setup_logger("etl_logger", ETL_LOG_FILE)


def detect_outliers_iqr(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series < lower) | (series > upper)


def run_etl():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print("No accepted data found.")
        return

    logger.info("ETL started")

    df = pd.read_json(DATA_FILE, lines=True)
    logger.info(f"Loaded rows: {len(df)}")

    initial_rows = len(df)
    missing_before = df.isna().sum().to_dict()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df = df.drop_duplicates(subset=["request_id"])
    logger.info(f"Rows after dropping duplicate request_id: {len(df)}")

    for col in ["temperature", "humidity", "pm25", "pm10", "ozone", "no2", "battery"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "temperature" in df.columns:
        df["temperature"] = df["temperature"].fillna(df["temperature"].median())
    if "humidity" in df.columns:
        df["humidity"] = df["humidity"].fillna(df["humidity"].median())
    if "battery" in df.columns:
        df["battery"] = df["battery"].fillna(df["battery"].median())

    if "irrigation" in df.columns:
        df["irrigation"] = df["irrigation"].fillna("OFF")

    outlier_counts = {}
    for col in ["temperature", "humidity"]:
        if col in df.columns:
            mask = detect_outliers_iqr(df[col].dropna())
            aligned_mask = df[col].isin(df[col].dropna()[mask])
            outlier_counts[col] = int(aligned_mask.sum())
            df.loc[aligned_mask, col] = df[col].median()

    df["hour"] = df["timestamp"].dt.hour
    df["comfort_index"] = df["temperature"] - ((100 - df["humidity"]) / 5.0)

    if "battery" in df.columns:
        df["battery_status"] = np.where(df["battery"] < 20, "LOW", "OK")
    else:
        df["battery_status"] = "UNKNOWN"

    os.makedirs("outputs", exist_ok=True)

    df.to_csv(CLEANED_FILE, index=False)
    logger.info(f"Saved cleaned data to {CLEANED_FILE}")

    df.to_csv(ENRICHED_FILE, index=False)
    logger.info(f"Saved enriched data to {ENRICHED_FILE}")

    missing_after = df.isna().sum().to_dict()

    with open(QUALITY_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("QUALITY REPORT\n")
        f.write("====================\n\n")
        f.write(f"Initial rows: {initial_rows}\n")
        f.write(f"Final rows: {len(df)}\n\n")
        f.write("Missing values before cleaning:\n")
        for k, v in missing_before.items():
            f.write(f"- {k}: {v}\n")
        f.write("\nMissing values after cleaning:\n")
        for k, v in missing_after.items():
            f.write(f"- {k}: {v}\n")
        f.write("\nOutliers handled:\n")
        for k, v in outlier_counts.items():
            f.write(f"- {k}: {v}\n")
        f.write("\nFeatures created:\n")
        f.write("- hour\n")
        f.write("- comfort_index\n")
        f.write("- battery_status\n")

    logger.info("Quality report generated")
    logger.info("ETL finished")
    print("ETL completed successfully.")