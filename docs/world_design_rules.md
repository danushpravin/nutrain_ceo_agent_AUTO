# Nutrain — World Model & Business Simulation Rules

This document defines the **deterministic business rules** used to simulate Nutrain’s internal operations.
All generated data adheres to these constraints so that AUTO (Autonomous Executive Intelligence)
can reason over realistic, causally consistent business behavior.

The goal is not realism for realism’s sake, but **stable patterns, trade-offs, and failure modes**
that enable executive-level reasoning.

---

## 1. Core Entities

### Products
- **Nutrain Vanilla** — Core hero product, stable demand
- **Nutrain Choco Coffee** — High revenue potential, margin risk
- **Nutrain Banana Oats** — Price-sensitive, inventory-constrained

### Channels
- **Instagram** — High reach, low intent
- **Google** — High intent, expensive CAC
- **Influencers** — Bursty, inconsistent, fake-growth risk

### Regions
- **Bangalore** — Early adopters, strong demand
- **Mumbai** — High volume
- **Delhi** — Price sensitive
- **Chennai** — Operationally efficient, steady demand

---

## 2. Unit Economics (Static Ground Truth)

Unit economics are **fixed** and do not change daily unless explicitly modeled later.
AUTO relies on these values to detect fake growth and profit leakage.

| Product | Selling Price (₹) | COGS (₹) | Packaging (₹) | Logistics (₹) |
|------|------|------|------|------|
| Nutrain Vanilla | 180 | 89 | 8 | 8 |
| Nutrain Choco Coffee | 190 | 95 | 10 | 12 |
| Nutrain Banana Oats | 170 | 88 | 8 | 14 |

Cost per unit = COGS + Packaging + Logistics

---

## 3. Demand Model

Demand is **product-driven first**, then modulated by channel and region.

### Base Daily Demand
- Nutrain Vanilla: 120 units
- Nutrain Choco Coffee: 90 units
- Nutrain Banana Oats: 60 units

### Daily Noise
To avoid flat curves and allow organic variation:

```text
true_demand = base_demand × random_noise
random_noise ∈ [0.85, 1.15]

