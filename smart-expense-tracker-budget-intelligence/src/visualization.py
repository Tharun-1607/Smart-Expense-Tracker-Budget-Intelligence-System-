import matplotlib.pyplot as plt


def category_chart(summary):
    fig, ax = plt.subplots(figsize=(8, 4))
    if summary.empty:
        ax.text(0.5, 0.5, "No expense data", ha="center", va="center")
        ax.set_axis_off()
        return fig

    ax.bar(summary["category"], summary["amount"])
    ax.set_title("Spending by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


def monthly_chart(summary):
    fig, ax = plt.subplots(figsize=(8, 4))
    if summary.empty:
        ax.text(0.5, 0.5, "No monthly data", ha="center", va="center")
        ax.set_axis_off()
        return fig

    ax.plot(summary["month"], summary["amount"], marker="o")
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig
