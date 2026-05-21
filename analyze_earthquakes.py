import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MPLCONFIG_DIR = os.path.join(BASE_DIR, ".matplotlib")
os.makedirs(MPLCONFIG_DIR, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", MPLCONFIG_DIR)

import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "earthquakes.csv")

df = pd.read_csv(INPUT_FILE)

df["time"] = pd.to_datetime(df["Time"])
df["magnitude"] = pd.to_numeric(df["Magnitude"], errors="coerce")
df["depth_km"] = pd.to_numeric(df["Depth/Km"], errors="coerce")
df = df.dropna(subset=["magnitude", "depth_km"])
df["shallow_event"] = df["depth_km"] <= 3

# Относительная сейсмическая энергия
df["energy"] = 10 ** (1.5 * df["magnitude"])

# =========================
# YEARLY ANALYSIS
# =========================

df["year"] = df["time"].dt.year

yearly = df.groupby("year").agg(
    earthquakes_count=("magnitude", "count"),
    avg_magnitude=("magnitude", "mean"),
    max_magnitude=("magnitude", "max"),
    total_energy=("energy", "sum")
).reset_index()

yearly["count_rolling_avg"] = yearly["earthquakes_count"].rolling(window=3).mean()
yearly["energy_rolling_avg"] = yearly["total_energy"].rolling(window=3).mean()

yearly.to_csv("yearly_analysis.csv", index=False)

latest_year = yearly["year"].max()
full_years = yearly[yearly["year"] < latest_year].copy()
current_year = yearly[yearly["year"] == latest_year].copy()

full_years["count_rolling_avg"] = (
    full_years["earthquakes_count"].rolling(window=3).mean()
)
full_years["energy_rolling_avg"] = (
    full_years["total_energy"].rolling(window=3).mean()
)

# 1. Количество землетрясений по годам
plt.figure(figsize=(14, 7))
plt.plot(full_years["year"], full_years["earthquakes_count"], label="Earthquakes per full year")
plt.plot(full_years["year"], full_years["count_rolling_avg"], label="3-Year Rolling Average (full years)")
plt.scatter(
    current_year["year"],
    current_year["earthquakes_count"],
    color="red",
    label=f"{latest_year} YTD",
    zorder=3
)
plt.xlabel("Year")
plt.ylabel("Earthquake Count")
plt.title(
    "Campi Flegrei Seismic Activity — Yearly Trend "
    f"({latest_year} = partial year / year-to-date)"
)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("earthquake_activity_yearly.png")
plt.close()

# 2. Максимальная магнитуда по годам
plt.figure(figsize=(14, 7))
plt.plot(yearly["year"], yearly["max_magnitude"], marker="o", label="Maximum Magnitude")
plt.xlabel("Year")
plt.ylabel("Magnitude")
plt.title("Campi Flegrei — Maximum Magnitude by Year")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("max_magnitude_yearly.png")
plt.close()

# 3. Относительная энергия по годам
plt.figure(figsize=(14, 7))
plt.plot(full_years["year"], full_years["total_energy"], label="Total Relative Seismic Energy (full years)")
plt.plot(full_years["year"], full_years["energy_rolling_avg"], label="3-Year Energy Rolling Average (full years)")
plt.scatter(
    current_year["year"],
    current_year["total_energy"],
    color="red",
    label=f"{latest_year} YTD",
    zorder=3
)
plt.xlabel("Year")
plt.ylabel("Relative Energy")
plt.title(
    "Campi Flegrei — Relative Seismic Energy Release by Year "
    f"({latest_year} = partial year / year-to-date)"
)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("seismic_energy_yearly.png")
plt.close()


# =========================
# DEPTH ANALYSIS
# =========================

depth_yearly = df.groupby("year").agg(
    avg_depth=("depth_km", "mean"),
    min_depth=("depth_km", "min"),
    shallow_events=("shallow_event", "sum"),
    total_events=("depth_km", "count")
).reset_index()

depth_yearly["shallow_share_percent"] = (
    depth_yearly["shallow_events"] / depth_yearly["total_events"] * 100
)

depth_yearly.to_csv("depth_analysis_yearly.csv", index=False)

