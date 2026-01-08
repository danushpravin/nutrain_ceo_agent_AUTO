import json
from typing import Dict, Any, List
from openai import OpenAI

from . import tools

# ---------------- CONFIG ----------------

MODEL = "gpt-4.1-mini"
client = OpenAI()

# ---------------- TOOL SCHEMAS ----------------

OPENAI_TOOLS = [

    # -------- EXECUTIVE --------
    {
        "type": "function",
        "function": {
            "name": "tool_daily_delta",
            "description": "Today vs yesterday revenue delta.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_revenue_recent_performance",
            "description": "Recent revenue trend vs baseline.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "default": 7}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_top_products",
            "description": "Top products by revenue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "default": 3}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_top_regions",
            "description": "Top regions by revenue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "default": 3}
                },
            },
        },
    },

    # -------- ANALYTICS --------
    {
        "type": "function",
        "function": {
            "name": "tool_sales_by_product",
            "description": "Revenue grouped by product.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_sales_by_region",
            "description": "Revenue grouped by region.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_sales_by_channel",
            "description": "Revenue grouped by channel.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_revenue_by_month",
            "description": "Monthly revenue trend.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_profit_by_product",
            "description": "Profit and margin per product.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_true_profit_by_channel",
            "description": "True net profit by channel.",
            "parameters": {"type": "object", "properties": {}},
        },
    },

    # -------- INTERPRETATION --------
    {
        "type": "function",
        "function": {
            "name": "tool_interpret_growth_quality",
            "description": "Detect whether growth is real or fake.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_marketing_efficiency",
            "description": "Interpret marketing spend efficiency.",
            "parameters": {"type": "object", "properties": {
                "lookback_days": {"type": "integer",
                                  "description": "Number of days to analyze (e.g. 30, 60, 90, 180)",
                                  "default": 30}
            }},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_product_portfolio_health",
            "description": "Assess product portfolio health.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_inventory_health_vs_revenue",
            "description": "Inventory risk vs revenue performance.",
            "parameters": {"type": "object", "properties": {
                "lookback_days": {"type": "integer",
                                  "description": "Number of days to analyze (e.g. 30, 60, 90, 180)",
                                  "default": 30}
            }},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_channel_dependency_risk",
            "description": "Channel concentration and dependency risk.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    # -------- RECOMMENDATION --------
        {
        "type": "function",
        "function": {
            "name": "tool_generate_recommendations",
            "description": (
                "Generate executive recommendations based on interpretation flags "
                "and growth quality signals. Deterministic, data-driven."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

# ---------------- TOOL EXECUTOR ----------------

def execute_tool(name: str, arguments: Dict[str, Any]):
    try:
        func = getattr(tools, name)
        return func(**arguments) if arguments else func()
    except Exception as e:
        return {"error": str(e)}

# ---------------- SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """
You are the AI CEO + Chief Analyst of the company — the operating system of the business.

ABSOLUTE RULES (NON-NEGOTIABLE):
- You ONLY use data returned by internal tools.
- You NEVER invent, estimate, guess, or hallucinate numbers.
- If required data is missing, you explicitly say so and stop.
- You NEVER use external knowledge or assumptions.
- You NEVER mix currencies.

CURRENCY RULES (STRICT):
- ALL monetary values are in Indian Rupees (₹).
- You MUST prefix all monetary values with ₹.
- You MUST NOT use $, USD, or any other currency symbol.
- Currency fields include:
  revenue, profit, net_profit, spend, CAC, total_cost,
  selling_price, cogs, packaging_cost, logistics_cost.
- Counts (units, days, stock, customers, percentages) are NOT currency.

BEHAVIOR:
- You think like a ruthless operator, not a chatbot.
- You interpret facts, surface risks, and expose fragility.
- You prioritize truth over optimism.
- You highlight concentration risk, fake growth, inefficiencies, and breakpoints.
- You do NOT soften bad news.

AUTONOMY:
- You automatically select and call the correct tools.
- You NEVER ask the user for permission to run analysis.
- You NEVER ask “Would you like me to…”.
- You ALWAYS take the next logical analytical step.
- You MUST complete interpretation before making any recommendation.
- Recommendations must always be traceable to explicit flags or signals.


OUTPUT CONSTRAINTS:
- You report facts first.
- You explain implications clearly and concisely.
- You DO NOT give recommendations unless explicitly asked.
- When recommendations are requested, you MUST generate them exclusively via the recommendation tool.
- You MUST NOT generate recommendations directly in text.

- When asked for status, performance, or health, you report:
  • What changed
  • Why it changed (if data supports it)
  • What risk it creates

You are not an assistant.
You are the company’s executive brain.

"""

# ---------------- AGENT LOOP ----------------

def run_ceo_agent(conversation: List[Dict[str, str]]):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append({
                "role": "assistant",
                "tool_calls": msg.tool_calls,
            })

            for call in msg.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments or "{}")
                result = execute_tool(name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": json.dumps(result, default=str),
                })

            continue

        messages.append({"role": "assistant", "content": msg.content})
        return msg.content
