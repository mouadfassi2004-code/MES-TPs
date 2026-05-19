from orchestration.nightly_dag import DAG
from utils.storage import write_json, today_partition, utc_now_iso
from config import STORAGE_DIR

class Scheduler:
    """
    Ordonnanceur logique simplifié.
    Il exécute les tâches dans l'ordre des dépendances.
    """

    def __init__(self, dag: dict = DAG):
        self.dag = dag
        self.status: dict[str, str] = {}

    def can_run(self, task_name: str) -> bool:
        dependencies = self.dag[task_name]["depends_on"]

        return all(
            self.status.get(dep) == "SUCCESS"
            for dep in dependencies
        )

    def run(self, date: str | None = None) -> dict:
        date = date or today_partition()
        remaining = set(self.dag.keys())

        while remaining:
            progress = False

            for task_name in list(remaining):
                if self.can_run(task_name):
                    try:
                        print(f"Exécution tâche: {task_name}")
                        self.dag[task_name]["function"](date)
                        self.status[task_name] = "SUCCESS"
                    except Exception as exc:
                        self.status[task_name] = f"FAILED: {exc}"
                        raise

                    remaining.remove(task_name)
                    progress = True

            if not progress:
                raise RuntimeError(
                    "Dépendance circulaire ou tâche bloquée dans le DAG"
                )

        result = {
            "date": date,
            "finished_at": utc_now_iso(),
            "tasks": self.status,
        }

        write_json(
            STORAGE_DIR / "orchestration" / f"run_{date}.json",
            result,
        )

        return result

if __name__ == "__main__":
    scheduler = Scheduler()
    print(scheduler.run())