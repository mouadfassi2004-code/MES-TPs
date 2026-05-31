from processing.batch.bronze_to_silver import (
    clean_orders,
    clean_payments,
    clean_snapshots,
)
from processing.batch.silver_to_gold import compute_daily_report

DAG = {
    "clean_orders": {
        "depends_on": [],
        "function": clean_orders,
    },
    "clean_payments": {
        "depends_on": [],
        "function": clean_payments,
    },
    "clean_snapshots": {
        "depends_on": [],
        "function": clean_snapshots,
    },
    "compute_daily_report": {
        "depends_on": [
            "clean_orders",
            "clean_payments",
            "clean_snapshots",
        ],
        "function": compute_daily_report,
    },
}