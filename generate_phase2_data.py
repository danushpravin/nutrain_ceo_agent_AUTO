import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -------------------------
# BASE CONFIG
# -------------------------

products = [
    "Nutrain Vanilla",
    "Nutrain Choco Coffee",
    "Nutrain Banana Oats"
]

channels = ["Instagram", "Google", "Influencers"]

customer_segments = ["Student", "Working Professional", "Gym-goer"]

start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365)]

# =====================================================
# 🚫 DISABLED: INVENTORY DATA (already generated)
# =====================================================
# inventory_rows = []
# for date in dates:
#     for product in products:
#         opening_stock = random.randint(8000, 15000)
#         units_produced = random.randint(2000, 6000)
#         units_sold = random.randint(1500, 6500)
#
#         closing_stock = max(opening_stock + units_produced - units_sold, 0)
#         stockout_flag = "Yes" if closing_stock < 1000 else "No"
#
#         inventory_rows.append([
#             date.strftime("%Y-%m-%d"),
#             product,
#             opening_stock,
#             units_produced,
#             units_sold,
#             closing_stock,
#             stockout_flag
#         ])
#
# inventory_df = pd.DataFrame(inventory_rows, columns=[
#     "date", "product", "opening_stock", "units_produced",
#     "units_sold", "closing_stock", "stockout_flag"
# ])
# inventory_df.to_csv("data/inventory.csv", index=False)

# =====================================================
# 🚫 DISABLED: UNIT ECONOMICS DATA (already generated)
# =====================================================
# unit_economics_rows = []
#
# price_map = {
#     "Nutrain Vanilla": 180,
#     "Nutrain Choco Coffee": 190,
#     "Nutrain Banana Oats": 170
# }
#
# for product in products:
#     selling_price = price_map[product]
#     cogs = random.randint(70, 95)
#     gross_margin = selling_price - cogs
#     packaging_cost = random.randint(8, 15)
#     logistics_cost = random.randint(8, 14)
#
#     unit_economics_rows.append([
#         product,
#         selling_price,
#         cogs,
#         gross_margin,
#         packaging_cost,
#         logistics_cost
#     ])
#
# unit_econ_df = pd.DataFrame(unit_economics_rows, columns=[
#     "product", "selling_price", "cogs",
#     "gross_margin", "packaging_cost", "logistics_cost"
# ])
# unit_econ_df.to_csv("data/unit_economics.csv", index=False)

# =====================================================
# 🚫 DISABLED: PROMOTIONS DATA (already generated)
# =====================================================
# promotion_rows = []
#
# promo_campaigns = ["Monsoon Sale", "Fitness Week", "New Year Boost", "Summer Shred"]
#
# for _ in range(80):
#     date = random.choice(dates)
#     product = random.choice(products)
#     campaign = random.choice(promo_campaigns)
#     discount_pct = random.choice([5, 10, 15, 20])
#     channel = random.choice(channels)
#     revenue_lift = random.randint(50000, 450000)
#
#     promotion_rows.append([
#         date.strftime("%Y-%m-%d"),
#         product,
#         campaign,
#         discount_pct,
#         channel,
#         revenue_lift
#     ])
#
# promo_df = pd.DataFrame(promotion_rows, columns=[
#     "date", "product", "campaign",
#     "discount_pct", "channel", "revenue_lift"
# ])
# promo_df.to_csv("data/promotions.csv", index=False)

# =====================================================
# ✅ ACTIVE: CUSTOMER SEGMENTS DATA (LOGIC FIXED)
# =====================================================

segment_rows = []

for i in range(1200):
    customer_id = f"C{i+1000}"
    segment = random.choice(customer_segments)
    age_group = random.choice(["18–24", "25–34", "35–44"])

    # ✅ LOGICAL RULE:
    # If segment is Gym-goer, gym_member MUST be Yes
    if segment == "Gym-goer":
        gym_member = "Yes"
    else:
        gym_member = random.choice(["Yes", "No"])

    monthly_spend = random.randint(499, 3499)

    segment_rows.append([
        customer_id,
        segment,
        age_group,
        gym_member,
        monthly_spend
    ])

segment_df = pd.DataFrame(segment_rows, columns=[
    "customer_id", "segment",
    "age_group", "gym_member",
    "monthly_spend"
])

segment_df.to_csv("data/customer_segments.csv", index=False)

print("✅ Customer сегments data regenerated with correct logic.")

