import json
from pathlib import Path


class OffsetStore:
    def __init__(self, path: str = "state/offsets.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {}

    def get(self, group: str, partition: int) -> int:
        return self._data.get(group, {}).get(str(partition), 0)

    def commit(self, group: str, partition: int, offset: int) -> None:
        self._data.setdefault(group, {})[str(partition)] = offset
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def dump(self) -> dict:
        return self._data