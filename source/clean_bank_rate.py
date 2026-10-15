import pandas as pd

file_path = "data/Bank-of-England-data-bank-rate.xlsx"

excel_file = pd.ExcelFile(file_path)

print(excel_file.sheet_names)

df = pd.read_excel(file_path, sheet_name="Sheet1", header=1)

df["Date"] = pd.to_datetime(df["Date"], format="%d %b %y")

df["Monthly average of official Bank Rate  [a] [b] IUMABEDR"] = pd.to_numeric(df["Monthly average of official Bank Rate  [a] [b] IUMABEDR"], errors="coerce")

df = df.rename(columns={"Monthly average of official Bank Rate  [a] [b] IUMABEDR": "bank_rate"})

df = df[(df["Date"].dt.year >= 2015) & (df["Date"].dt.year <= 2025)].copy()

df = df.sort_values("Date").reset_index(drop=True)

print(df.head())
print("\n...")
print(df.tail()) 

print("\nNUMBER OF MONTHLY OBSERVATIONS:", len(df))

output_path = "data/bank_rate_2015_2025.csv"

df.to_csv(output_path, index=False)

print(f"Saved cleaned data to: {output_path}")
