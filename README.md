# AUTO — Autonomous Executive Intelligence

AUTO is a **deterministic, AI-assisted executive intelligence system** designed to analyze internal business data and generate **founder-level interpretations and recommendations** across growth, profitability, marketing efficiency, inventory, and operational risk.

Unlike traditional LLM dashboards or chatbots, AUTO treats the LLM as a **language and synthesis layer**, not a decision-maker. All conclusions are grounded in structured analytics and explicit rules.

---

## What AUTO Is (and Is Not)

**AUTO is:**
- A modular decision system that operates on structured business data
- Deterministic analytics + probabilistic language synthesis
- Designed to behave like a **central executive layer**, not an assistant

**AUTO is not:**
- A chatbot over CSVs
- A black-box ML predictor
- A generic BI dashboard

---

## High-Level Architecture

AUTO is structured into **four explicit layers**:

Data → Analytics → Interpretation → Recommendation


### 1. Data Layer
- Operates on daily-granularity internal business data
- Currently uses **synthetic but realistic datasets** covering:
  - Sales
  - Marketing
  - Inventory
  - Unit economics
- ~12 months of simulated operations (10k+ rows)

The system is intentionally built to be **data-source agnostic** (real data can replace synthetic data without changing logic).

---

### 2. Analytics Layer (Deterministic)

This layer contains **pure, deterministic functions** that compute facts — not opinions.

Examples:
- Revenue trends and baselines
- Channel-level ROAS, CAC, net profit
- Product revenue concentration
- Inventory stockouts vs revenue impact
- Channel dependency risk
- Growth quality (real vs spend-driven)

Each analytic:
- Accepts a `DataContext`
- Has explicit parameters (e.g. `lookback_days`)
- Returns structured outputs (tables + metrics)

No LLM involvement here.

---

### 3. Interpretation Layer (Tool-Driven)

The interpretation layer:
- Consumes analytics outputs
- Applies **explicit business logic and thresholds**
- Produces:
  - Structured **flags** (type, severity, values)
  - Plain-language **interpretations**

Key design choices:
- Severity is encoded at the analytic level
- Interpretations are explainable and auditable
- Multiple interpretations can coexist without overwriting each other

Example flags:
- `LOW_ROAS`
- `NEGATIVE_OR_LOW_NET_MARGIN`
- `CHANNEL_DEPENDENCY_HIGH`
- `FAKE_GROWTH_SIGNAL`
- `INVENTORY_STOCKOUT_CRITICAL`

---

### 4. Recommendation Layer (LLM-Assisted)

The recommendation layer:
- Uses the LLM **only after interpretation**
- Receives:
  - Flags
  - Interpretations
  - Contextual summaries
- Outputs **actionable recommendations**, not analysis

Design constraints:
- The LLM cannot invent metrics
- The LLM cannot override flags
- Recommendations must map back to identified risks

This ensures the system **reasons before it speaks**.

---

## What Currently Works

### ✅ End-to-End Executive Analysis
AUTO can already generate:
- Executive briefs
- Risk summaries
- Prioritized problem lists
- Action-oriented recommendations

All grounded in analytics.

---

### ✅ Marketing Efficiency Analysis
- Multi-channel ROAS, CAC, net profit
- Spend vs revenue trend comparisons
- Identification of value-destructive channels
- Configurable time windows (30 / 60 / 90 / 180 days)

---

### ✅ Growth Quality Detection
- Differentiates between:
  - Real demand-driven growth
  - Spend-driven or fragile growth
- Uses baseline comparisons and contribution logic

---

### ✅ Product & Channel Concentration Risk
- Detects over-reliance on:
  - Top SKUs
  - Single channels
  - Single regions
- Assigns severity based on concentration thresholds

---

### ✅ Inventory Risk vs Revenue Impact
- Tracks stockouts at SKU-day level
- Quantifies revenue loss during stockout periods
- Flags operational failures with financial impact

---

### ✅ Modular, Extensible Tooling
- Each analytic is isolated and testable
- New tools can be added without breaking the agent
- The agent dynamically selects tools based on query intent

---

### ✅ Deterministic + LLM Hybrid Design
- Analytics are fully deterministic
- LLM is used strictly for:
  - Synthesis
  - Explanation
  - Recommendation phrasing

This avoids hallucination and preserves trust.

---

## Design Principles

- **Determinism before language**
- **Interpretation before recommendation**
- **Severity encoded in logic, not prose**
- **Explainability over cleverness**
- **Executive usefulness over model novelty**

---

## Current Limitations (Intentional)

- Uses simulated data (by design)
- No automated action execution (advisory only)
- No UI beyond a minimal Streamlit interface
- No forecasting models yet (diagnostic first, predictive later)

---

## Why AUTO Exists

Most AI business tools answer questions.

AUTO is designed to **surface problems you didn’t ask about**, rank them by severity, and recommend what to fix first — the way a strong founder or operator would.

---

## Status

**Active development (v2)**  
Focus areas:
- Scenario stress testing
- Memory across time windows
- Improved prioritization logic
- Cleaner agent–tool contracts
