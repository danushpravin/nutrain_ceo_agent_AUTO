import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# -------------------------------
# CONFIG
# -------------------------------

PRODUCTS = ["Nutrain Vanilla", "Nutrain Choco Coffee", "Nutrain Banana Oats"]
REGIONS = ["Bangalore", "Mumbai", "Delhi", "Chennai"]
CHANNELS = ["Instagram", "Google", "Influencers"]

BASE_PRICE = {
    "Nutrain Vanilla": 180,
    "Nutrain Choco Coffee": 190,
    "Nutrain Banana Oats": 170,
}

BASE_DAILY_DEMAND = {
    "Nutrain Vanilla": 120,
    "Nutrain Choco Coffee": 90,
    "Nutrain Banana Oats": 60,
}

# -------------------------------
# LOAD LAST DATE
# -------------------------------

LIVE_PATH = "data/live/sales_live.csv"

last_date = None

if os.path.exists(LIVE_PATH) and os.path.getsize(LIVE_PATH) > 0:
    live_df = pd.read_csv(LIVE_PATH)

    if "date" in live_df.columns:
        live_df["date"] = pd.to_datetime(live_df["date"], format="mixed", errors="coerce")
        last_date = live_df["date"].max()

# ✅ Fallback if file empty, missing dates, or NaT
if last_date is None or pd.isna(last_date):
    last_date = datetime(2024, 12, 31)

today = last_date + timedelta(days=1)


# -------------------------------
# SIMULATE DAY
# -------------------------------

rows = []

for product in PRODUCTS:
    for region in REGIONS:
        for channel in CHANNELS:

            # Demand noise (realism)
            demand_multiplier = np.random.normal(1.0, 0.15)

            units = int(
                BASE_DAILY_DEMAND[product]
                * demand_multiplier
                * np.random.uniform(0.7, 1.3)
            )

            units = max(units, 0)

            revenue = units * BASE_PRICE[product]

            cac = round(np.random.uniform(25, 70), 2)

            rows.append([
                today.strftime("%Y-%m-%d"),
                product,
                region,
                channel,
                units,
                revenue,
                cac
            ])
day_df = pd.DataFrame(rows, columns=[
    "date", "product", "region", "channel",
    "units_sold", "revenue", "CAC"
])
# -------------------------------
# MARKETING SIMULATION
# -------------------------------

MARKETING_PATH = "data/live/marketing_live.csv"
marketing_rows = []

for channel in CHANNELS:
    # Total revenue attributed to this channel today
    channel_revenue = day_df[day_df["channel"] == channel]["revenue"].sum()

    # Spend as % of revenue (inefficient channels burn more)
    spend_ratio = {
        "Instagram": np.random.uniform(0.15, 0.25),
        "Google": np.random.uniform(0.25, 0.45),
        "Influencers": np.random.uniform(0.30, 0.50),
    }[channel]

    spend = round(channel_revenue * spend_ratio, 2)

    # Funnel simulation
    impressions = int(spend * np.random.uniform(80, 150))
    ctr = np.random.uniform(0.8, 2.5) / 100
    clicks = int(impressions * ctr)

    conversion_rate = np.random.uniform(1.5, 4.0) / 100
    conversions = int(clicks * conversion_rate)

    marketing_rows.append([
        today.strftime("%Y-%m-%d"),
        channel,
        spend,
        impressions,
        clicks,
        conversions,
        channel_revenue
    ])

marketing_df = pd.DataFrame(
    marketing_rows,
    columns=[
        "date",
        "channel",
        "spend",
        "impressions",
        "clicks",
        "conversions",
        "revenue"
    ]
)

if os.path.exists(MARKETING_PATH):
    old = pd.read_csv(MARKETING_PATH)
    if not old.empty:
        marketing_df = pd.concat([old, marketing_df], ignore_index=True)

marketing_df.to_csv(MARKETING_PATH, index=False)

# -------------------------------
# INVENTORY SIMULATION
# -------------------------------

INVENTORY_PATH = "data/live/inventory_live.csv"
inventory_rows = []

# Load previous inventory
if os.path.exists(INVENTORY_PATH) and os.path.getsize(INVENTORY_PATH) > 0:
    inv_df = pd.read_csv(INVENTORY_PATH)
    last_stock = inv_df.groupby("product")["closing_stock"].last().to_dict()
else:
    last_stock = {p: 5000 for p in PRODUCTS}

for product in PRODUCTS:
    opening_stock = last_stock.get(product, 5000)

    units_sold_today = day_df[
        day_df["product"] == product
    ]["units_sold"].sum()

    # Simple production logic
    units_produced = int(np.random.uniform(200, 500))

    units_dispatched = min(
        opening_stock + units_produced,
        units_sold_today
    )

    closing_stock = (
        opening_stock + units_produced - units_dispatched
    )

    inventory_rows.append([
        today.strftime("%Y-%m-%d"),
        product,
        opening_stock,
        units_produced,
        units_dispatched,
        closing_stock,
        "Yes" if closing_stock <= 0 else "No"
    ])

inventory_df = pd.DataFrame(
    inventory_rows,
    columns=[
        "date",
        "product",
        "opening_stock",
        "units_produced",
        "units_dispatched",
        "closing_stock",
        "stockout_flag"
    ]
)

if os.path.exists(INVENTORY_PATH):
    old = pd.read_csv(INVENTORY_PATH)
    if not old.empty:
        inventory_df = pd.concat([old, inventory_df], ignore_index=True)


inventory_df.to_csv(INVENTORY_PATH, index=False)

# -------------------------------
# APPEND TO LIVE DATA
# -------------------------------



if live_df.empty:
    final_df = day_df
else:
    final_df = pd.concat([live_df, day_df], ignore_index=True)

final_df.to_csv(LIVE_PATH, index=False)

print(f"✅ Simulated business day: {today.date()}")