depth_full_years = depth_yearly[depth_yearly["year"] < latest_year].copy()
depth_current_year = depth_yearly[depth_yearly["year"] == latest_year].copy()

depth_full_years["shallow_rolling_avg"] = (
    depth_full_years["shallow_events"].rolling(window=3).mean()
)

# 4. Мелкие землетрясения по годам
plt.figure(figsize=(14, 7))
plt.plot(
    depth_full_years["year"],
    depth_full_years["shallow_events"],
    label="Shallow earthquakes per full year"
)
plt.plot(
    depth_full_years["year"],
    depth_full_years["shallow_rolling_avg"],
    label="3-Year Rolling Average (full years)"
)
plt.scatter(
    depth_current_year["year"],
    depth_current_year["shallow_events"],
    color="red",
    label=f"{latest_year} YTD",
    zorder=3
)
plt.xlabel("Year")
plt.ylabel("Number of Shallow Earthquakes")
plt.title(
    "Campi Flegrei — Shallow Earthquakes by Year "
    f"({latest_year} = partial year / year-to-date)"
)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("shallow_earthquakes_yearly.png")
plt.close()

# 5. Средняя глубина землетрясений по годам
plt.figure(figsize=(14, 7))
plt.plot(depth_yearly["year"], depth_yearly["avg_depth"], marker="o", label="Average Depth")
plt.xlabel("Year")
plt.ylabel("Average Depth (km)")
plt.title("Campi Flegrei — Average Earthquake Depth by Year")
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_depth_yearly.png")
plt.close()


# =========================
# MONTHLY ANALYSIS 2020+
# =========================

recent_df = df[df["time"].dt.year >= 2020].copy()

recent_df["month"] = recent_df["time"].dt.to_period("M").astype(str)

monthly = recent_df.groupby("month").agg(
    earthquakes_count=("magnitude", "count"),
    avg_magnitude=("magnitude", "mean"),
    max_magnitude=("magnitude", "max"),
    total_energy=("energy", "sum")
).reset_index()

monthly["count_rolling_avg"] = monthly["earthquakes_count"].rolling(window=3).mean()
monthly["energy_rolling_avg"] = monthly["total_energy"].rolling(window=3).mean()

monthly.to_csv("monthly_analysis_2020_2026.csv", index=False)

# 4. Количество землетрясений по месяцам
plt.figure(figsize=(16, 7))
plt.plot(monthly["month"], monthly["earthquakes_count"], label="Monthly earthquakes")
plt.plot(monthly["month"], monthly["count_rolling_avg"], label="3-Month Rolling Average")
plt.xlabel("Month")
plt.ylabel("Earthquake Count")
plt.title("Campi Flegrei Seismic Activity — Monthly Trend 2020–2026")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("earthquake_activity_monthly_2020_2026.png")
plt.close()

# 5. Максимальная магнитуда по месяцам
plt.figure(figsize=(16, 7))
plt.plot(monthly["month"], monthly["max_magnitude"], marker="o", label="Maximum Magnitude")
plt.xlabel("Month")
plt.ylabel("Magnitude")
plt.title("Campi Flegrei — Monthly Maximum Magnitude 2020–2026")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("max_magnitude_monthly_2020_2026.png")
plt.close()

# 6. Относительная энергия по месяцам
plt.figure(figsize=(16, 7))
plt.plot(monthly["month"], monthly["total_energy"], label="Monthly Relative Seismic Energy")
plt.plot(monthly["month"], monthly["energy_rolling_avg"], label="3-Month Energy Rolling Average")
plt.xlabel("Month")
plt.ylabel("Relative Energy")
plt.title("Campi Flegrei — Monthly Relative Seismic Energy 2020–2026")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("seismic_energy_monthly_2020_2026.png")
plt.close()


print("Saved files:")
print("yearly_analysis.csv")
print("monthly_analysis_2020_2026.csv")
print("depth_analysis_yearly.csv")
print("earthquake_activity_yearly.png")
print("max_magnitude_yearly.png")
print("seismic_energy_yearly.png")
print("shallow_earthquakes_yearly.png")
print("avg_depth_yearly.png")
print("earthquake_activity_monthly_2020_2026.png")
print("max_magnitude_monthly_2020_2026.png")
print("seismic_energy_monthly_2020_2026.png")
