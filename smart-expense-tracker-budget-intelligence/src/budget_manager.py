import json
from pathlib import Path

BUDGET_PATH = Path(__file__).resolve().parent.parent / "data" / "budgets.json"

DEFAULT_BUDGETS = {
    "Food": 5000,
    "Transport": 2500,
    "Education": 5000,
    "Entertainment": 2000,
    "Shopping": 4000,
    "Bills": 3000,
    "Other": 2000,
}


def load_budgets(path=BUDGET_PATH):
    path = Path(path)
    if not path.exists():
        return DEFAULT_BUDGETS.copy()

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_BUDGETS.copy()


def save_budgets(budgets, path=BUDGET_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(budgets, indent=2), encoding="utf-8")
