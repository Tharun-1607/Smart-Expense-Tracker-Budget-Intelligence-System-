import pandas as pd
import numpy as np


def total_expense(df):
    return float(df["amount"].sum()) if not df.empty else 0.0


def category_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])

    result = (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    return result


def monthly_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["month", "amount"])

    temp = df.copy()
    temp["month"] = temp["date"].dt.to_period("M").astype(str)
    return (
        temp.groupby("month", as_index=False)["amount"]
        .sum()
        .sort_values("month")
    )


def average_daily_spending(df):
    if df.empty:
        return 0.0

    days = max(df["date"].dt.date.nunique(), 1)
    return total_expense(df) / days


def detect_high_expenses(df, threshold=None):
    if df.empty:
        return df.copy()

    if threshold is None:
        threshold = df["amount"].mean() + 2 * df["amount"].std()
        if np.isnan(threshold):
            threshold = df["amount"].mean()

    return df[df["amount"] >= threshold].sort_values("amount", ascending=False)


def budget_status(df, budget):
    spent = total_expense(df)
    remaining = budget - spent
    percentage = (spent / budget * 100) if budget > 0 else 0
    return {
        "spent": spent,
        "remaining": remaining,
        "percentage": percentage,
        "overspent": remaining < 0,
    }


def forecast_next_month(df):
    summary = monthly_summary(df)
    if summary.empty:
        return 0.0

    # Simple data-science baseline: average of available monthly spending.
    return float(summary["amount"].tail(3).mean())
