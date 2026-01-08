## 📄 sales.csv — Historical Sales Dataset (2024)

### Purpose
Acts as the canonical source of truth for Nutrain’s realized revenue and demand behavior in 2024. This dataset anchors all profitability, growth, and operational analyses in actual sales outcomes.

### Granularity
Daily data at the intersection of:
- Product
- Region (city-level)
- Sales channel 

Each row represents one product–region–channel combination for a given day.

### Key Fields
- `date`: Calendar day of sale 
- `product`: Product SKU / variant 
- `region`: City-level market 
- `channel`: Fulfillment or sales channel (e.g., Amazon, Website, Gyms) 
- `units_sold`: Units sold for that slice 
- `revenue`: Gross revenue generated (₹ INR) 
- `CAC`: Blended per-unit customer acquisition cost (directional, not campaign-level)

### Design Notes
- Denormalized structure chosen to maximize analytical flexibility. 
- Revenue is deterministic (units × price); no refunds or discounts modeled. 
- CAC is an allocated estimate used for unit economics and profitability analysis, not marketing attribution. 
- Channels represent fulfillment paths, not traffic acquisition sources.

### Role in AUTO
Provides the foundational revenue layer that enables AUTO to:
- Detect fake growth vs real profitability 
- Compare product, region, and channel performance 
- Ground all executive reasoning in verifiable historical data 

This dataset is intentionally static to establish baseline business behavior before introducing live, evolving data streams.

