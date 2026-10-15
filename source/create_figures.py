import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"
SQL_PATH = PROJECT_ROOT / "sql" / "02_affordability_metrics.sql"
FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(exist_ok=True)

with open(SQL_PATH, "r", encoding="utf-8") as file:
    sql_query = file.read()

with sqlite3.connect(DATABASE_PATH) as conn:
    df = pd.read_sql_query(sql_query, conn)

df["earnings_index"] = (df["annual_earnings"] / df["annual_earnings"].iloc[0] * 100)

df["house_price_index"] = (df["house_price"] / df["house_price"].iloc[0] * 100)

df["rent_index"] = (df["annual_rent"] / df["annual_rent"].iloc[0] * 100)

end_year = df.iloc[-1]

plt.annotate(
    f"+{end_year['earnings_index'] - 100:.1f}%",
    (end_year["Year"], end_year["earnings_index"]),
    xytext=(8, -12),
    textcoords="offset points",
    fontsize=9
)

plt.annotate(
    f"+{end_year['house_price_index'] - 100:.1f}%",
    (end_year["Year"], end_year["house_price_index"]),
    xytext=(8, 0),
    textcoords="offset points",
    fontsize=9
)
plt.annotate(
    f"+{end_year['rent_index'] - 100:.1f}%",
    (end_year["Year"], end_year["rent_index"]),
    xytext=(8, 0),
    textcoords="offset points",
    fontsize=9
)
plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["earnings_index"], marker="o", label="Full-time annual earnings")
plt.plot(df["Year"], df["house_price_index"], marker="o", label="Standardised house price")
plt.plot(df["Year"], df["rent_index"], marker="o", label="Annualised advertised rent (monthly average x 12)")
plt.axhline(100, linestyle="--", linewidth=1, label="2015 baseline")
plt.title("Earnings, House Prices and Rents in Northern Ireland, 2015–2025")
plt.xlabel("Year")
plt.ylabel("Index (2015 = 100)")
plt.xticks(df["Year"], rotation=45)
plt.xlim(2015, 2026)
plt.legend()
plt.grid(True, alpha=0.3)
plt.figtext(0.01, 0.01, "Sources: NISRA ASHE; NI House Price Index; ONS Price Index of Private Rents. Author's calculations.", ha="left", fontsize=8)
plt.tight_layout(rect=[0, 0.04, 1, 1])

output_path = FIGURES_DIR / "earnings_house_prices_rents_index.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Figure saved to: {output_path}")

