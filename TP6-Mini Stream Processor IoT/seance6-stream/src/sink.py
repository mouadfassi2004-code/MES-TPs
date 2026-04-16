import csv
import pathlib


def write_csv_rows(path: str, rows: list[dict]):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        if not p.exists():
            p.write_text("", encoding="utf-8")
        return

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)