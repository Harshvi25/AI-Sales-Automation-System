import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

from ai_engine.intent_classifier import predict_intent
from ai_engine.response_generator import generate_response
from ai_engine.lead_extractor import extract_lead_info
from ai_engine.lead_scorer import score_lead

from crm.database import save_lead


# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="💬",
    layout="wide",
)

# -----------------------------------
# Global CSS
# -----------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:          #05080F;
    --panel:       #090D17;
    --surface:     #0F1623;
    --border:      #1A2234;
    --border-light:#24304A;
    --accent:      #25D366;
    --accent-glow: rgba(37,211,102,0.15);
    --accent2:     #00B4D8;
    --hot:         #FF4757;
    --medium:      #FFA502;
    --low:         #2ED573;
    --text:        #E8EDF5;
    --subtext:     #6B7A99;
    --user-bubble: #1A3A2A;
    --ai-bubble:   #111827;
    --font:        'Plus Jakarta Sans', sans-serif;
    --mono:        'JetBrains Mono', monospace;
}

/* ─── Reset ─── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ─── Layout shell ─── */
.app-shell {
    display: grid;
    grid-template-columns: 280px 1fr 300px;
    height: 100vh;
    overflow: hidden;
}

/* ─── LEFT SIDEBAR ─── */
.sidebar {
    background: var(--panel);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 0;
    overflow: hidden;
}
.sidebar-brand {
    padding: 1.5rem 1.4rem 1rem;
    border-bottom: 1px solid var(--border);
}
.brand-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.3rem;
}
.brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent), #1DB954);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 4px 14px rgba(37,211,102,0.35);
}
.brand-name {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.02em;
}
.brand-tagline {
    font-size: 0.68rem;
    color: var(--subtext);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding-left: 0.2rem;
}

.sidebar-section {
    padding: 1rem 1.4rem 0.5rem;
}
.sidebar-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--subtext);
    margin-bottom: 0.8rem;
}

/* Phone input custom */
.phone-field {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    font-family: var(--mono);
    font-size: 0.82rem;
    color: var(--accent);
    width: 100%;
    outline: none;
    transition: border-color 0.2s;
}
.phone-field:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
}

.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
    display: inline-block;
    box-shadow: 0 0 8px var(--accent);
    animation: pulse 2s infinite;
    margin-right: 0.4rem;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.online-status {
    font-size: 0.72rem;
    color: var(--accent);
    display: flex;
    align-items: center;
    margin-top: 0.9rem;
}

.sidebar-nav {
    flex: 1;
    padding: 0.5rem 0.8rem;
    overflow-y: auto;
}
.nav-item {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.65rem 0.8rem;
    border-radius: 9px;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--subtext);
    cursor: pointer;
    transition: all 0.15s;
    margin-bottom: 0.15rem;
}
.nav-item:hover { background: var(--surface); color: var(--text); }
.nav-item.active { background: var(--accent-glow); color: var(--accent); }
.nav-icon { font-size: 1rem; width: 20px; text-align: center; }

/* ─── CENTER CHAT ─── */
.chat-area {
    display: flex;
    flex-direction: column;
    background: var(--bg);
    overflow: hidden;
}
.chat-topbar {
    background: var(--panel);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}
.chat-topbar-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
}
.chat-topbar-sub {
    font-size: 0.72rem;
    color: var(--subtext);
    margin-top: 0.1rem;
}
.topbar-badge {
    background: var(--accent-glow);
    color: var(--accent);
    border: 1px solid rgba(37,211,102,0.3);
    border-radius: 20px;
    font-size: 0.67rem;
    font-weight: 700;
    padding: 0.2rem 0.7rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.chat-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem 2rem;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-track { background: transparent; }
.chat-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ─── BUBBLES ─── */
.msg-row {
    display: flex;
    margin-bottom: 1.2rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.avatar.user-av {
    background: linear-gradient(135deg, #3A7BD5, #00D2FF);
    margin-left: 0.7rem;
}
.avatar.ai-av {
    background: linear-gradient(135deg, var(--accent), #1DB954);
    margin-right: 0.7rem;
    box-shadow: 0 2px 10px var(--accent-glow);
}

.bubble {
    max-width: 70%;
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.84rem;
    line-height: 1.6;
}
.bubble.user-bubble {
    background: var(--user-bubble);
    border: 1px solid rgba(37,211,102,0.2);
    border-bottom-right-radius: 4px;
    color: #C8F7D6;
}
.bubble.ai-bubble {
    background: var(--ai-bubble);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
    color: var(--text);
}

/* Lead info inside AI bubble */
.lead-meta {
    margin-top: 0.9rem;
    padding-top: 0.9rem;
    border-top: 1px solid var(--border-light);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}
.lead-chip {
    background: var(--surface);
    border: 1px solid var(--border-light);
    border-radius: 8px;
    padding: 0.45rem 0.65rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.lead-chip-label {
    font-size: 0.62rem;
    color: var(--subtext);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    display: block;
    margin-bottom: 0.1rem;
}
.lead-chip-value {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text);
    font-family: var(--mono);
}
.lead-chip-value.hot    { color: var(--hot); }
.lead-chip-value.medium { color: var(--medium); }
.lead-chip-value.low    { color: var(--low); }
.lead-chip-value.esc-true  { color: var(--hot); }
.lead-chip-value.esc-false { color: var(--low); }

/* Empty state */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--subtext);
    text-align: center;
    gap: 0.8rem;
}
.empty-icon {
    font-size: 3rem;
    opacity: 0.3;
}
.empty-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--subtext);
}
.empty-sub {
    font-size: 0.78rem;
    color: var(--border-light);
    max-width: 240px;
}

