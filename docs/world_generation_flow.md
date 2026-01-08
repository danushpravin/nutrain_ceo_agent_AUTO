DAILY BUSINESS SIMULATION (date t)
─────────────────────────────────

1. Demand Generation
   └─ For each product:
      • Start from BASE_DAILY_DEMAND
      • Apply controlled random noise
      → Final daily demand per product

2. Inventory Production
   └─ For each product:
      • Read opening_stock from previous day
      • Produce units within defined range
      • Compute temporary available_stock

3. Sales Feasibility Check
   └─ actual_sold = min(demand, available_stock)
      • Enforces physical constraints
      • Prevents overselling

4. Sales Allocation
   └─ Two-stage stochastic allocation:
      • Product → Regions (weighted multinomial)
      • Region → Channels (weighted multinomial)
      • Revenue = units_sold × selling_price

5. Inventory State Update
   └─ For each product:
      • units_dispatched = actual_sold
      • closing_stock = opening + produced − sold
      • stockout_flag if closing_stock ≤ 0
      • Persist state for next day

6. Marketing Simulation (per channel)
   └─ Aggregate sales revenue by channel
      • Derive spend using channel inefficiency
      • Simulate funnel:
          impressions → clicks → conversions
      • Record spend and funnel metrics

7. CAC Attribution
   └─ CAC = spend / conversions (per channel-day)
      • Inject CAC back into all sales rows

END OF DAY OUTPUT
─────────────────
• sales_df
• marketing_df
• inventory_df
• updated stock_state (used for next day)

[ Previous Day State ]
        │
        ▼
[ Demand Engine ]
        │
        ▼
[ Inventory Production ]
        │
        ▼
[ Sales Constraint Layer ]
        │
        ▼
[ Allocation Engine ]
  (Region → Channel)
        │
        ▼
[ Revenue Computation ]
        │
        ▼
[ Inventory State Machine ]
        │
        ▼
[ Marketing Funnel Simulator ]
        │
        ▼
[ CAC Attribution Layer ]
        │
        ▼
[ Day t Outputs + State Update ]



