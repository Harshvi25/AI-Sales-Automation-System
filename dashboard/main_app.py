import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import sqlite3
import pandas as pd

from ai_engine.intent_classifier import predict_intent
from ai_engine.response_generator import generate_response
from ai_engine.lead_extractor import extract_lead_info
from ai_engine.lead_scorer import score_lead

from crm.database import save_lead

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI WhatsApp Sales System",
    page_icon="💬",
    layout="wide",
)

# -----------------------------------
# CSS — WhatsApp Dark + Analytics
# -----------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ══ Tokens ══ */
:root {
    --wa-dark:      #111B21;
    --wa-panel:     #202C33;
    --wa-surface:   #2A3942;
    --wa-bubble-in: #202C33;
    --wa-bubble-out:#005C4B;
    --wa-border:    #2A3942;
    --wa-green:     #00A884;
    --wa-green-lt:  #25D366;
    --wa-teal:      #53BDEB;
    --hot:          #FF6B6B;
    --medium:       #FFD93D;
    --low:          #6BCB77;
    --muted:        #8696A0;
    --text:         #E9EDEF;
    --subtext:      #8696A0;
    --font:         'Outfit', sans-serif;
    --mono:         'IBM Plex Mono', monospace;
}

/* ══ Global reset ══ */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--wa-dark) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ══ Scrollbar ══ */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--wa-surface); border-radius: 4px; }

/* ══════════════════════════════════
   TOPBAR
══════════════════════════════════ */
.topbar {
    background: var(--wa-panel);
    border-bottom: 1px solid var(--wa-border);
    padding: 0.75rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.topbar-avatar {
    width: 40px; height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--wa-green), #1a7a60);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
    box-shadow: 0 0 0 2px rgba(0,168,132,0.3);
}
.topbar-info { flex: 1; }
.topbar-name {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.topbar-status {
    font-size: 0.72rem;
    color: var(--wa-green-lt);
    display: flex;
    align-items: center;
    gap: 0.35rem;
    margin-top: 1px;
}
.pulse-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--wa-green-lt);
    box-shadow: 0 0 6px var(--wa-green-lt);
    animation: blink 2s infinite;
    display: inline-block;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.topbar-badge {
    background: rgba(0,168,132,0.15);
    border: 1px solid rgba(0,168,132,0.35);
    color: var(--wa-green-lt);
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ══════════════════════════════════
   LEFT CHAT PANEL
══════════════════════════════════ */

/* Phone strip */
.phone-strip {
    background: var(--wa-panel);
    border-bottom: 1px solid var(--wa-border);
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.phone-icon { font-size: 0.85rem; color: var(--muted); }
.phone-label {
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    white-space: nowrap;
}

/* Override phone input */
[data-testid="stTextInput"] {
    margin: 0 !important;
}
[data-testid="stTextInput"] > div { margin: 0 !important; }
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: var(--wa-green-lt) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    padding: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextInput"] input:focus {
    box-shadow: none !important;
    border: none !important;
}
[data-testid="stTextInput"] label { display: none !important; }

/* Chat scroll window */
.chat-bg {
    background: var(--wa-dark);
    background-image:
        radial-gradient(circle at 20% 50%, rgba(0,168,132,0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(83,189,235,0.02) 0%, transparent 50%);
    padding: 1rem 1.2rem;
}

/* Message bubbles */
.msg-wrap { display: flex; margin-bottom: 0.6rem; animation: pop 0.2s ease; }
@keyframes pop { from{opacity:0;transform:scale(0.97) translateY(5px);} to{opacity:1;transform:none;} }
.msg-wrap.user { justify-content: flex-end; }
.msg-wrap.bot  { justify-content: flex-start; }

.bubble {
    max-width: 75%;
    border-radius: 12px;
    padding: 0.6rem 0.9rem;
    font-size: 0.85rem;
    line-height: 1.55;
    position: relative;
}
.bubble.user {
    background: var(--wa-bubble-out);
    border-bottom-right-radius: 3px;
    color: #E9EDEF;
}
.bubble.bot {
    background: var(--wa-bubble-in);
    border-bottom-left-radius: 3px;
    color: #E9EDEF;
    border: 1px solid rgba(255,255,255,0.04);
}
.bubble-time {
    font-size: 0.62rem;
    color: rgba(255,255,255,0.35);
    text-align: right;
    margin-top: 0.3rem;
}

/* Lead chips inside bot bubble */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.65rem;
    padding-top: 0.65rem;
    border-top: 1px solid rgba(255,255,255,0.07);
}
.chip {
    border-radius: 6px;
    padding: 0.25rem 0.55rem;
    font-size: 0.68rem;
    font-weight: 600;
    font-family: var(--mono);
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    white-space: nowrap;
}
.chip.intent  { color: var(--wa-teal); }
.chip.hot     { color: var(--hot); background: rgba(255,107,107,0.1); border-color: rgba(255,107,107,0.25); }
.chip.medium  { color: var(--medium); background: rgba(255,217,61,0.1); border-color: rgba(255,217,61,0.25); }
.chip.low     { color: var(--low); background: rgba(107,203,119,0.1); border-color: rgba(107,203,119,0.25); }
.chip.score   { color: #B39DDB; background: rgba(179,157,219,0.1); border-color: rgba(179,157,219,0.25); }
.chip.esc-yes { color: var(--hot); }
.chip.esc-no  { color: var(--low); }

/* Override chat input */
[data-testid="stChatInput"] {
    background: var(--wa-panel) !important;
    border-top: 1px solid var(--wa-border) !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--wa-surface) !important;
    border: none !important;
    border-radius: 24px !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-size: 0.875rem !important;
    padding: 0.7rem 1.1rem !important;
}

/* Streamlit chat_message wrapper — remove default styles */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
}
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    display: none !important;
}

