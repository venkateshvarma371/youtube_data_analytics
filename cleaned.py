
import pandas as pd
from pathlib import Path

# 1. File paths
input_file = Path("data/raw/datacollection.ytanalysis.csv")
output_folder = Path("data/cleaned")
output_folder.mkdir(parents=True, exist_ok=True)

# 2. Load dataset
df = pd.read_csv(input_file)

print("ORIGINAL DATASET")
print("Shape:", df.shape)
print(df.head())

# 3. Clean column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# 4. Remove exact duplicate rows
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()
print("\nDuplicates removed:", duplicate_count)

# 5. Remove extra spaces from text columns
text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:
    df[col] = df[col].str.strip()

# 6. Convert known numeric columns
numeric_columns = [
    "rank",
    "subscribers",
    "video_views",
    "uploads",
    "video_views_rank",
    "country_rank",
    "channel_type_rank",
    "video_views_for_the_last_30_days",
    "lowest_monthly_earnings",
    "highest_monthly_earnings",
    "lowest_yearly_earnings",
    "highest_yearly_earnings",
    "subscribers_for_last_30_days",
    "created_year",
    "population",
    "unemployment_rate",
    "urban_population",
    "latitude",
    "longitude",
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 7. Display missing values
print("\nMissing values:")
print(df.isnull().sum())

# 8. Check for invalid negative counts
count_columns = [
    "subscribers",
    "video_views",
    "uploads",
    "population",
    "urban_population",
]

print("\nNegative count values:")
for col in count_columns:
    if col in df.columns:
        print(col, (df[col] < 0).sum())

# 9. Check unusual creation years
if "created_year" in df.columns:
    print("\nCreation year anomalies:")
    print(
        df.loc[
            ~df["created_year"].between(2005, 2026),
            ["youtuber", "created_year"]
        ]
    )

# 10. Save cleaned data
output_file = output_folder / "datacollection.ytanalysis.cleaned.csv"
df.to_csv(output_file, index=False)

# 11. Final report
print("\nDATA CLEANING COMPLETED")
print("Final shape:", df.shape)
print("Output saved to:", output_file)

import pandas as pd

file_path = "data/cleaned/datacollection.ytanalysis.cleaned.csv"

df = pd.read_csv(file_path)

print("Rows and columns:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print("\nMissing values:")
print(df.isnull().sum())
print("\nFirst five rows:")
print(df.head())
print("\nSummary statistics:")
print(df.describe())