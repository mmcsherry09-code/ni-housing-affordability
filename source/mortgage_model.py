import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"
SQL_PATH = PROJECT_ROOT / "sql" / "03_mortgage_affordability.sql"

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_query = file.read()

with sqlite3.connect(DATABASE_PATH) as conn:
    df = pd.read_sql_query(sql_query, conn)

MORTGAGE_TERM_YEARS = 25
MONTHS = MORTGAGE_TERM_YEARS * 12

deposit_scenarios = {"5% deposit": ("rate_95_ltv", 0.05), "10% deposit": ("rate_90_ltv", 0.10), "25% deposit": ("rate_75_ltv", 0.25),}

for scenario, (rate_column, deposit_fraction) in deposit_scenarios.items():
    deposit_column = scenario.replace(" ", "_").replace("%", "percent") + "_amount"
    repayment_column = scenario.replace(" ", "_").replace("%", "percent") + "_monthly"
    burden_column = scenario.replace(" ", "_").replace("%", "percent") + "_burden"

    df[deposit_column] = df["house_price"] * deposit_fraction
    loan = df["house_price"] - df[deposit_column]

    monthly_rate = df[rate_column] / 100 / 12

    df[repayment_column] = (loan * monthly_rate * (1 + monthly_rate) ** MONTHS / ((1 + monthly_rate) ** MONTHS - 1))

    df[burden_column] = (df[repayment_column] * 12 / df["annual_earnings"] * 100)

latest = df[df["Year"] == 2025].iloc[0]

print("MORTGAGE AFFORDABILITY MODEL")
print(f"Assumed mortgage term: {MORTGAGE_TERM_YEARS} years")
print("Property price: £{:,.2f}".format(latest["house_price"]))
print("Annual full-time median earnings: £{:,.2f}".format(latest["annual_earnings"]))

for scenario in deposit_scenarios:
    prefix = scenario.replace(" ", "_").replace("%", "percent")

    deposit = latest[f"{prefix}_amount"]
    monthly = latest[f"{prefix}_monthly"]
    burden = latest[f"{prefix}_burden"]

    print(f"\n{scenario}")
    print(f"  Deposit required: £{deposit:,.2f}")
    print(f"  Monthly repayment: £{monthly:,.2f}")
    print(f"  Annual repayments / gross earnings: {burden:.1f}%")
