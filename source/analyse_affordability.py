import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"
SQL_PATH = PROJECT_ROOT / "sql" / "02_affordability_metrics.sql"

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_query = file.read()

with sqlite3.connect(DATABASE_PATH) as conn:
    affordability = pd.read_sql_query(sql_query, conn)

print("AFFORDABILITY DATA")
print(affordability.to_string(index=False))

first_year = affordability.iloc[0]
last_year = affordability.iloc[-1]

earnings_change = ((last_year["annual_earnings"] / first_year["annual_earnings"]) - 1) * 100

house_price_change = ((last_year["house_price"] / first_year["house_price"]) - 1) * 100

rent_change = ((last_year["annual_rent"] / first_year["annual_rent"]) - 1) * 100

print("\nCHANGE BETWEEN 2015 AND 2025")
print(f"Full-time annual earnings: {earnings_change:.2f}%")
print(f"House prices: {house_price_change:.2f}%")
print(f"Annual rent: {rent_change:.2f}%")
