import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# =========================
# CONFIG (WORLD RULES)
# =========================

PRODUCTS = ["Nutrain Vanilla", "Nutrain Choco Coffee", "Nutrain Banana Oats"]
REGIONS = ["Bangalore", "Mumbai", "Delhi", "Chennai"]
CHANNELS = ["Instagram", "Google", "Influencers"]

UNIT_ECON = {
    "Nutrain Vanilla": {"selling_price": 180},
    "Nutrain Choco Coffee": {"selling_price": 190},
    "Nutrain Banana Oats": {"selling_price": 170},
}

BASE_DAILY_DEMAND = {
    "Nutrain Vanilla": 120,
    "Nutrain Choco Coffee": 90,
    "Nutrain Banana Oats": 60,
}

# Region demand share (must sum to 1.0)
REGION_W = {
    "Bangalore": 0.28,
    "Mumbai": 0.30,
    "Delhi": 0.22,
    "Chennai": 0.20,
}

# Channel share (must sum to 1.0)
CHANNEL_W = {
    "Instagram": 0.40,
    "Google": 0.38,
    "Influencers": 0.22,
}

# Marketing channel behavior (for funnel + efficiency)
CHANNEL_BEHAVIOR = {
    "Instagram": {"ctr": (0.008, 0.018), "cvr": (0.015, 0.030), "cpc": (4.0, 8.0)},
    "Google": {"ctr": (0.020, 0.050), "cvr": (0.030, 0.060), "cpc": (12.0, 28.0)},
    "Influencers": {"ctr": (0.004, 0.012), "cvr": (0.010, 0.025), "cpc": (6.0, 18.0)},
}

# Inventory rules
STARTING_STOCK = 150  # per product
PRODUCTION_RANGE = {
    "Nutrain Vanilla": (105, 135),
    "Nutrain Choco Coffee": (80, 105),
    "Nutrain Banana Oats": (55, 75),
}

# Noise range (stable)
DEMAND_NOISE = (0.85, 1.15)
START_DATE = None
# =========================
# HELPERS
# =========================

def _safe_int(x: float) -> int:
    return int(max(0, round(x)))

def _alloc(total: int, weights: dict, rng: np.random.Generator) -> dict:
    """Integer allocation of total across keys by weights."""
    keys = list(weights.keys())
    w = np.array([weights[k] for k in keys], dtype=float)
    w = w / w.sum()
    raw = rng.multinomial(total, w)
    return {k: int(v) for k, v in zip(keys, raw)}

def simulate_day(date: datetime, stock_state: dict, rng: np.random.Generator):
    """
    Returns:
      sales_day_df, marketing_day_df, inventory_day_df, updated_stock_state
    """

    # 1) Demand (per product)
    product_demand = {}
    for p in PRODUCTS:
        noise = rng.uniform(*DEMAND_NOISE)
        product_demand[p] = _safe_int(BASE_DAILY_DEMAND[p] * noise)

    # 2) Inventory: produce first
    inventory_rows = []
    produced_today = {}
    for p in PRODUCTS:
        opening = stock_state.get(p, STARTING_STOCK)
        prod_lo, prod_hi = PRODUCTION_RANGE[p]
        produced = int(rng.integers(prod_lo, prod_hi + 1))
        if rng.random() < 0.12:  # 12% of days
            produced = int(produced * rng.uniform(0.2, 0.5))

        produced_today[p] = produced

        inventory_rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "product": p,
            "opening_stock": opening,
            "units_produced": produced,
            "units_dispatched": 0,   # fill after sales
            "closing_stock": opening + produced,  # temp, update later
            "lost_demand": 0,
            "stockout_flag": "No",
        })

    inventory_df = pd.DataFrame(inventory_rows)

    # 3) Sales allocation by region+channel, capped by inventory
    sales_rows = []
    for p in PRODUCTS:
        available = int(inventory_df.loc[inventory_df["product"] == p, "closing_stock"].iloc[0])
        demand = product_demand[p]
        actual_sold = min(demand, available)
        lost_demand = max(0, demand - available)

        # allocate across regions then channels
        region_alloc = _alloc(actual_sold, REGION_W, rng)
        for r, units_r in region_alloc.items():
            channel_alloc = _alloc(units_r, CHANNEL_W, rng)
            for c, units in channel_alloc.items():
                price = UNIT_ECON[p]["selling_price"]
                revenue = units * price
                sales_rows.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "product": p,
                    "region": r,
                    "channel": c,
                    "units_sold": units,
                    "revenue": revenue,
                    "CAC": None,  # fill after marketing computes CAC per channel
                })

        # update inventory dispatched + closing
        idx = inventory_df.index[inventory_df["product"] == p][0]
        inventory_df.at[idx, "units_dispatched"] = actual_sold
        closing = int(inventory_df.at[idx, "opening_stock"] + inventory_df.at[idx, "units_produced"] - actual_sold)
        inventory_df.at[idx, "closing_stock"] = closing
        inventory_df.at[idx, "lost_demand"] = lost_demand
        inventory_df.at[idx, "stockout_flag"] = "Yes" if closing <= 0 else "No"

        # update state
        stock_state[p] = closing

    sales_df = pd.DataFrame(sales_rows)

    # 4) Marketing (per channel) — revenue attributed from sales by channel
    marketing_rows = []
    revenue_by_channel = sales_df.groupby("channel")["revenue"].sum().to_dict()

    for c in CHANNELS:
        channel_rev = float(revenue_by_channel.get(c, 0.0))

        # spend derived from desired ROAS-ish behavior (but noisy)
        # Spend proportional to revenue capture, with channel inefficiency baked in
        # Google tends to burn more.
        ineff = {"Instagram": (0.18, 0.28), "Google": (0.30, 0.55), "Influencers": (0.28, 0.60)}[c]
        spend = channel_rev * rng.uniform(*ineff)
        spend = float(max(0.0, round(spend, 2)))

        beh = CHANNEL_BEHAVIOR[c]
        ctr = rng.uniform(*beh["ctr"])
        cvr = rng.uniform(*beh["cvr"])
        cpc = rng.uniform(*beh["cpc"])

        clicks = _safe_int(spend / cpc) if spend > 0 else 0
        impressions = _safe_int(clicks / ctr) if ctr > 0 else 0
        conversions = _safe_int(clicks * cvr)

        marketing_rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "channel": c,
            "spend": spend,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "revenue": channel_rev,
        })

    marketing_df = pd.DataFrame(marketing_rows)

    # 5) CAC injection into sales rows (per channel-day CAC)
    cac_by_channel = {}
    for _, row in marketing_df.iterrows():
        conv = float(row["conversions"])
        spend = float(row["spend"])
        cac = (spend / conv) if conv > 0 else None
        cac_by_channel[row["channel"]] = cac

    sales_df["CAC"] = sales_df["channel"].map(cac_by_channel)

    return sales_df, marketing_df, inventory_df, stock_state


