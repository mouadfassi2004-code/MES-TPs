from utils.storage import utc_now_iso

class BatchMetrics:
    def __init__(self, task_name: str):
        self.task_name = task_name
        self.rows_read = 0
        self.rows_written = 0
        self.rows_rejected = 0

    def snapshot(self, status: str) -> dict:
        return {
            "timestamp": utc_now_iso(),
            "task": self.task_name,
            "status": status,
            "rows_read": self.rows_read,
            "rows_written": self.rows_written,
            "rows_rejected": self.rows_rejected,
        }