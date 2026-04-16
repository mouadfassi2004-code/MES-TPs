import logging
import os

from pipeline import run_pipeline


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)s] %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


if __name__ == "__main__":
    setup_logging()

    run_pipeline(
        runtime_sec=15,
        num_producers=3,
        num_workers=2,
        queue_maxsize=50,
        csv_path="outputs/valid_readings.csv",
        dead_letter_path="outputs/dead_letters.json",
    )