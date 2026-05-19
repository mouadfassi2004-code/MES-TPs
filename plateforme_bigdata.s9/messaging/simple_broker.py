from pathlib import Path
from typing import Any
from config import BROKER_DIR
from utils.storage import append_jsonl, read_jsonl, write_json, read_json

class SimpleBroker:
    """
    Broker local simplifié.
    Chaque topic est un fichier JSONL.
    L'offset est l'index de la ligne dans le fichier.
    """

    def __init__(self, base_dir: Path = BROKER_DIR):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def topic_path(self, topic: str) -> Path:
        return self.base_dir / f"{topic}.jsonl"

    def checkpoint_path(self, consumer_group: str, topic: str) -> Path:
        safe_topic = topic.replace(".", "_")
        return self.base_dir / "offsets" / f"{consumer_group}_{safe_topic}.json"

    def publish(self, topic: str, event: dict[str, Any]) -> int:
        path = self.topic_path(topic)
        offset = len(read_jsonl(path))

        record = {
            "offset": offset,
            "topic": topic,
            "value": event,
        }

        append_jsonl(path, record)
        return offset

    def consume(
        self,
        topic: str,
        consumer_group: str,
        max_events: int = 100,
    ) -> list[dict[str, Any]]:
        path = self.topic_path(topic)
        rows = read_jsonl(path)

        checkpoint = read_json(
            self.checkpoint_path(consumer_group, topic),
            {"next_offset": 0},
        )

        next_offset = checkpoint["next_offset"]

        return [
            row for row in rows
            if row["offset"] >= next_offset
        ][:max_events]

    def commit(self, topic: str, consumer_group: str, offset: int) -> None:
        write_json(
            self.checkpoint_path(consumer_group, topic),
            {"next_offset": offset + 1},
        )