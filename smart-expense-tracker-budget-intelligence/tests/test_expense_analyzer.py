import pandas as pd

from src.expense_analyzer import (
    total_expense,
    category_summary,
    average_daily_spending,
    budget_status,
    forecast_next_month,
)


def sample_data():
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-08-01", "2026-08-01", "2026-08-02"]),
        "category": ["Food", "Transport", "Food"],
        "description": ["Lunch", "Bus", "Dinner"],
        "amount": [200, 100, 300],
        "payment_method": ["UPI", "Cash", "UPI"],
    })


def test_total_expense():
    assert total_expense(sample_data()) == 600


def test_category_summary():
    result = category_summary(sample_data())
    assert result.iloc[0]["category"] == "Food"
    assert result.iloc[0]["amount"] == 500


def test_average_daily_spending():
    assert average_daily_spending(sample_data()) == 300


def test_budget_status():
    result = budget_status(sample_data(), 1000)
    assert result["remaining"] == 400
    assert result["overspent"] is False


def test_forecast():
    result = forecast_next_month(sample_data())
    assert result == 600
