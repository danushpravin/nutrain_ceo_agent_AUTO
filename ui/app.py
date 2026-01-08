import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.agent import run_ceo_agent



st.set_page_config(page_title="AUTO", layout="wide")

# ---------- Session Memory ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Global Clean Styling ----------
st.markdown("""
<style>
body {
    background: #FAFAFA;
}

.stChatMessage {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 14px;
    border: 1px solid rgba(0,0,0,0.06);
}

.stChatInputContainer textarea {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    color: #0B0B0B !important;
    font-size: 16px !important;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid rgba(0,0,0,0.08);
}

.stMarkdown {
    color: #0B0B0B;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h2 style="
font-weight:600;
letter-spacing:2px;
margin-bottom:0;
">
AUTO
</h2>

<p style="
margin-top:0;
font-size:13px;
letter-spacing:1px;
opacity:0.6;">
Autonomous executive intelligence
</p>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("### System")
st.sidebar.markdown("**Status:** Online")
st.sidebar.markdown("**Mode:** Autonomous")
st.sidebar.markdown("**Currency:** ₹ INR")

if st.sidebar.button("Reset Memory"):
    st.session_state.messages = []
    st.rerun()
    
if "auto_brief_shown" not in st.session_state:
    st.session_state.auto_brief_shown = True

    with st.spinner("AUTO initializing..."):
        brief = run_ceo_agent([
            {"role": "user", "content": "Generate today’s executive brief."}
        ])

    with st.chat_message("assistant"):
        st.markdown(brief)



# ---------- Chat History ----------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ---------- Input ----------
query = st.chat_input("Command AUTO")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Processing"):
        response = run_ceo_agent(st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

