"""Mini-pipeline ETL pour le TP1 : Station météo & irrigation.

Étapes :
1. Extraction du CSV brut.
2. Nettoyage et standardisation des données.
3. Génération d'un rapport de qualité.
4. Feature engineering vectorisé.
5. Export des fichiers CSV et journalisation dans logs/pipeline.log.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd


CONFIG: Dict[str, object] = {
    "input_path": "data/raw/meteo_brut.csv",
    "output_clean": "outputs/meteo_clean.csv",
    "output_features": "outputs/meteo_features.csv",
    "output_report": "outputs/quality_report.txt",
    "log_file": "logs/pipeline.log",
    "temp_min": -40,
    "temp_max": 60,
    "humidity_min": 0,
    "humidity_max": 100,
    "irrigation_map": {"ON": "ON", "OFF": "OFF", "OUI": "ON"},
}

logger = logging.getLogger("meteo_pipeline")


def setup_logging(log_file: str) -> None:
    """Configure les logs dans un fichier et dans la console."""
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def extract(filepath: str) -> pd.DataFrame:
    """Lit le fichier CSV brut."""
    try:
        df = pd.read_csv(filepath)
        logger.info(
            "EXTRACT : %d lignes et %d colonnes lues depuis %s",
            len(df),
            len(df.columns),
            filepath,
        )
        return df
    except FileNotFoundError:
        logger.critical("EXTRACT : fichier introuvable : %s", filepath)
        raise
    except pd.errors.ParserError as exc:
        logger.critical("EXTRACT : erreur de parsing CSV : %s", exc)
        raise


def parse_dates(date_series: pd.Series) -> pd.Series:
    """Parse deux formats de date : yyyy-mm-dd et dd/mm/yyyy."""
    as_text = date_series.astype("string").str.strip()

    iso_dates = pd.to_datetime(as_text, format="%Y-%m-%d", errors="coerce")
    european_dates = pd.to_datetime(as_text, format="%d/%m/%Y", errors="coerce")

    return iso_dates.fillna(european_dates)


def detect_outliers_iqr(series: pd.Series, factor: float = 1.5) -> pd.Series:
    """Retourne un masque True pour les outliers détectés par la méthode IQR."""
    clean_series = series.dropna()

    if clean_series.empty:
        return pd.Series(False, index=series.index)

    q1 = clean_series.quantile(0.25)
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - factor * iqr
    upper = q3 + factor * iqr

    return (series < lower) | (series > upper)


def transform(df: pd.DataFrame, config: Dict[str, object]) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Nettoie et standardise les données météo.

    Décisions appliquées :
    - standardisation des stations en majuscules ;
    - conversion des colonnes numériques avec errors='coerce' ;
    - dates invalides supprimées ;
    - doublons supprimés ;
    - valeurs hors domaine remplacées par NaN puis imputées ;
    - outlier de vent traité par IQR puis imputé.
    """

    cleaned = df.copy()

    stats: Dict[str, object] = {
        "rows_initial": len(cleaned),
        "duplicates_removed": 0,
        "invalid_dates_removed": 0,
        "numeric_coercions": {},
        "domain_invalid": {},
        "wind_outliers": 0,
        "imputations": {},
    }

    logger.info("TRANSFORM : début du nettoyage")

    # 1. Normalisation des champs texte
    cleaned["station"] = cleaned["station"].astype("string").str.strip().str.upper()

    irrigation_upper = cleaned["irrigation"].astype("string").str.strip().str.upper()
    cleaned["irrigation"] = irrigation_upper.map(config["irrigation_map"])

    invalid_irrigation = int(cleaned["irrigation"].isna().sum())
    if invalid_irrigation:
        logger.warning(
            "TRANSFORM : %d valeur(s) d'irrigation non reconnue(s)",
            invalid_irrigation,
        )
        cleaned["irrigation"] = cleaned["irrigation"].fillna("UNKNOWN")

    # 2. Conversion numérique robuste
    numeric_cols = ["temperature", "humidity", "rain_mm", "wind_kmh"]

    for col in numeric_cols:
        before_na = int(cleaned[col].isna().sum())
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        after_na = int(cleaned[col].isna().sum())

        coerced = max(0, after_na - before_na)
        stats["numeric_coercions"][col] = coerced

        if coerced:
            logger.warning(
                "TRANSFORM : %s contient %d valeur(s) non numérique(s)",
                col,
                coerced,
            )

    # 3. Parsing des dates
    before_nat = int(cleaned["date"].isna().sum())
    cleaned["date"] = parse_dates(cleaned["date"])
    after_nat = int(cleaned["date"].isna().sum())

    created_nat = max(0, after_nat - before_nat)

    if created_nat:
        logger.warning(
            "TRANSFORM : %d date(s) invalide(s) convertie(s) en NaT",
            created_nat,
        )

    # 4. Suppression des doublons exacts après normalisation
    duplicate_cols = [
        "station",
        "date",
        "temperature",
        "humidity",
        "rain_mm",
        "wind_kmh",
        "irrigation",
    ]

    duplicate_count = int(cleaned.duplicated(subset=duplicate_cols).sum())

    if duplicate_count:
        cleaned = cleaned.drop_duplicates(subset=duplicate_cols)
        logger.warning("TRANSFORM : %d doublon(s) supprimé(s)", duplicate_count)

    stats["duplicates_removed"] = duplicate_count

    # 5. Valeurs hors domaine physique
    invalid_temp = (
        ~cleaned["temperature"].between(config["temp_min"], config["temp_max"])
        & cleaned["temperature"].notna()
    )
    stats["domain_invalid"]["temperature"] = int(invalid_temp.sum())
    cleaned.loc[invalid_temp, "temperature"] = np.nan

    invalid_humidity = (
        ~cleaned["humidity"].between(config["humidity_min"], config["humidity_max"])
        & cleaned["humidity"].notna()
    )
    stats["domain_invalid"]["humidity"] = int(invalid_humidity.sum())
    cleaned.loc[invalid_humidity, "humidity"] = np.nan

    if stats["domain_invalid"]["temperature"]:
        logger.warning(
            "TRANSFORM : %d température(s) hors domaine mise(s) à NaN",
            stats["domain_invalid"]["temperature"],
        )

    if stats["domain_invalid"]["humidity"]:
        logger.warning(
            "TRANSFORM : %d humidité(s) hors domaine mise(s) à NaN",
            stats["domain_invalid"]["humidity"],
        )

    # 6. Détection d'outlier sur la vitesse du vent
    wind_outliers = detect_outliers_iqr(cleaned["wind_kmh"])
    stats["wind_outliers"] = int(wind_outliers.sum())

    if stats["wind_outliers"]:
        logger.warning(
            "TRANSFORM : %d outlier(s) détecté(s) dans wind_kmh",
            stats["wind_outliers"],
        )
        cleaned.loc[wind_outliers, "wind_kmh"] = np.nan

    # 7. Suppression des dates invalides ou manquantes
    before_drop_dates = len(cleaned)
    cleaned = cleaned.dropna(subset=["date"])

    stats["invalid_dates_removed"] = before_drop_dates - len(cleaned)

    if stats["invalid_dates_removed"]:
        logger.warning(
            "TRANSFORM : %d ligne(s) supprimée(s) à cause de date invalide/manquante",
            stats["invalid_dates_removed"],
        )

    # 8. Imputation des valeurs manquantes
    temp_missing_before = int(cleaned["temperature"].isna().sum())
    global_temp_median = float(cleaned["temperature"].median())

    cleaned["temperature"] = cleaned.groupby("station")["temperature"].transform(
        lambda s: s.fillna(s.median())
    )
    cleaned["temperature"] = cleaned["temperature"].fillna(global_temp_median)
    stats["imputations"]["temperature"] = temp_missing_before

    humidity_missing_before = int(cleaned["humidity"].isna().sum())
    cleaned["humidity"] = cleaned["humidity"].fillna(float(cleaned["humidity"].median()))
    stats["imputations"]["humidity"] = humidity_missing_before

    rain_missing_before = int(cleaned["rain_mm"].isna().sum())
    cleaned["rain_mm"] = cleaned["rain_mm"].fillna(0.0)
    stats["imputations"]["rain_mm"] = rain_missing_before

    wind_missing_before = int(cleaned["wind_kmh"].isna().sum())
    cleaned["wind_kmh"] = cleaned["wind_kmh"].fillna(float(cleaned["wind_kmh"].median()))
    stats["imputations"]["wind_kmh"] = wind_missing_before

    # 9. Colonnes finales et tri
    cleaned["id"] = cleaned["id"].astype(int)
    cleaned["date"] = cleaned["date"].dt.strftime("%Y-%m-%d")

    cleaned = cleaned[
        [
            "id",
            "station",
            "date",
            "temperature",
            "humidity",
            "rain_mm",
            "wind_kmh",
            "irrigation",
        ]
    ]

    cleaned = cleaned.sort_values(["station", "date", "id"]).reset_index(drop=True)
    stats["rows_final"] = len(cleaned)

    logger.info(
        "TRANSFORM : fin — %d lignes conservées sur %d",
        len(cleaned),
        stats["rows_initial"],
    )

    return cleaned, stats


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Construit des features vectorisées à partir du dataset propre."""
    features = df.copy()

    date_col = pd.to_datetime(features["date"], errors="coerce")

    features["day_of_week"] = date_col.dt.day_name()
    features["is_rainy"] = (features["rain_mm"] > 0).astype(int)
    features["irrigation_binary"] = (features["irrigation"] == "ON").astype(int)

    temp_conditions = [
        features["temperature"] < 15,
        features["temperature"].between(15, 25, inclusive="left"),
        features["temperature"] >= 25,
    ]

    features["temperature_class"] = np.select(
        temp_conditions,
        ["froid", "tempere", "chaud"],
        default="unknown",
    )

    humidity_conditions = [
        features["humidity"] < 40,
        features["humidity"].between(40, 70),
        features["humidity"] > 70,
    ]

    features["humidity_class"] = np.select(
        humidity_conditions,
        ["sec", "normal", "humide"],
        default="unknown",
    )

    # Score simple : plus il fait chaud et sec, plus le besoin d'eau augmente.
    # La pluie réduit le besoin d'eau.
    features["water_need_score"] = (
        features["temperature"] * (100 - features["humidity"]) / 100
        - features["rain_mm"] * 2
    ).round(2)

    logger.info(
        "FEATURES : %d features ajoutées",
        len(set(features.columns) - set(df.columns)),
    )

    return features


def quality_report(
    raw: pd.DataFrame,
    cleaned: pd.DataFrame,
    stats: Dict[str, object],
    output_path: str,
) -> None:
    """Génère un rapport qualité au format texte."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    missing_before = raw.isna().sum().to_dict()
    missing_after = cleaned.isna().sum().to_dict()

    report = []

    report.append("RAPPORT QUALITÉ - TP1 Station météo & irrigation")
    report.append("=" * 60)
    report.append("")

    report.append("1. Dimensions du dataset")
    report.append(f"- Lignes initiales : {stats['rows_initial']}")
    report.append(f"- Lignes finales : {stats['rows_final']}")
    report.append(f"- Colonnes finales : {', '.join(cleaned.columns)}")
    report.append("")

    report.append("2. Problèmes détectés et traitements appliqués")
    report.append(f"- Doublons supprimés : {stats['duplicates_removed']}")
    report.append(
        f"- Lignes supprimées pour date invalide ou manquante : "
        f"{stats['invalid_dates_removed']}"
    )
    report.append(
        f"- Valeurs non numériques converties en NaN : "
        f"{stats['numeric_coercions']}"
    )
    report.append(f"- Valeurs hors domaine : {stats['domain_invalid']}")
    report.append(f"- Outliers wind_kmh détectés par IQR : {stats['wind_outliers']}")
    report.append(f"- Valeurs imputées : {stats['imputations']}")
    report.append("")

    report.append("3. Valeurs manquantes avant nettoyage")
    for col, value in missing_before.items():
        report.append(f"- {col}: {value}")
    report.append("")

    report.append("4. Valeurs manquantes après nettoyage")
    for col, value in missing_after.items():
        report.append(f"- {col}: {value}")
    report.append("")

    report.append("5. Statistiques descriptives après nettoyage")
    report.append(
        cleaned[["temperature", "humidity", "rain_mm", "wind_kmh"]]
        .describe()
        .round(2)
        .to_string()
    )
    report.append("")

    report.append("6. Résumé par station")
    station_summary = (
        cleaned.groupby("station")
        .agg(
            nb_mesures=("id", "count"),
            temperature_moyenne=("temperature", "mean"),
            humidite_moyenne=("humidity", "mean"),
            pluie_totale=("rain_mm", "sum"),
            vent_moyen=("wind_kmh", "mean"),
        )
        .round(2)
    )
    report.append(station_summary.to_string())
    report.append("")

    report.append("7. Conclusion")
    report.append(
        "Le pipeline a produit un dataset propre, un dataset enrichi avec des "
        "features et des logs d'exécution."
    )

    Path(output_path).write_text("\n".join(report), encoding="utf-8")
    logger.info("REPORT : rapport qualité écrit dans %s", output_path)


