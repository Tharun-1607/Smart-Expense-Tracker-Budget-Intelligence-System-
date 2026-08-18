from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "expenses.csv"

COLUMNS = ["date", "category", "description", "amount", "payment_method"]


def load_expenses(path=DATA_PATH):
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(path)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def save_expense(expense, path=DATA_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    new_row = pd.DataFrame([expense])
    if path.exists():
        df = pd.read_csv(path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(path, index=False)
