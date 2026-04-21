import json
from pathlib import Path
from src.events import Event


class PartitionedStorage:
    def __init__(self, root: str = "outputs"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_event(self, event: Event, partition: int) -> None:
        date_str = event.event_time.split("T")[0]
        path = (
            self.root
            / f"date={date_str}"
            / f"site={event.site_id}"
            / f"partition={partition}"
        )
        path.mkdir(parents=True, exist_ok=True)

        file_path = path / "events.jsonl"
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")