def load(
    df_clean: pd.DataFrame,
    df_features: pd.DataFrame,
    config: Dict[str, object],
) -> None:
    """Exporte les résultats dans le dossier outputs."""
    Path(str(config["output_clean"])).parent.mkdir(parents=True, exist_ok=True)

    df_clean.to_csv(str(config["output_clean"]), index=False)
    df_features.to_csv(str(config["output_features"]), index=False)

    logger.info("LOAD : fichier clean écrit dans %s", config["output_clean"])
    logger.info("LOAD : fichier features écrit dans %s", config["output_features"])


def run_pipeline(config: Dict[str, object] = CONFIG) -> None:
    """Exécute le pipeline complet."""
    start = time.perf_counter()

    setup_logging(str(config["log_file"]))
    logger.info("PIPELINE : démarrage")

    raw = extract(str(config["input_path"]))
    cleaned, stats = transform(raw, config)

    if cleaned.empty:
        logger.critical("PIPELINE : aucune ligne valide après nettoyage")
        raise ValueError("Aucune ligne valide après nettoyage")

    features = build_features(cleaned)

    load(cleaned, features, config)
    quality_report(raw, cleaned, stats, str(config["output_report"]))

    elapsed = time.perf_counter() - start
    logger.info("PIPELINE : terminé avec succès en %.3f secondes", elapsed)


if __name__ == "__main__":
    run_pipeline()