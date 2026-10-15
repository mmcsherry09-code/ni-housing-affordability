import pandas as pd

file_path = "data/ASHE-1997-2025-headline-timeseries.xlsx"

df = pd.read_excel(file_path, sheet_name="Annual", header=3)

df.columns = ["Year", "Full-time", "Part-time", "All"]

df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
df["Full-time"] = pd.to_numeric(df["Full-time"], errors="coerce")
df["Part-time"] = pd.to_numeric(df["Part-time"], errors="coerce")
df["All"] = pd.to_numeric(df["All"], errors="coerce")

df = df[(df["Year"] >= 2015) & (df["Year"] <= 2025)]

df = df.reset_index(drop=True)

print(df)
print("\nDATA TYPES:")
print(df.dtypes)

output_path = "data/ashe_earnings_2015_2025.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved cleaned data to: {output_path}")