def generate_range(start_date: str, end_date: str, seed: int = 42):
    """
    Generates inclusive date range data.
    """
    rng = np.random.default_rng(seed)
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    stock_state = {p: STARTING_STOCK for p in PRODUCTS}

    all_sales = []
    all_marketing = []
    all_inventory = []

    cur = start
    while cur <= end:
        s, m, i, stock_state = simulate_day(cur, stock_state, rng)
        all_sales.append(s)
        all_marketing.append(m)
        all_inventory.append(i)
        cur += timedelta(days=1)

    return (
        pd.concat(all_sales, ignore_index=True),
        pd.concat(all_marketing, ignore_index=True),
        pd.concat(all_inventory, ignore_index=True),
    )


def write_outputs(sales_df, marketing_df, inventory_df, out_dir="data"):
    out = Path(out_dir)
    out.mkdir(exist_ok=True, parents=True)

    sales_path = out / "sales.csv"
    marketing_path = out / "marketing.csv"
    inventory_path = out / "inventory.csv"

    sales_df.to_csv(sales_path, index=False)
    marketing_df.to_csv(marketing_path, index=False)
    inventory_df.to_csv(inventory_path, index=False)

    print("✅ Wrote:")
    print(f" - {sales_path} ({len(sales_df):,} rows)")
    print(f" - {marketing_path} ({len(marketing_df):,} rows)")
    print(f" - {inventory_path} ({len(inventory_df):,} rows)")
    
def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists() and path.stat().st_size > 0:
        return pd.read_csv(path)
    return pd.DataFrame()

def simulate_next_day(data_dir="data", seed=None):
    rng = np.random.default_rng(seed)

    data_dir = Path(data_dir)
    sales_path = data_dir / "sales.csv"
    marketing_path = data_dir / "marketing.csv"
    inventory_path = data_dir / "inventory.csv"

    # --- Load existing data ---
    sales_df = read_csv_if_exists(sales_path)
    inventory_df = read_csv_if_exists(inventory_path)

    if sales_df.empty or inventory_df.empty:
        raise RuntimeError("❌ Cannot simulate next day without historical data.")

    # --- Determine last date ---
        # --- Determine last date ---
    sales_df["date"] = pd.to_datetime(sales_df["date"])
    inventory_df["date"] = pd.to_datetime(inventory_df["date"])

    global START_DATE
    if START_DATE is None:
        START_DATE = inventory_df["date"].min().to_pydatetime()


    last_date = sales_df["date"].max()
    next_date = last_date + timedelta(days=1)

    day_seed = (
        hash((seed, next_date.strftime("%Y-%m-%d"))) % (2**32)
        if seed is not None else None
    )

    rng = np.random.default_rng(day_seed)

    # --- Reconstruct stock state from last inventory snapshot ---
    
    last_inventory = (
        inventory_df.sort_values("date")
        .groupby("product")
        .tail(1)
    )

    stock_state = {
        row["product"]: int(row["closing_stock"])
        for _, row in last_inventory.iterrows()
    }

    # --- Simulate one day ---
    s, m, i, _ = simulate_day(next_date, stock_state, rng)

    # --- Append ---
    s.to_csv(sales_path, mode="a", header=False, index=False)
    m.to_csv(marketing_path, mode="a", header=False, index=False)
    i.to_csv(inventory_path, mode="a", header=False, index=False)

    print(f"✅ Simulated next business day: {next_date.date()}")


if __name__ == "__main__":
    MODE = "daily"  # "history" or "daily"

    if MODE == "history":
        sales, marketing, inventory = generate_range(
            "2024-01-01", "2024-12-31", seed=7
        )
        write_outputs(sales, marketing, inventory, out_dir="data")

    elif MODE == "daily":
        simulate_next_day(data_dir="data", seed=42)
