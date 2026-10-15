import pandas as pd

file_path = "data/PIPR-UK-monthly-price-statistics.xlsx"

df = pd.read_excel(file_path, sheet_name="Table 1", header=None)

print(df.head(15).to_string())

print(df[[1, 2]].drop_duplicates().to_string(index=False))

ni_rents = df[df[1] == "N92000002"][[0, 1, 2, 7]].copy()

ni_rents.columns = ["Time period", "Area code", "Area name", "Rental price"]

print(ni_rents.head(15).to_string(index=False))

ni_rents["Time period"] = pd.to_datetime(ni_rents["Time period"])

ni_rents["Year"] = ni_rents["Time period"].dt.year

ni_rents = ni_rents[(ni_rents["Year"] >= 2015) & (ni_rents["Year"] <= 2025)].copy()

ni_rents["Rental price"] = pd.to_numeric(ni_rents["Rental price"], errors="coerce")

print(ni_rents.head())
print("\nDATA TYPES:")
print(ni_rents.dtypes)

print("\nNUMBER OF MONTHLY OBSERVATIONS:", len(ni_rents))

annual_rents = (ni_rents.groupby("Year", as_index=False)["Rental price"].mean().rename(columns={"Rental price": "average_monthly_rent"}))

annual_rents["average_monthly_rent"] = annual_rents["average_monthly_rent"].round(2)

annual_rents["annual_rent"] = (annual_rents["average_monthly_rent"] * 12).round(2)

print(annual_rents)

output_path = "data/rents_2015_2025.csv"

annual_rents.to_csv(output_path, index=False)

print(f"Saved cleaned data to: {output_path}")