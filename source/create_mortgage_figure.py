import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"
SQL_PATH = PROJECT_ROOT / "sql" / "03_mortgage_affordability.sql"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_query = file.read()

with sqlite3.connect(DATABASE_PATH) as conn:
    df = pd.read_sql_query(sql_query, conn)

MORTGAGE_TERM_YEARS = 25
MONTHS = MORTGAGE_TERM_YEARS * 12

scenarios = [("5% deposit", "rate_95_ltv", 0.05), ("10% deposit", "rate_90_ltv", 0.10), ("25% deposit", "rate_75_ltv", 0.25)]

for name, rate_column, deposit_fraction in scenarios:
    prefix = name.replace(" ", "_").replace("%", "percent")

    deposit_column = f"{prefix}_amount"
    repayment_column = f"{prefix}_monthly"

    df[deposit_column] = df["house_price"] * deposit_fraction
    loan = df["house_price"] - df[deposit_column]
    monthly_rate = df[rate_column] / 100 / 12

    df[repayment_column] = (loan * monthly_rate * (1 + monthly_rate) ** MONTHS / ((1 + monthly_rate) ** MONTHS - 1))
    burden_column = f"{prefix}_burden"
    df[burden_column]=(df[repayment_column] * 12 / df["annual_earnings"] * 100)

latest = df.loc[df["Year"] == df["Year"].max()].iloc[0]

labels = [scenario[0] for scenario in scenarios]

deposits = [latest[f"{name.replace(' ', '_').replace('%', 'percent')}_amount"] for name, _, _ in scenarios]

repayments = [latest[f"{name.replace(' ', '_').replace('%', 'percent')}_monthly"] for name, _, _ in scenarios]

fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

deposit_bars = axes[0].bar(labels, deposits)
axes[0].set_title("Deposit Required")
axes[0].set_ylabel("Deposit (£)")
axes[0].set_ylim(0, max(deposits) * 1.2)
axes[0].bar_label(deposit_bars, labels=[f"£{value:,.0f}" for value in deposits], padding=4)
axes[0].tick_params(axis="x", rotation=15)
axes[0].grid(axis="y", alpha=0.25)
axes[0].set_axisbelow(True)


repayment_bars = axes[1].bar(labels, repayments)
axes[1].set_title("Estimated Monthly Mortgage Repayment")
axes[1].set_ylabel("Monthly repayment (£)")
axes[1].set_ylim(0, max(repayments) * 1.35)
burdens = [latest[f"{name.replace(' ', '_').replace('%', 'percent')}_burden"] for name, _, _ in scenarios]
axes[1].bar_label(repayment_bars, labels=[f"£{payment:,.0f}\n({burden:.1f}% of gross earnings)" for payment, burden in zip(repayments, burdens)], padding=4, fontsize=9)
axes[1].tick_params(axis="x", rotation=15)
axes[1].grid(axis="y", alpha=0.25)
axes[1].set_axisbelow(True)

fig.suptitle(f"Illustrative Mortgage Affordability in Northern Ireland ({int(latest['Year'])})", fontsize=14)

fig.text(0.5, 0.01, "Illustrative estimates assuming a 25 year repayement term. " "Annual average rates for two year fixed-rate products are held " "constant for illustration. Repayements exclude fees and other housing costs.", ha="center", fontsize=8, wrap=True)

fig.tight_layout(rect=[0, 0.08, 1, 0.93])

output_path = FIGURES_DIR / "mortgage_affordability_scenarios.png"
fig.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Figure saved to: {output_path}")


