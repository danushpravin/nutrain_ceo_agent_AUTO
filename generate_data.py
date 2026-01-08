import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ---------- CONFIG ----------
products = ["Nutrain Vanilla", "Nutrain Choco Coffee", "Nutrain Banana Oats"]
regions = ["Bangalore", "Mumbai", "Delhi", "Chennai"]
channels = ["Website", "Amazon", "Gyms"]
marketing_channels = ["Instagram", "Google", "Influencers"]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq="D")

# ---------- 1. SALES DATA ----------
sales_rows = []

for date in dates:
    for product in products:
        for region in regions:
            channel = random.choice(channels)

            # realistic units_sold patterns
            base = {
                "Nutrain Vanilla": 40,
                "Nutrain Choco Coffee": 30,
                "Nutrain Banana Oats": 15
            }[product]

            # region boost
            region_factor = {
                "Bangalore": 1.4,
                "Mumbai": 1.2,
                "Delhi": 1.0,
                "Chennai": 0.9
            }[region]

            # seasonal variation
            season = 1.2 if date.month in [1,2,6,7] else 1.0

            units = int(np.random.normal(base * region_factor * season, 5))
            units = max(units, 0)

            revenue = units * random.choice([99, 109, 119])  # typical RTD price
            CAC = random.uniform(20, 80)  # cost to acquire customer

            sales_rows.append([
                date.strftime("%Y-%m-%d"),
                product,
                region,
                channel,
                units,
                revenue,
                round(CAC, 2)
            ])

sales_df = pd.DataFrame(sales_rows, columns=[
    "date", "product", "region", "channel", "units_sold", "revenue", "CAC"
])


# ---------- 2. CUSTOMER DATA ----------
customer_rows = []
customer_id = 1000

for i in range(1200):  # approx customers
    customer_id += 1
    signup = start_date + timedelta(days=random.randint(0, 364))
    region = random.choice(regions)
    subscription = random.choice(["Yes", "No"])

    # realistic LTV
    if subscription == "Yes":
        LTV = random.uniform(1500, 6000)
        churned = "No"
    else:
        LTV = random.uniform(300, 1200)
        churned = random.choice(["Yes", "No"])

    customer_rows.append([
        customer_id,
        signup.strftime("%Y-%m-%d"),
        region,
        subscription,
        round(LTV, 2),
        churned
    ])

customers_df = pd.DataFrame(customer_rows, columns=[
    "customer_id", "signup_date", "region", "subscription", "LTV", "churned"
])


# ---------- 3. MARKETING DATA ----------
marketing_rows = []

for date in dates:
    for channel in marketing_channels:

        if channel == "Instagram":
            spend = random.uniform(3000, 9000)
            impressions = random.randint(20000, 80000)
            clicks = int(impressions * random.uniform(0.01, 0.03))
        elif channel == "Google":
            spend = random.uniform(5000, 15000)
            impressions = random.randint(15000, 50000)
            clicks = int(impressions * random.uniform(0.015, 0.04))
        else:  # influencers
            spend = random.uniform(2000, 15000)
            impressions = random.randint(10000, 70000)
            clicks = int(impressions * random.uniform(0.005, 0.02))

        conversions = int(clicks * random.uniform(0.02, 0.08))
        revenue = conversions * random.uniform(99, 119)

        marketing_rows.append([
            date.strftime("%Y-%m-%d"),
            channel,
            round(spend, 2),
            impressions,
            clicks,
            conversions,
            round(revenue, 2)
        ])

marketing_df = pd.DataFrame(marketing_rows, columns=[
    "date", "channel", "spend", "impressions", "clicks", "conversions", "revenue"
])


# ---------- 4. COMPETITOR DATA ----------
competitors = ["Huel India", "Zago Protein", "MuscleBlaze Shake"]

updates = [
    "Launched a new flavour",
    "Reduced pricing by 10%",
    "Started influencer campaign",
    "Expanded to new city",
    "Introduced subscription discounts",
]

competitor_rows = []

for comp in competitors:
    price = random.choice([99, 129, 149])
    protein = random.choice([20, 22, 25])
    calories = random.choice([150, 180, 200])
    highlight = random.choice([
        "High protein, low sugar",
        "Best for office workers",
        "Vegan-friendly",
        "Budget fitness drink"
    ])
    update = random.choice(updates)

    competitor_rows.append([comp, price, protein, calories, highlight, update])

competitors_df = pd.DataFrame(competitor_rows, columns=[
    "competitor", "price", "protein", "calories", "highlight", "update"
])


# ---------- SAVE CSV ----------
sales_df.to_csv("data/sales.csv", index=False)
customers_df.to_csv("data/customers.csv", index=False)
marketing_df.to_csv("data/marketing.csv", index=False)
competitors_df.to_csv("data/competitors.csv", index=False)

print("✔ Fake Nutrain data generated successfully!")
