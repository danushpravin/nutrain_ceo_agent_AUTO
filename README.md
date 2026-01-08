┌──────────────────────────────┐
│        YOU (CEO / User)      │
│  (Streamlit Chat UI - app.py)│
└───────────────┬──────────────┘
                │
                │  User Question
                ▼
┌──────────────────────────────┐
│        agent.py (BRAIN)      │
│  - System Prompt (AI COS)   │
│  - Chat History / Memory   │
│  - Tool Selection Logic    │
└───────────────┬──────────────┘
                │
                │  1️⃣ First LLM Call
                │  → "Which tool(s) do I need?"
                ▼
┌──────────────────────────────┐
│        OPENAI LLM            │
│  - Reads System Prompt      │
│  - Reads Your Question      │
│  - Sees Available Tools     │
│  - Decides Tool Calls       │
└───────────────┬──────────────┘
                │
                │  Tool Call(s)
                │  e.g.:
                │  → tool_roas_by_channel
                │  → tool_churn_rate
                ▼
┌──────────────────────────────┐
│     execute_tool() (agent.py)│
│  - Dispatches tool name     │
│  - Calls tools.py function │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│        tools.py (ADAPTER)   │
│  - Calls analytics.py      │
│  - Converts DF → JSON      │
│  - Returns dict / list     │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│     analytics.py (BI CORE)  │
│  - Opens CSV with Pandas   │
│  - Computes real metrics  │
│  - Returns DataFrames     │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│        data/*.csv           │
│  - sales.csv                │
│  - customers.csv           │
│  - marketing.csv           │
└──────────────────────────────┘

🔁 FULL RUNTIME FLOW (STEP-BY-STEP)
✅ STEP 1 — You Type a Question (UI Layer)

From Streamlit (app.py):

response = run_ceo_agent(st.session_state.messages)


Example question:

"Where am I losing money?"

This becomes:

conversation = [
  {"role": "user", "content": "Where am I losing money?"}
]

✅ STEP 2 — agent.py Adds the CEO Identity (Brain Setup)
messages = [
  {"role": "system", "content": SYSTEM_PROMPT},
  {"role": "user", "content": "Where am I losing money?"}
]


This tells the LLM:

You are the AI Chief of Staff

You must use real tools

You must not hallucinate

You must give strategic advice

✅ STEP 3 — FIRST LLM CALL: “Which tools should I use?”
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=OPENAI_TOOLS,
    tool_choice="auto",
)


The LLM now mentally does:

“To find money leaks, I need:

Churn rate

ROAS by channel”

So it returns:

tool_calls = [
  { name: "tool_churn_rate", arguments: "{}" },
  { name: "tool_roas_by_channel", arguments: "{}" }
]

✅ STEP 4 — Python Executes Each Tool

Inside this block:

result = execute_tool(func, args)


This calls:

agent.py → tools.py → analytics.py → CSV file


Example:

tool_roas_by_channel
→ roas_by_channel(_marketing_df)
→ computes ROAS
→ returns DataFrame
→ converted to JSON

✅ STEP 5 — Tool Results Are Injected Back into Chat

This is what the LLM now sees:

{
  "role": "tool",
  "name": "tool_roas_by_channel",
  "content": [
    {"channel": "Instagram", "ROAS": 0.94},
    {"channel": "Google", "ROAS": 0.56},
    {"channel": "Influencers", "ROAS": 0.43}
  ]
}


and

{
  "role": "tool",
  "name": "tool_churn_rate",
  "content": {"churn_rate": 0.246}
}

✅ STEP 6 — SECOND LLM CALL: “Interpret the Numbers”

Now the LLM sees:

Original question

Its own tool calls

REAL computed data

Then it reasons:

Churn is high → customer loss

Google + Influencers ROAS < 1 → losing money

And replies:

“You are losing money due to high churn and inefficient Google & Influencer ads…”

✅ This is pure CEO reasoning on real data.

✅ STEP 7 — Final Answer Goes Back to UI

Streamlit displays the final response in chat bubbles.

🧩 WHO DOES WHAT (CLEAR SEPARATION OF RESPONSIBILITY)
File	Role
data/*.csv	Raw business truth
analytics.py	Math & business KPIs
tools.py	Converts KPIs → JSON
agent.py	Decides what to compute & explains it
app.py	Chat interface
OpenAI LLM	Strategic reasoning & communication