/* ─── RIGHT PANEL ─── */
.info-panel {
    background: var(--panel);
    border-left: 1px solid var(--border);
    padding: 1.4rem;
    overflow-y: auto;
}
.info-panel-title {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--subtext);
    margin-bottom: 1rem;
}
.stat-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.65rem;
}
.stat-label {
    font-size: 0.68rem;
    color: var(--subtext);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.stat-value {
    font-family: var(--mono);
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text);
}
.stat-value.green { color: var(--accent); }
.stat-value.red   { color: var(--hot); }
.stat-value.amber { color: var(--medium); }

.pipeline-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--subtext);
    margin: 1.5rem 0 0.8rem;
}
.pipeline-bar {
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 0.4rem;
}
.pipeline-fill {
    height: 6px;
    border-radius: 8px;
    transition: width 0.6s ease;
}

/* ─── Override Streamlit chat_input ─── */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border) !important;
    background: var(--panel) !important;
    padding: 0.8rem 1.5rem !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: var(--font) !important;
    font-size: 0.85rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ─── Override Streamlit text_input ─── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 10px !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
[data-testid="stTextInput"] label {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--subtext) !important;
}

/* ─── Chat message override ─── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Session State
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "stats" not in st.session_state:
    st.session_state.stats = {"total": 0, "hot": 0, "escalated": 0}

# -----------------------------------
# Layout: 3 columns
# -----------------------------------

left, center, right = st.columns([1.1, 3, 1.2])

# ── LEFT SIDEBAR ──
with left:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-logo">
            <div class="brand-icon">💬</div>
            <span class="brand-name">SalesBot AI</span>
        </div>
        <div class="brand-tagline">WhatsApp Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><div class="sidebar-label">Customer</div>', unsafe_allow_html=True)

    user_phone = st.text_input(
        "Phone Number",
        value="+919999999999",
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="online-status">
        <span class="status-dot"></span> AI Engine Online
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-nav">
        <div class="sidebar-label" style="padding: 0.5rem 0.8rem 0.4rem;">Navigation</div>
        <div class="nav-item active"><span class="nav-icon">💬</span> Live Chat</div>
        <div class="nav-item"><span class="nav-icon">📊</span> Dashboard</div>
        <div class="nav-item"><span class="nav-icon">👥</span> Leads CRM</div>
        <div class="nav-item"><span class="nav-icon">🔔</span> Escalations</div>
        <div class="nav-item"><span class="nav-icon">⚙️</span> Settings</div>
    </div>
    """, unsafe_allow_html=True)

# ── CENTER CHAT ──
with center:
    st.markdown("""
    <div style="background:var(--panel);border-bottom:1px solid var(--border);
                padding:1rem 1.4rem;display:flex;align-items:center;
                justify-content:space-between;">
        <div>
            <div style="font-size:0.95rem;font-weight:700;color:var(--text);">
                AI Sales Conversation
            </div>
            <div style="font-size:0.72rem;color:var(--subtext);margin-top:0.1rem;">
                Powered by intent classification + lead scoring
            </div>
        </div>
        <div style="background:var(--accent-glow);color:var(--accent);
                    border:1px solid rgba(37,211,102,0.3);border-radius:20px;
                    font-size:0.67rem;font-weight:700;padding:0.2rem 0.8rem;
                    letter-spacing:0.06em;text-transform:uppercase;">
            ● Live
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages area
    chat_container = st.container(height=480)

    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🤖</div>
                <div class="empty-title">AI Assistant Ready</div>
                <div class="empty-sub">Type a customer message below to start the conversation</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                role = msg["role"]
                if role == "user":
                    with st.chat_message("user"):
                        st.markdown(
                            f'<div style="font-size:0.85rem;line-height:1.6;">{msg["content"]}</div>',
                            unsafe_allow_html=True
                        )
                else:
                    with st.chat_message("assistant"):
                        # Render AI reply + lead chips
                        reply_text = msg.get("reply", "")
                        meta = msg.get("meta", {})
                        priority = meta.get("priority", "")
                        score = meta.get("score", "")
                        intent = meta.get("intent", "")
                        escalation = meta.get("escalation", False)

                        p_class = "hot" if "HOT" in priority else ("medium" if "MEDIUM" in priority else "low")
                        e_class = "esc-true" if escalation else "esc-false"
                        e_label = "⚠️ YES" if escalation else "✅ NO"

                        st.markdown(f"""
                        <div style="font-size:0.85rem;line-height:1.6;margin-bottom:0.3rem;">
                            {reply_text}
                        </div>
                        <div class="lead-meta">
                            <div class="lead-chip">
                                <div>
                                    <div class="lead-chip-label">Intent</div>
                                    <div class="lead-chip-value">🎯 {intent}</div>
                                </div>
                            </div>
                            <div class="lead-chip">
                                <div>
                                    <div class="lead-chip-label">Priority</div>
                                    <div class="lead-chip-value {p_class}">{priority}</div>
                                </div>
                            </div>
                            <div class="lead-chip">
                                <div>
                                    <div class="lead-chip-label">Lead Score</div>
                                    <div class="lead-chip-value">📊 {score}</div>
                                </div>
                            </div>
                            <div class="lead-chip">
                                <div>
                                    <div class="lead-chip-label">Escalation</div>
                                    <div class="lead-chip-value {e_class}">{e_label}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    # Chat input
    user_message = st.chat_input("Type customer message here...")

# ── RIGHT PANEL ──
with right:
    stats = st.session_state.stats
    total = stats["total"]
    hot = stats["hot"]
    escalated = stats["escalated"]

    conversion = round((hot / total * 100) if total > 0 else 0)
    hot_pct = round((hot / total * 100) if total > 0 else 0)

    st.markdown(f"""
    <div class="info-panel-title">Session Stats</div>

    <div class="stat-row">
        <div class="stat-label">Messages Processed</div>
        <div class="stat-value green">{total}</div>
    </div>
    <div class="stat-row">
        <div class="stat-label">Hot Leads Detected</div>
        <div class="stat-value red">{hot}</div>
    </div>
    <div class="stat-row">
        <div class="stat-label">Escalations Triggered</div>
        <div class="stat-value amber">{escalated}</div>
    </div>

    <div class="pipeline-label">Lead Pipeline</div>

    <div style="margin-bottom:0.6rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;
                    color:var(--subtext);margin-bottom:0.3rem;">
            <span>🔥 Hot</span><span>{hot_pct}%</span>
        </div>
        <div style="background:var(--surface);border-radius:8px;overflow:hidden;">
            <div style="height:6px;width:{hot_pct}%;background:var(--hot);
                        border-radius:8px;transition:width 0.6s;"></div>
        </div>
    </div>
    <div style="margin-bottom:0.6rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;
                    color:var(--subtext);margin-bottom:0.3rem;">
            <span>⚡ Medium</span><span>{max(0, 100-hot_pct-20)}%</span>
        </div>
        <div style="background:var(--surface);border-radius:8px;overflow:hidden;">
            <div style="height:6px;width:{max(0, 100-hot_pct-20)}%;background:var(--medium);
                        border-radius:8px;"></div>
        </div>
    </div>
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.72rem;
                    color:var(--subtext);margin-bottom:0.3rem;">
            <span>🌱 Low</span><span>{min(20, 100-hot_pct)}%</span>
        </div>
        <div style="background:var(--surface);border-radius:8px;overflow:hidden;">
            <div style="height:6px;width:{min(20,100-hot_pct)}%;background:var(--low);
                        border-radius:8px;"></div>
        </div>
    </div>

    <div class="info-panel-title" style="margin-top:0.5rem;">AI Engine Status</div>
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:0.9rem 1rem;">
        <div style="font-size:0.75rem;color:var(--subtext);line-height:2;">
            <div>🎯 Intent Classifier &nbsp;<span style="color:var(--accent);font-weight:600;">Active</span></div>
            <div>🧠 Lead Scorer &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--accent);font-weight:600;">Active</span></div>
            <div>📨 Response Gen &nbsp;&nbsp;&nbsp;<span style="color:var(--accent);font-weight:600;">Active</span></div>
            <div>💾 CRM Sync &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:var(--accent);font-weight:600;">Active</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# Process Message
# -----------------------------------

if user_message:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # AI Pipeline
    intent        = predict_intent(user_message)
    extracted_data = extract_lead_info(user_message)
    lead_result   = score_lead(intent, extracted_data)
    auto_reply    = generate_response(intent)
    escalation    = lead_result["priority"] == "HOT LEAD"

    # Save to CRM
    save_lead(user_phone, user_message, intent, extracted_data, lead_result, escalation)

    # Update stats
    st.session_state.stats["total"] += 1
    if lead_result["priority"] == "HOT LEAD":
        st.session_state.stats["hot"] += 1
    if escalation:
        st.session_state.stats["escalated"] += 1

    # Store AI message with structured meta
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