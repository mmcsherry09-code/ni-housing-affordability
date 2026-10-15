import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "financial_independence.db"
SQL_DIR = PROJECT_ROOT / "sql"

if len(sys.argv) != 2:
    print("Usage: python source/run_sql.py <sql_file>")
    sys.exit(1)

conn = sqlite3.connect(DATABASE_PATH)

sql_file = SQL_DIR / sys.argv[1]

with open(sql_file, "r") as file:
    sql_script = file.read()

queries = [query.strip() for query in sql_script.split(";") if query.strip()]

for query in queries:
    cursor = conn.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

print("\nSQL script executed successfully.")

conn.close()