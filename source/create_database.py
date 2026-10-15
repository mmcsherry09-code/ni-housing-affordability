import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"

conn = sqlite3.connect(DATABASE_PATH)

print(f"Database created at: {DATABASE_PATH}")

earnings = pd.read_csv(DATA_DIR / "ashe_earnings_2015_2025.csv")

earnings.to_sql("earnings", conn, if_exists="replace", index=False)

print("Earnings data loaded.")

check = pd.read_sql_query("SELECT * FROM earnings LIMIT 5;", conn)

print("\nEarnings table:")
print(check)

house_prices = pd.read_csv(DATA_DIR / "house_prices_2015_2025.csv")

house_prices.to_sql("house_prices", conn, if_exists="replace", index=False)

print("House price data loaded.")

check = pd.read_sql_query("SELECT * FROM house_prices LIMIT 5;", conn)

print("\nHouse prices table:")
print(check)


rents = pd.read_csv(DATA_DIR / "rents_2015_2025.csv")

rents.to_sql("rents", conn, if_exists="replace", index=False)

print("Rent data loaded.")

check = pd.read_sql_query("SELECT * FROM rents LIMIT 5;", conn)

print("\nRents table:")
print(check)

bank_rate = pd.read_csv(DATA_DIR / "bank_rate_2015_2025.csv")

bank_rate.to_sql("bank_rate", conn, if_exists="replace", index=False)

print("Bank Rate data loaded.")

check = pd.read_sql_query("SELECT * FROM bank_rate LIMIT 5;", conn)

print("\nBank Rate table:")
print(check)

mortgage_75 = pd.read_csv(DATA_DIR / "mortgage_rate_75_ltv_2015_2025.csv")

mortgage_90 = pd.read_csv(DATA_DIR / "mortgage_rate_90_ltv_2015_2025.csv")

mortgage_95 = pd.read_csv( DATA_DIR / "mortgage_rate_95_ltv_2015_2025.csv")

mortgage_rates = mortgage_75.merge(mortgage_90, on="Date", how="inner")

mortgage_rates = mortgage_rates.merge(mortgage_95, on="Date", how="inner")

mortgage_rates.to_sql("mortgage_rates", conn, if_exists="replace", index=False)

print("Mortgage rate data loaded.")

check = pd.read_sql_query("SELECT * FROM mortgage_rates LIMIT 5;", conn)

print("\nMortgage rates table:")
print(check)
