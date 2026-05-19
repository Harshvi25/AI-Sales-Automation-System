import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI WhatsApp Sales Dashboard",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------------
# Custom CSS — Dark Premium Theme
# -----------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Reset ── */
:root {
    --bg:        #080C14;
    --surface:   #0E1420;
    --border:    #1C2538;
    --accent:    #00E5FF;
    --hot:       #FF4D6D;
    --medium:    #FFB700;
    --low:       #00C896;
    --muted:     #4A5568;
    --text:      #E2E8F0;
    --subtext:   #8892A4;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1400px;
}

/* ── Hero header ── */
.hero {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.25rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00E5FF 0%, #7B61FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 0.85rem;
    color: var(--subtext);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card.total::before  { background: linear-gradient(90deg, #00E5FF, #7B61FF); }
.metric-card.hot::before    { background: linear-gradient(90deg, #FF4D6D, #FF8C42); }
.metric-card.medium::before { background: linear-gradient(90deg, #FFB700, #FF8C42); }
.metric-card.low::before    { background: linear-gradient(90deg, #00C896, #00E5FF); }

.metric-label {
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--subtext);
    margin-bottom: 0.6rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.metric-card.total  .metric-value { color: #00E5FF; }
.metric-card.hot    .metric-value { color: #FF4D6D; }
.metric-card.medium .metric-value { color: #FFB700; }
.metric-card.low    .metric-value { color: #00C896; }

.metric-icon {
    position: absolute;
    right: 1.4rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2rem;
    opacity: 0.15;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.section-badge {
    background: rgba(255,77,109,0.15);
    color: #FF4D6D;
    border: 1px solid rgba(255,77,109,0.3);
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.15rem 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.section-badge.all {
    background: rgba(0,229,255,0.1);
    color: #00E5FF;
    border-color: rgba(0,229,255,0.25);
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
    margin: 0.5rem 0 1.5rem;
}

/* ── Dataframe overrides ── */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] iframe {
    border-radius: 14px;
}

/* ── Streamlit metric override ── */
[data-testid="stMetric"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Database Connection
# -----------------------------------

conn = sqlite3.connect("database/leads.db")
df = pd.read_sql_query("SELECT * FROM leads", conn)
conn.close()

# -----------------------------------
# Metrics
# -----------------------------------

total_leads  = len(df)
hot_leads    = len(df[df["priority"] == "HOT LEAD"])
medium_leads = len(df[df["priority"] == "MEDIUM LEAD"])
low_leads    = len(df[df["priority"] == "LOW LEAD"])
escalated_df = df[df["escalation_required"] == "True"]

# -----------------------------------
# Hero Header
# -----------------------------------

st.markdown("""
<div class="hero">
    <div>
        <p class="hero-sub">Real-time Intelligence</p>
        <h1 class="hero-title">AI WhatsApp Sales Dashboard</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Metric Cards
# -----------------------------------

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card total">
        <div class="metric-label">Total Leads</div>
        <div class="metric-value">{total_leads}</div>
        <span class="metric-icon">📊</span>
    </div>
    <div class="metric-card hot">
        <div class="metric-label">Hot Leads</div>
        <div class="metric-value">{hot_leads}</div>
        <span class="metric-icon">🔥</span>
    </div>
    <div class="metric-card medium">
        <div class="metric-label">Medium Leads</div>
        <div class="metric-value">{medium_leads}</div>
        <span class="metric-icon">⚡</span>
    </div>
    <div class="metric-card low">
        <div class="metric-label">Low Leads</div>
        <div class="metric-value">{low_leads}</div>
        <span class="metric-icon">🌱</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Escalation Alerts
# -----------------------------------

st.markdown("""
<div class="section-header">
    <span class="section-title">🚨 Escalated Leads</span>
    <span class="section-badge">Needs Attention</span>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

st.dataframe(
    escalated_df,
    use_container_width=True,
    hide_index=True,
)

# -----------------------------------
# All Leads Table
# -----------------------------------

st.markdown("""
<div class="section-header">
    <span class="section-title">📋 All Lead Records</span>
    <span class="section-badge all">Full Database</span>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)