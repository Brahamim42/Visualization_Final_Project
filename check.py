import pandas as pd

df_macro = pd.read_csv("../Users/orasi/Downloads/VizFinal/VizFinal/macro.csv")

print("=== MACRO DATASET (RAW) ===")
print(f"Total rows: {len(df_macro)}")

print("\nColumns in dataset:")
print(df_macro.columns.tolist())

# Detect country column
if "countryname" in df_macro.columns:
    country_col = "countryname"
elif "country" in df_macro.columns:
    country_col = "country"
else:
    raise ValueError("Country column not found")

# Cardinality checks
num_countries = df_macro[country_col].nunique()
num_years = df_macro["year"].nunique()

print(f"\nUnique countries: {num_countries}")
print(f"Unique years: {num_years}")
print(f"Year range: {df_macro['year'].min()} - {df_macro['year'].max()}")

# GDP statistics
print("\nReal GDP per capita statistics:")
print(df_macro["rGDP_pc"].describe())
