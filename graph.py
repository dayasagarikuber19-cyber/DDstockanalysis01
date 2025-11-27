import os
import pandas as pd
import matplotlib.pyplot as plt
folder =( r"C:\Users\admin\Documents\python_folder\ticker_csv")

all_data = []

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        df["Ticker"] = file.replace(".csv", "") 
        all_data.append(df)

data = pd.concat(all_data, ignore_index=True)

print("Data loaded successfully!")
print("Rows:", len(data))
print(data.head())
returns = data.groupby("Ticker")["close"].apply(
    lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]
).reset_index(name="YearlyReturn")
top_green = returns.sort_values("YearlyReturn", ascending=False).head(10)
top_red = returns.sort_values("YearlyReturn").head(10)

print("\nTOP 10 GREEN STOCKS:")
print(top_green)

print("\nTOP 10 LOSS STOCKS:")
print(top_red)
green_count = (returns["YearlyReturn"] > 0).sum()
red_count = (returns["YearlyReturn"] <= 0).sum()

avg_price = data["close"].mean()
avg_volume = data["volume"].mean()

print("\n--- MARKET SUMMARY ---")
print("Green Stocks:", green_count)
print("Red Stocks:", red_count)
print("Average Price:", avg_price)
print("Average Volume:", avg_volume)

data["DailyReturn"] = data.groupby("Ticker")["close"].pct_change()

volatility = data.groupby("Ticker")["DailyReturn"].std().reset_index(name="Volatility")

top_vol = volatility.sort_values("Volatility", ascending=False).head(10)

print("\nTOP 10 MOST VOLATILE STOCKS:")
print(top_vol)
print()

plt.figure(figsize=(10, 6))
plt.bar(top_vol["Ticker"], top_vol["Volatility"])
plt.title("Top 10 Most Volatile Stocks")
plt.xlabel("Ticker")
plt.ylabel("Volatility")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# second requirement of the project
import matplotlib.pyplot as plt
import pandas as pd
import os
folder = r"C:\Users\admin\Documents\python_folder\ticker_csv"
all_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

df_list = []
for f in all_files:
    path = os.path.join(folder, f)
    data = pd.read_csv(path)
    df_list.append(data)

df = pd.concat(df_list, ignore_index=True)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["Ticker", "date"])

df["daily_return"] = df.groupby("Ticker")["close"].pct_change()

df["cumulative_return"] = (1 + df["daily_return"]).groupby(df["Ticker"]).cumprod() - 1

final_returns = df.groupby("Ticker")["cumulative_return"].last()
top5 = final_returns.sort_values(ascending=False).head(5).index


plt.figure(figsize=(12, 6))
for ticker in top5:
    stock_data = df[df["Ticker"] == ticker]
    plt.plot(stock_data["date"], stock_data["cumulative_return"], label=ticker)
plt.title("Cumulative Return Over Time (Top 5 Stocks)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.show()

 # 3rd requirement of the project
import pandas as pd
import glob
import os

sector_df = pd.read_csv("sector.csv")
sector_df["Symbol"] = sector_df["Symbol"].apply(lambda x: x.split(":")[-1].strip())

path = "ticker_csv/*.csv"
files = glob.glob(path)

dfs = []
for f in files:
    df = pd.read_csv(f)
    df["Ticker"] = os.path.basename(f).replace(".csv", "")
    dfs.append(df)

all_stock_df = pd.concat(dfs, ignore_index=True)

merged = all_stock_df.merge(sector_df, left_on="Ticker", right_on="Symbol", how="left")
merged["Year"] = pd.to_datetime(merged["date"]).dt.year
merged = merged.sort_values(["Ticker", "date"])
merged["pct_change"] = merged.groupby("Ticker")["close"].pct_change()

sector_yearly = merged.groupby("sector")["pct_change"].mean()
print(sector_yearly)

top3_sectors = sector_yearly.sort_values(ascending=False).head(3)
print("\nTop 3 Sectors by Average Yearly Return:")
print(top3_sectors)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
sector_yearly.sort_values().plot(kind='barh')
plt.title("Average Yearly Return by Sector")
plt.xlabel("Average Yearly Return")
plt.ylabel("Sector")
plt.grid(True)
plt.show()

#5th requirement of the project

files = glob.glob("ticker_csv/*.csv")

all_data = []
for f in files:
    df = pd.read_csv(f)
    df["Ticker"] = os.path.basename(f).replace(".csv", "")
    df["date"] = pd.to_datetime(df["date"])
    all_data.append(df)

data = pd.concat(all_data)

data["Month"] = data["date"].dt.to_period("M")

simple = data.sort_values("date")
simple["Prev_Close"] = simple.groupby(["Ticker", "Month"])["close"].transform("first")
simple["Return"] = (simple["close"] - simple["Prev_Close"]) / simple["Prev_Close"]

monthly = simple.groupby(["Ticker", "Month"])["Return"].last().reset_index()
months = monthly["Month"].unique()

for m in months:
    temp = monthly[monthly["Month"] == m]

    gain = temp.sort_values("Return", ascending=False).head(5)
    lose = temp.sort_values("Return", ascending=True).head(5)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.bar(gain["Ticker"], gain["Return"])
plt.title(f"{m} - Top 5 Gainers")
plt.subplot(1, 2, 2)
plt.bar(lose["Ticker"], lose["Return"])
plt.title(f"{m} - Top 5 Losers")
plt.tight_layout()
plt.show()


               


