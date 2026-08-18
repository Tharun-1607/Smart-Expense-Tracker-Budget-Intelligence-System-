import sys
from pathlib import Path

import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data_loader import load_expenses, save_expense
from src.expense_analyzer import (
    total_expense,
    category_summary,
    monthly_summary,
    average_daily_spending,
    detect_high_expenses,
    budget_status,
    forecast_next_month,
)
from src.budget_manager import load_budgets, save_budgets
from src.visualization import category_chart, monthly_chart

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Smart Expense Tracker & Budget Intelligence")
st.caption("Track spending, understand patterns, and make better budget decisions.")

df = load_expenses()
budgets = load_budgets()

with st.sidebar:
    st.header("Add Expense")

    expense_date = st.date_input("Date")
    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Education", "Entertainment", "Shopping", "Bills", "Other"],
    )
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=1.0, step=10.0)
    payment = st.selectbox("Payment Method", ["UPI", "Cash", "Card", "Bank Transfer"])

    if st.button("➕ Add Expense", use_container_width=True):
        save_expense({
            "date": expense_date.isoformat(),
            "category": category,
            "description": description or "Expense",
            "amount": amount,
            "payment_method": payment,
        })
        st.success("Expense added!")
        st.rerun()

    st.divider()
    st.header("Monthly Budget")
    total_budget = st.number_input(
        "Total Budget (₹)",
        min_value=0.0,
        value=float(sum(budgets.values())),
        step=500.0,
    )

    if st.button("Save Budget", use_container_width=True):
        budgets["Total"] = total_budget
        save_budgets(budgets)
        st.success("Budget saved!")

    st.divider()
    st.info("Tip: Add expenses regularly to improve the spending insights.")

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    selected_month = st.selectbox(
        "Select month",
        sorted(df["date"].dt.to_period("M").astype(str).unique(), reverse=True),
    )
    view_df = df[df["date"].dt.to_period("M").astype(str) == selected_month].copy()
else:
    selected_month = None
    view_df = df.copy()

budget = float(budgets.get("Total", sum(budgets.values())))
status = budget_status(view_df, budget)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Spending", f"₹{status['spent']:,.0f}")
c2.metric("Budget", f"₹{budget:,.0f}")
c3.metric("Remaining", f"₹{status['remaining']:,.0f}")
c4.metric("Daily Average", f"₹{average_daily_spending(view_df):,.0f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("📊 Category Analysis")
    cat = category_summary(view_df)
    st.pyplot(category_chart(cat), use_container_width=True)

with right:
    st.subheader("📈 Monthly Trend")
    month = monthly_summary(df)
    st.pyplot(monthly_chart(month), use_container_width=True)

st.subheader("🧠 Budget Intelligence")

if status["overspent"]:
    st.error(
        f"You are over budget by ₹{abs(status['remaining']):,.0f}. "
        "Consider reducing discretionary spending."
    )
elif status["percentage"] >= 80:
    st.warning(
        f"You have used {status['percentage']:.1f}% of your budget. "
        "Watch your spending for the rest of the month."
    )
else:
    st.success(
        f"You have used {status['percentage']:.1f}% of your budget. "
        "Your spending is currently within the planned limit."
    )

forecast = forecast_next_month(df)
st.info(f"Estimated next-month spending based on recent history: ₹{forecast:,.0f}")

high = detect_high_expenses(view_df)
if not high.empty:
    st.write("### 🚨 High Expense Alerts")
    st.dataframe(
        high[["date", "category", "description", "amount", "payment_method"]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.write("No unusually high expenses detected.")

st.subheader("🧾 Expense Records")

if view_df.empty:
    st.info("No expenses available for the selected period.")
else:
    st.dataframe(
        view_df.sort_values("date", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

csv = view_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Selected Expenses",
    data=csv,
    file_name="expenses_export.csv",
    mime="text/csv",
)
