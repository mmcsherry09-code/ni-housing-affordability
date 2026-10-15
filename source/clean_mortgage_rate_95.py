import pandas as pd 

file_path = "data/IUM2WTL-Bank-of-England-Database.xlsx"

df = pd.read_excel(file_path, header= 1)

df["Date"] = pd.to_datetime(df["Date"], format="%d %b %y")

df = df.rename(columns={df.columns[1]: "mortgage_rate_95_ltv"})

df = df[(df["Date"].dt.year >= 2015) & (df["Date"].dt.year <= 2025)].copy()

df = df.sort_values("Date").reset_index(drop=True)

print(df.head())
print("\nCOLUMNS:")
print(df.columns)

print(df.head())
print("\nLAST 5 ROWS:")
print(df.tail())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nNUMBER OF MONTHLY OBSERVATIONS:", len(df))

output_path = "data/mortgage_rate_95_ltv_2015_2025.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved cleaned data to: {output_path}")