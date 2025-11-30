

import os
import yaml
import pandas as pd

base_path = r"C:\Users\admin\Documents\python_folder\daya"

all_rows = []

for month in sorted(os.listdir(base_path)):
    month_folder = os.path.join(base_path, month)

    if not os.path.isdir(month_folder):
        continue



    for file in sorted(os.listdir(month_folder)):
        if file.endswith(".yaml"):
            file_path = os.path.join(month_folder, file)

            with open(file_path, 'r') as f:
                data_list = yaml.safe_load(f)

            for row in data_list:
                row["month"] = month
                row["file"] = file
                all_rows.append(row)

df = pd.DataFrame(all_rows)

print("\n==============================")
print("FINAL DATAFRAME PREVIEW")
print("==============================")
print(df.head())
print(df.shape)

df.to_csv("final_full_year_data.csv", index=False)
print("\n Saved: final_full_year_data.csv")

if "Ticker" in df.columns:
    tickers = df["Ticker"].unique()

    output_folder = "ticker_files"
    os.makedirs(output_folder, exist_ok=True)

    for t in tickers:
        tdf = df[df["Ticker"] == t]
        tdf.to_csv(f"{output_folder}/{t}.csv", index=False)

    print(f"Created {len(tickers)} ticker CSV files inside: ticker_files")
else:
    print("'Ticker' column not found!")