/* ══════════════════════════════════
   RIGHT DASHBOARD PANEL
══════════════════════════════════ */
.dash-header {
    background: var(--wa-panel);
    border-bottom: 1px solid var(--wa-border);
    padding: 0.95rem 1.3rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--subtext);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    padding: 0.9rem;
}
.mcard {
    background: var(--wa-panel);
    border: 1px solid var(--wa-border);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.mcard:hover { transform: translateY(-2px); }
.mcard::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 12px 12px 0 0;
}
.mcard.total::after  { background: linear-gradient(90deg,#53BDEB,#1a90c4); }
.mcard.hot::after    { background: linear-gradient(90deg,#FF6B6B,#ff4040); }
.mcard.medium::after { background: linear-gradient(90deg,#FFD93D,#ffaa00); }
.mcard.low::after    { background: linear-gradient(90deg,#6BCB77,#35a844); }
.mcard-label {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--subtext);
    margin-bottom: 0.4rem;
}
.mcard-value {
    font-family: var(--mono);
    font-size: 2rem;
    font-weight: 500;
    line-height: 1;
}
.mcard.total  .mcard-value { color: #53BDEB; }
.mcard.hot    .mcard-value { color: var(--hot); }
.mcard.medium .mcard-value { color: var(--medium); }
.mcard.low    .mcard-value { color: var(--low); }
.mcard-icon {
    position: absolute;
    right: 0.9rem; top: 50%;
    transform: translateY(-50%);
    font-size: 1.6rem;
    opacity: 0.1;
}

/* Section label */
.section-lbl {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--subtext);
    padding: 0 0.9rem 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-lbl::after {
    content:'';
    flex:1;
    height:1px;
    background: var(--wa-border);
}

/* Bar chart */
.bar-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.25rem 0.9rem;
    font-size: 0.75rem;
}
.bar-label { width: 70px; color: var(--subtext); font-size: 0.72rem; }
.bar-track {
    flex: 1;
    height: 8px;
    background: var(--wa-surface);
    border-radius: 6px;
    overflow: hidden;
}
.bar-fill { height: 100%; border-radius: 6px; transition: width 0.6s ease; }
.bar-count { width: 24px; text-align: right; color: var(--text); font-family: var(--mono); font-size: 0.72rem; }

/* Escalation badge */
.esc-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.3);
    color: var(--hot);
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.15rem 0.55rem;
    margin-left: 0.4rem;
}

/* Table styling */
[data-testid="stDataFrame"] {
    border: 1px solid var(--wa-border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Hide default Streamlit metric */
[data-testid="stMetric"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Session State
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# GLOBAL TOPBAR
# -----------------------------------

st.markdown("""
<div class="topbar">
    <div class="topbar-avatar">🤖</div>
    <div class="topbar-info">
        <div class="topbar-name">AI WhatsApp Sales System</div>
        <div class="topbar-status">
            <span class="pulse-dot"></span> AI Engine Online · End-to-end sales automation
        </div>
    </div>
    <div class="topbar-badge">● Live</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Main 2-column layout
# -----------------------------------

left_col, right_col = st.columns([1.2, 1])

# ═══════════════════════════════════
#  LEFT → WhatsApp Chat
# ═══════════════════════════════════

with left_col:

    # Phone strip
    st.markdown("""
    <div class="phone-strip">
        <span class="phone-icon">📱</span>
        <span class="phone-label">To:</span>
    </div>
    """, unsafe_allow_html=True)

    user_phone = st.text_input(
        "Customer Phone Number",
        value="+919999999999",
        label_visibility="collapsed",
    )

    # Chat messages window
    chat_box = st.container(height=460)

    import datetime
    now = datetime.datetime.now().strftime("%I:%M %p")

    with chat_box:
        st.markdown('<div class="chat-bg">', unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;
                        justify-content:center;height:380px;gap:0.6rem;text-align:center;">
                <div style="font-size:3rem;opacity:0.2;">💬</div>
                <div style="font-size:0.85rem;font-weight:600;color:var(--subtext);">
                    No messages yet
                </div>
                <div style="font-size:0.75rem;color:#455A64;max-width:220px;">
                    Enter a customer message below to start the AI pipeline
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                role = msg["role"]

                if role == "user":
                    st.markdown(f"""
                    <div class="msg-wrap user">
                        <div class="bubble user">
                            {msg["content"]}
                            <div class="bubble-time">{now} ✓✓</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    meta = msg.get("meta", {})
                    reply = msg.get("reply", msg.get("content", ""))
                    priority = meta.get("priority", "")
                    score    = meta.get("score", "")
                    intent   = meta.get("intent", "")
                    esc      = meta.get("escalation", False)

                    p_cls = "hot" if "HOT" in priority else ("medium" if "MEDIUM" in priority else "low")
                    e_cls = "esc-yes" if esc else "esc-no"
                    e_lbl = "🚨 Escalated" if esc else "✅ No Escalation"

                    st.markdown(f"""
                    <div class="msg-wrap bot">
                        <div class="bubble bot">
                            <div style="font-size:0.82rem;margin-bottom:0.1rem;
                                        color:var(--wa-green-lt);font-weight:600;">
                                🤖 AI Sales Assistant
                            </div>
                            {reply}
                            <div class="chip-row">
                                <span class="chip intent">🎯 {intent}</span>
                                <span class="chip {p_cls}">🔥 {priority}</span>
                                <span class="chip score">📊 Score: {score}</span>
                                <span class="chip {e_cls}">{e_lbl}</span>
                            </div>
                            <div class="bubble-time">{now}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    user_message = st.chat_input("Type customer message...")

    # ── Process message ──
    if user_message:

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        intent         = predict_intent(user_message)
        extracted_data = extract_lead_info(user_message)
        lead_result    = score_lead(intent, extracted_data)
        auto_reply     = generate_response(intent)
        escalation     = lead_result["priority"] == "HOT LEAD"

        save_lead(user_phone, user_message, intent, extracted_data, lead_result, escalation)

        st.session_state.messages.append({
            "role": "assistant",
            "reply": auto_reply,
            "meta": {
                "intent":     intent,
                "priority":   lead_result["priority"],
                "score":      lead_result["lead_score"],
                "escalation": escalation,
            }
        })

        st.rerun()

# ═══════════════════════════════════
#  RIGHT → Dashboard
# ═══════════════════════════════════

with right_col:

    # Database
    conn = sqlite3.connect("database/leads.db")
    df   = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()

    total_leads  = len(df)
    hot_leads    = len(df[df["priority"] == "HOT LEAD"])
    medium_leads = len(df[df["priority"] == "MEDIUM LEAD"])
    low_leads    = len(df[df["priority"] == "LOW LEAD"])
    escalated_df = df[df["escalation_required"] == "True"]
    esc_count    = len(escalated_df)

    # ── Dash header ──
    st.markdown('<div class="dash-header">📊 Sales Intelligence</div>', unsafe_allow_html=True)

    # ── Metric cards ──
    st.markdown(f"""
    <div class="metric-grid">
        <div class="mcard total">
            <div class="mcard-label">Total Leads</div>
            <div class="mcard-value">{total_leads}</div>
            <div class="mcard-icon">📈</div>
        </div>
        <div class="mcard hot">
            <div class="mcard-label">Hot Leads</div>
            <div class="mcard-value">{hot_leads}</div>
            <div class="mcard-icon">🔥</div>
        </div>
        <div class="mcard medium">
            <div class="mcard-label">Medium</div>
            <div class="mcard-value">{medium_leads}</div>
            <div class="mcard-icon">⚡</div>
        </div>
        <div class="mcard low">
            <div class="mcard-label">Low Leads</div>
            <div class="mcard-value">{low_leads}</div>
            <div class="mcard-icon">🌱</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Lead distribution bar chart ──
    def pct(n): return round((n / total_leads * 100) if total_leads > 0 else 0)

    st.markdown('<div class="section-lbl" style="margin-top:0.5rem;">Lead Distribution</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding-bottom:0.6rem;">
        <div class="bar-row">
            <div class="bar-label">🔥 Hot</div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{pct(hot_leads)}%;background:var(--hot);"></div>
            </div>
            <div class="bar-count">{hot_leads}</div>
        </div>
        <div class="bar-row">
            <div class="bar-label">⚡ Medium</div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{pct(medium_leads)}%;background:var(--medium);"></div>
            </div>
            <div class="bar-count">{medium_leads}</div>
        </div>
        <div class="bar-row">
            <div class="bar-label">🌱 Low</div>
            <div class="bar-track">
                <div class="bar-fill" style="width:{pct(low_leads)}%;background:var(--low);"></div>
            </div>
            <div class="bar-count">{low_leads}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Escalated leads table ──
    st.markdown(f"""
    <div class="section-lbl" style="margin-top:0.4rem;">
        🚨 Escalated Leads
        <span class="esc-badge">{esc_count} urgent</span>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        escalated_df,
        use_container_width=True,
        hide_index=True,
        height=160,
    )

    # ── All CRM records ──
    st.markdown('<div class="section-lbl" style="margin-top:0.8rem;">📋 CRM Lead Records</div>', unsafe_allow_html=True)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=200,
    )