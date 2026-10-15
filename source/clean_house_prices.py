import pandas as pd

file_path = "data/NI-House-Price-Index-Q1-2005-Q2-2026.xlsx"

df = pd.read_excel(file_path, sheet_name="Table 1", header=3)

df = df[["Year", "Quarter", "NI House Price Index", "NI House Standardised Price"]]

df["Year"] = df["Year"].ffill()

df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

df["NI House Price Index"] = pd.to_numeric(df["NI House Price Index"], errors="coerce")

df["NI House Standardised Price"] = pd.to_numeric(df["NI House Standardised Price"], errors="coerce" )

df = df[(df["Year"] >= 2015) & (df["Year"] <= 2025)]

df = df.reset_index(drop=True)

print(df)
print("\nDATA TYPES:")
print(df.dtypes)

annual_house_prices = (df.groupby("Year", as_index=False)["NI House Standardised Price"].mean().rename(columns={"NI House Standardised Price": "house_price"}))

annual_house_prices["house_price"] = annual_house_prices["house_price"].round(2)

print(annual_house_prices)

print("\nNUMBER OF YEARS:", len(annual_house_prices))

output_path = "data/house_prices_2015_2025.csv"

annual_house_prices.to_csv(output_path, index=False)

print(f"\nSaved cleaned data to: {output_path}")

