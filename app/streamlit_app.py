"""
Restaurant Business Rankings 2020 – Analytical Dashboard
Professional Streamlit application with top navigation,
Help guide, consistent cards, and guided AI assistant.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Paths & data
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

@st.cache_data
def load_all():
    f50 = pd.read_csv(PROCESSED / "Future50_clean.csv")
    ind = pd.read_csv(PROCESSED / "Independence100_clean.csv")
    top = pd.read_csv(PROCESSED / "Top250_clean.csv")
    return f50, ind, top

# ---------------------------------------------------------------------------
# Page config – hide default sidebar chrome
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RB Rankings 2020 | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# CSS – top nav, consistent cards, help panel, clean theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0a0e17;
    --card: #1a2332;
    --card-hover: #1f2a3d;
    --border: #2a3a4f;
    --accent: #00e5ff;
    --accent-dim: #00b8d4;
    --glow: rgba(0, 229, 255, 0.15);
    --text: #e8edf5;
    --muted: #94a3b8;
    --radius: 12px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #0a0e17 0%, #0d1520 45%, #111827 100%);
}

/* Hide default sidebar completely */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Top header bar */
.top-header {
    background: linear-gradient(90deg, #0d1320 0%, #111827 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.85rem 1.25rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.top-brand {
    font-size: 1.30rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00e5ff, #64ffda);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
    white-space: nowrap;
}
.top-sub {
    color: var(--muted);
    font-size: 0.75rem;
    margin-top: 0.1rem;
}

h1 {
    background: linear-gradient(90deg, #00e5ff, #64ffda);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.25rem !important;
}
h2, h3 { color: var(--text) !important; font-weight: 600 !important; }

/* Metric cards – consistent */
div[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.15rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
div[data-testid="stMetric"]:hover {
    border-color: var(--accent-dim);
    box-shadow: 0 0 18px var(--glow);
}
div[data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-weight: 700 !important;
    font-size: 1.45rem !important;
}

.glow-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    margin: 0.4rem 0 1.25rem 0;
    opacity: 0.55;
}

.insight-box {
    background: linear-gradient(135deg, rgba(0,229,255,0.07), rgba(100,255,218,0.04));
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 0.9rem 1.15rem;
    margin: 0.75rem 0;
    color: var(--text);
    font-size: 0.92rem;
    line-height: 1.45;
}

.help-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}
.help-card h4 {
    color: var(--accent) !important;
    margin: 0 0 0.4rem 0 !important;
    font-size: 0.95rem !important;
}
.help-card p, .help-card li {
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.4;
    margin: 0.2rem 0;
}

/* Equal-height image containers for model visuals */
.model-img-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.75rem;
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
.model-img-wrap img {
    max-height: 260px;
    width: auto;
    object-fit: contain;
}

.footer {
    margin-top: 2rem;
    padding: 1rem 0;
    border-top: 1px solid var(--border);
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
}

/* Buttons */
.stDownloadButton button, .stButton > button {
    background: linear-gradient(135deg, #00b8d4, #00e5ff) !important;
    color: #0a0e17 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stDownloadButton button:hover, .stButton > button:hover {
    box-shadow: 0 0 16px var(--glow) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.4rem;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px 8px 0 0;
    color: var(--muted);
}
.stTabs [aria-selected="true"] {
    border-color: var(--accent-dim) !important;
    color: var(--accent) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: var(--radius);
}

[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1px solid var(--border);
    border-radius: var(--radius);
}

/* Radio as top nav pills */
div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap;
    gap: 0.4rem;
    justify-content: flex-start;
}
div[role="radiogroup"] label {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    padding: 0.35rem 0.9rem !important;
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
div[role="radiogroup"] label[data-checked="true"],
div[role="radiogroup"] label:has(input:checked) {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 12px var(--glow);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Plotly layout
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e8edf5", size=12),
    margin=dict(l=40, r=20, t=48, b=40),
    legend=dict(bgcolor="rgba(26,35,50,0.85)", bordercolor="#2a3a4f"),
    xaxis=dict(gridcolor="#2a3a4f", zerolinecolor="#2a3a4f"),
    yaxis=dict(gridcolor="#2a3a4f", zerolinecolor="#2a3a4f"),
    colorway=["#00e5ff", "#64ffda", "#818cf8", "#f472b6", "#fbbf24", "#34d399", "#f87171"],
)

def style_fig(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

# ---------------------------------------------------------------------------
# AI answers
# ---------------------------------------------------------------------------
def ai_answer(query: str, f50, ind, top) -> str:
    q = query.lower().strip()

    if any(k in q for k in ["top grow", "highest growth", "fastest grow", "best growth", "top yoy"]):
        if "future" in q or "50" in q:
            t = f50.nlargest(5, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M"]]
            lines = [f"{r.Rank}. **{r.Restaurant}** — {r.YOY_Sales_pct:.1f}% YOY (${r.Sales_M}M)" for r in t.itertuples()]
            return "**Future 50 – Top 5 by sales growth**\n\n" + "\n".join(lines)
        t = top.nlargest(5, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M", "Segment_Standard"]]
        lines = [f"{r.Rank}. **{r.Restaurant}** — {r.YOY_Sales_pct:.1f}% (${r.Sales_M}M) · {r.Segment_Standard}" for r in t.itertuples()]
        return "**Top 250 – Top 5 by sales growth**\n\n" + "\n".join(lines)

    if any(k in q for k in ["declin", "worst growth", "negative", "losing", "bottom"]):
        t = top.nsmallest(5, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M"]]
        lines = [f"{r.Rank}. **{r.Restaurant}** — {r.YOY_Sales_pct:.1f}% (${r.Sales_M}M)" for r in t.itertuples()]
        return "**Top 250 – Steepest sales declines**\n\n" + "\n".join(lines)

    if any(k in q for k in ["largest", "biggest", "top sales", "highest sales", "most sales"]):
        if "independent" in q or "independence" in q:
            t = ind.nlargest(5, "Sales_M")[["Rank", "Restaurant", "Sales_M", "City", "State"]]
            lines = [f"{r.Rank}. **{r.Restaurant}** — ${r.Sales_M:.1f}M · {r.City}, {r.State}" for r in t.itertuples()]
            return "**Independence 100 – Top 5 by sales**\n\n" + "\n".join(lines)
        t = top.nlargest(5, "Sales_M")[["Rank", "Restaurant", "Sales_M", "Units"]]
        lines = [f"{r.Rank}. **{r.Restaurant}** — ${r.Sales_M:,.0f}M · {r.Units:,} units" for r in t.itertuples()]
        return "**Top 250 – Top 5 by system sales**\n\n" + "\n".join(lines)

    if "segment" in q or "category" in q:
        seg = top["Segment_Standard"].value_counts().head(8)
        lines = [f"• {k}: {v} chains" for k, v in seg.items()]
        avg = top.groupby("Segment_Standard")["YOY_Sales_pct"].mean().sort_values(ascending=False).head(5)
        lines2 = [f"• {k}: **{v:.1f}%** avg YOY" for k, v in avg.items()]
        return "**Segment counts (top 8)**\n\n" + "\n".join(lines) + "\n\n**Best average growth segments**\n\n" + "\n".join(lines2)

    if "franchise" in q:
        yes = int(f50["Is_Franchised"].sum())
        pct = f50["Is_Franchised"].mean() * 100
        avg_y = f50.groupby("Is_Franchised")["YOY_Sales_pct"].mean()
        return (
            f"**Future 50 – Franchising**\n\n"
            f"• Franchised: **{yes}/50** ({pct:.0f}%)\n"
            f"• Avg YOY sales (franchised): **{avg_y.get(True, 0):.1f}%**\n"
            f"• Avg YOY sales (company-owned): **{avg_y.get(False, 0):.1f}%**"
        )

    if any(k in q for k in ["state", "city", "where", "location", "geography", "geo"]):
        states = ind["State"].value_counts().head(6)
        lines = [f"• {k}: {v} restaurants" for k, v in states.items()]
        return "**Independence 100 – Top states**\n\n" + "\n".join(lines)

    if "chicken" in q:
        chick = top[top["Segment_Standard"].str.contains("Chicken", case=False, na=False)]
        t = chick.nlargest(5, "YOY_Sales_pct")[["Restaurant", "YOY_Sales_pct", "Sales_M"]]
        lines = [f"• **{r.Restaurant}**: {r.YOY_Sales_pct:.1f}% (${r.Sales_M}M)" for r in t.itertuples()]
        return f"**Chicken-related chains in Top 250** ({len(chick)} total)\n\nTop by growth:\n" + "\n".join(lines)

    if any(k in q for k in ["summary", "overview", "insight", "key finding", "tell me about", "what is", "highlight"]):
        return (
            "**Quick highlights from the 2020 rankings**\n\n"
            "• **Future 50** – Emerging concepts; median ~25% sales growth; 58% franchised.\n"
            "• **Independence 100** – Top independents average ~$17.8M sales; concentrated in NY, IL, CA, NV, FL, DC.\n"
            "• **Top 250** – Growth is mixed: many chains flat or down; standouts include Chicken Salad Chick, "
            "First Watch, Shake Shack, and Raising Cane’s.\n"
            "• Strongest segment growth on average: chicken, selected fast-casual, steak, and sports bars.\n\n"
            "Pick another topic from the dropdown, or type a restaurant name."
        )

    if "how many" in q:
        if "future" in q:
            return f"There are **{len(f50)}** concepts in Future 50."
        if "independent" in q or "independence" in q:
            return f"There are **{len(ind)}** restaurants in Independence 100."
        if "top" in q or "250" in q:
            return f"There are **{len(top)}** chains in Top 250."
        return f"Future 50: {len(f50)} · Independence 100: {len(ind)} · Top 250: {len(top)}"

    # Restaurant name lookup
    for df, label in [(top, "Top 250"), (f50, "Future 50"), (ind, "Independence 100")]:
        for rest in df["Restaurant"].dropna().unique():
            if rest.lower() in q or (len(rest) > 4 and rest.lower().split()[0] in q):
                row = df[df["Restaurant"] == rest].iloc[0]
                if label == "Top 250":
                    return (
                        f"**{rest}** (Top 250 #{int(row['Rank'])})\n\n"
                        f"• Sales: **${row['Sales_M']:,.0f}M**\n"
                        f"• YOY sales growth: **{row['YOY_Sales_pct']:.1f}%**\n"
                        f"• Units: **{int(row['Units']):,}**\n"
                        f"• Segment: {row['Segment_Standard']}"
                    )
                if label == "Future 50":
                    return (
                        f"**{rest}** (Future 50 #{int(row['Rank'])})\n\n"
                        f"• Sales: **${row['Sales_M']}M**\n"
                        f"• YOY sales growth: **{row['YOY_Sales_pct']:.1f}%**\n"
                        f"• Units: **{int(row['Units'])}**\n"
                        f"• Franchising: {row['Franchising']}\n"
                        f"• Location: {row.get('Location', '—')}"
                    )
                return (
                    f"**{rest}** (Independence 100 #{int(row['Rank'])})\n\n"
                    f"• Sales: **${row['Sales_M']:.1f}M**\n"
                    f"• Average check: **${row['Avg_Check']}**\n"
                    f"• Meals served: **{int(row['Meals_Served']):,}**\n"
                    f"• Location: {row['City']}, {row['State']}"
                )

    return (
        "I can help with growth leaders, declining chains, segments, franchising, "
        "states, chicken concepts, overall highlights, or a specific restaurant name.\n\n"
        "Use the **dropdown** above for ready-made questions, or type your own."
    )

def to_csv_download(df, filename, label="Download CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label=label, data=csv, file_name=filename, mime="text/csv", use_container_width=True)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
f50, ind, top = load_all()

# ---------------------------------------------------------------------------
# TOP NAVIGATION (header)
# ---------------------------------------------------------------------------
st.markdown("""
<div class="top-header">
  <div>
    <div class="top-brand">Restaurant Business Ranking 2020</div>
    <div class="top-sub"> Analytical Dashboard · Descriptive & Predictive Modelling</div>
  </div>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "Overview",
    "Top 250",
    "Independence 100",
    "Future 50",
    "Growth & Models",
    "AI Assistant",
    "Export",
    "Help Guide",
]

page = st.radio(
    "Navigation",
    nav_options,
    horizontal=True,
    label_visibility="collapsed",
    key="main_nav",
)

st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

# ===========================================================================
# OVERVIEW
# ===========================================================================
if page == "Overview":
    st.markdown("# Overview")
    st.caption("A clear snapshot of the three 2020 restaurant rankings.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Top 250 chains", f"{len(top)}")
    c2.metric("Independents", f"{len(ind)}")
    c3.metric("Future 50 concepts", f"{len(f50)}")
    c4.metric("High growth (≥10%) in Top 250", f"{(top['YOY_Sales_pct'] >= 10).sum()}")

    st.markdown("### Highlights")
    a, b = st.columns(2)
    with a:
        st.markdown("""
        <div class="insight-box">
        <strong>Growth is uneven in Top 250</strong><br>
        Many large chains were flat or down. A smaller group — including chicken and selected fast-casual brands — posted strong gains.
        </div>
        <div class="insight-box">
        <strong>Chicken concepts stand out</strong><br>
        Quick-service and fast-casual chicken segments show some of the best average growth. Raising Cane’s and Chicken Salad Chick are clear examples.
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="insight-box">
        <strong>Future 50 = rapid expansion</strong><br>
        These emerging brands grow much faster than the large-chain average. Most are franchised and still relatively small in system sales.
        </div>
        <div class="insight-box">
        <strong>Independents cluster in big cities</strong><br>
        Top independent restaurants are concentrated in destination markets: New York, Illinois, California, Nevada, Florida, and Washington DC.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Snapshot charts")
    c1, c2 = st.columns(2)
    with c1:
        band_counts = top["Sales_Growth_Band"].value_counts().reindex(
            ["High (≥20%)", "Moderate (5–20%)", "Low (0–5%)", "Negative"]
        ).fillna(0)
        fig = px.bar(
            x=band_counts.index, y=band_counts.values,
            labels={"x": "Growth band", "y": "Number of chains"},
            title="Top 250 – Sales growth bands",
            color=band_counts.values,
            color_continuous_scale=["#f87171", "#fbbf24", "#34d399", "#00e5ff"],
        )
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        top10 = top.nlargest(10, "Sales_M")
        fig = px.bar(
            top10, y="Restaurant", x="Sales_M", orientation="h",
            title="Top 250 – Largest chains by system sales ($M)",
            color="Sales_M", color_continuous_scale="Tealgrn",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

# ===========================================================================
# TOP 250
# ===========================================================================
elif page == "Top 250":
    st.markdown("# Top 250")
    st.caption("Largest U.S. restaurant chains by system sales — filter, explore, and download.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        segments = sorted(top["Segment_Standard"].dropna().unique())
        sel_seg = st.multiselect("Segment", segments, default=[])
    with f2:
        bands = ["High (≥20%)", "Moderate (5–20%)", "Low (0–5%)", "Negative"]
        sel_band = st.multiselect("Growth band", bands, default=[])
    with f3:
        lo, hi = float(top["Sales_M"].min()), float(top["Sales_M"].max())
        sales_range = st.slider("Sales range ($M)", lo, hi, (lo, hi))

    filtered = top.copy()
    if sel_seg:
        filtered = filtered[filtered["Segment_Standard"].isin(sel_seg)]
    if sel_band:
        filtered = filtered[filtered["Sales_Growth_Band"].isin(sel_band)]
    filtered = filtered[(filtered["Sales_M"] >= sales_range[0]) & (filtered["Sales_M"] <= sales_range[1])]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Chains shown", len(filtered))
    m2.metric("Median sales ($M)", f"{filtered['Sales_M'].median():,.0f}" if len(filtered) else "—")
    m3.metric("Median YOY %", f"{filtered['YOY_Sales_pct'].median():.1f}" if len(filtered) else "—")
    m4.metric("% high growth (≥10%)", f"{(filtered['YOY_Sales_pct']>=10).mean()*100:.0f}%" if len(filtered) else "—")

    t1, t2, t3 = st.tabs(["Table", "Charts", "Leaders"])
    with t1:
        cols = ["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Units", "YOY_Units_pct", "Segment_Standard", "Sales_Growth_Band"]
        st.dataframe(filtered[cols].sort_values("Rank"), use_container_width=True, height=400)
        to_csv_download(filtered[cols], "top250_filtered.csv", "Download filtered data")
    with t2:
        a, b = st.columns(2)
        with a:
            fig = px.scatter(
                filtered, x="Units", y="Sales_M", color="Sales_Growth_Band",
                hover_name="Restaurant", size="Sales_M",
                title="Units vs sales (by growth band)", log_x=True, log_y=True,
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with b:
            seg_avg = filtered.groupby("Segment_Standard")["YOY_Sales_pct"].mean().sort_values().tail(12)
            fig = px.bar(
                x=seg_avg.values, y=seg_avg.index, orientation="h",
                title="Average YOY sales % by segment",
                labels={"x": "Avg YOY %", "y": ""},
                color=seg_avg.values, color_continuous_scale="Tealgrn",
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)
    with t3:
        a, b = st.columns(2)
        with a:
            st.markdown("**Top 10 by sales**")
            st.dataframe(
                filtered.nlargest(10, "Sales_M")[["Rank", "Restaurant", "Sales_M", "YOY_Sales_pct", "Segment_Standard"]],
                use_container_width=True, hide_index=True,
            )
        with b:
            st.markdown("**Top 10 by YOY growth**")
            st.dataframe(
                filtered.nlargest(10, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M", "Segment_Standard"]],
                use_container_width=True, hide_index=True,
            )

# ===========================================================================
# INDEPENDENCE 100
# ===========================================================================
elif page == "Independence 100":
    st.markdown("# Independence 100")
    st.caption("Top independent restaurants by sales — explore by state and download.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    states = sorted(ind["State"].dropna().unique())
    sel_states = st.multiselect("State", states, default=[])
    filtered = ind[ind["State"].isin(sel_states)] if sel_states else ind.copy()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Restaurants", len(filtered))
    m2.metric("Avg sales ($M)", f"{filtered['Sales_M'].mean():.1f}" if len(filtered) else "—")
    m3.metric("Avg check ($)", f"{filtered['Avg_Check'].mean():.0f}" if len(filtered) else "—")
    m4.metric("Avg meals (thousands)", f"{filtered['Meals_Served'].mean()/1000:.0f}" if len(filtered) else "—")

    t1, t2 = st.tabs(["Table", "Charts"])
    with t1:
        cols = ["Rank", "Restaurant", "Sales_M", "Avg_Check", "Meals_Served", "City", "State"]
        st.dataframe(filtered[cols].sort_values("Rank"), use_container_width=True, height=400)
        to_csv_download(filtered[cols], "independence100_filtered.csv", "Download filtered data")
    with t2:
        a, b = st.columns(2)
        with a:
            fig = px.scatter(
                filtered, x="Avg_Check", y="Sales_M", size="Meals_Served",
                hover_name="Restaurant", color="State",
                title="Average check vs sales (size = meals served)",
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with b:
            st_counts = filtered["State"].value_counts().head(10)
            fig = px.bar(
                x=st_counts.values, y=st_counts.index, orientation="h",
                title="Top states by count",
                labels={"x": "Count", "y": "State"},
                color=st_counts.values, color_continuous_scale="Tealgrn",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)

# ===========================================================================
# FUTURE 50
# ===========================================================================
elif page == "Future 50":
    st.markdown("# Future 50")
    st.caption("Emerging high-growth concepts — filter by franchising and explore growth.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    franchise_filter = st.radio("Franchising", ["All", "Yes", "No"], horizontal=True)
    filtered = f50.copy()
    if franchise_filter == "Yes":
        filtered = filtered[filtered["Is_Franchised"] == True]
    elif franchise_filter == "No":
        filtered = filtered[filtered["Is_Franchised"] == False]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Concepts", len(filtered))
    m2.metric("Median YOY sales %", f"{filtered['YOY_Sales_pct'].median():.1f}" if len(filtered) else "—")
    m3.metric("Avg units", f"{filtered['Units'].mean():.0f}" if len(filtered) else "—")
    m4.metric("% franchised", f"{filtered['Is_Franchised'].mean()*100:.0f}%" if len(filtered) else "—")

    t1, t2 = st.tabs(["Table", "Charts"])
    with t1:
        cols = ["Rank", "Restaurant", "Location", "Sales_M", "YOY_Sales_pct", "Units",
                "YOY_Units_pct", "Unit_Volume_Avg", "Franchising", "Sales_Growth_Band"]
        st.dataframe(filtered[cols].sort_values("Rank"), use_container_width=True, height=400)
        to_csv_download(filtered[cols], "future50_filtered.csv", "Download filtered data")
    with t2:
        a, b = st.columns(2)
        with a:
            fig = px.scatter(
                filtered, x="Sales_M", y="YOY_Sales_pct", color="Is_Franchised",
                size="Units", hover_name="Restaurant",
                title="Sales vs YOY growth (size = units)",
                color_discrete_map={True: "#00e5ff", False: "#f472b6"},
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)
        with b:
            fig = px.histogram(
                filtered, x="Unit_Volume_Avg", nbins=12,
                title="Unit volume distribution",
                color_discrete_sequence=["#00e5ff"],
            )
            st.plotly_chart(style_fig(fig), use_container_width=True)
        st.markdown("**Fastest growers in this view**")
        st.dataframe(
            filtered.nlargest(8, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M", "Units", "Franchising"]],
            use_container_width=True, hide_index=True,
        )

# ===========================================================================
# GROWTH & MODELS
# ===========================================================================
elif page == "Growth & Models":
    st.markdown("# Growth & Models")
    st.caption("What drives growth, and what a simple predictive model can (and cannot) explain.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <strong>What the model does</strong><br>
    It estimates whether a Top 250 chain is likely to achieve strong sales growth (YOY ≥ 10%) using only structural information available in the ranking: sales size, unit count, sales per unit, and segment. Performance is modest by design — growth depends on many factors beyond size and category.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Model ROC-AUC (logistic)", "0.65")
    c2.metric("Cross-validated F1 (forest)", "0.31")
    c3.metric("Share of high-growth chains", "17.6%")

    st.markdown("### Strongest signals in the data")
    st.markdown("""
    - **Higher sales per unit** tends to go with better growth odds  
    - **Fast-casual burger, chicken, and sandwich** segments lean positive  
    - Several traditional casual-dining and family-casual segments lean weaker  
    """)

    seg_stats = (
        top.groupby("Segment_Standard")
        .agg(count=("Restaurant", "count"), avg_yoy=("YOY_Sales_pct", "mean"))
        .query("count >= 5")
        .sort_values("avg_yoy", ascending=True)
    )
    fig = px.bar(
        x=seg_stats["avg_yoy"], y=seg_stats.index, orientation="h",
        title="Average YOY sales growth by segment (segments with 5+ chains)",
        labels={"x": "Avg YOY sales %", "y": ""},
        color=seg_stats["avg_yoy"], color_continuous_scale="RdYlGn",
    )
    fig.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
    fig.update_layout(coloraxis_showscale=False, height=500)
    st.plotly_chart(style_fig(fig), use_container_width=True)

    a, b = st.columns(2)
    with a:
        st.markdown("**Highest YOY sales growth**")
        st.dataframe(
            top.nlargest(8, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M", "Segment_Standard"]],
            use_container_width=True, hide_index=True,
        )
    with b:
        st.markdown("**Steepest declines**")
        st.dataframe(
            top.nsmallest(8, "YOY_Sales_pct")[["Rank", "Restaurant", "YOY_Sales_pct", "Sales_M", "Segment_Standard"]],
            use_container_width=True, hide_index=True,
        )

    st.markdown("### Model evaluation visuals")
   
    imgs = [
        ("top250_confusion_matrices.png", "Confusion matrices"),
        ("top250_feature_importance.png", "Feature importance"),
        ("top250_roc_curve.png", "ROC curve"),
    ]
    cols = st.columns(3)
    for col, (name, title) in zip(cols, imgs):
        path = REPORTS / name
        with col:
            st.markdown(f"**{title}**")
            if path.exists():
                st.image(str(path), use_container_width=True)
            else:
                st.info("Image not found")

# ===========================================================================
# AI ASSISTANT – guided dropdown + optional free text
# ===========================================================================
elif page == "AI Assistant":
    st.markdown("# AI Assistant")
    st.caption("Ask questions about the rankings — pick a ready-made topic or type your own.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <strong>How to use</strong><br>
    1. Choose a question from the dropdown (easiest), <em>or</em><br>
    2. Type a restaurant name or your own question in the chat box below.<br>
    Answers always come from the live ranking data on this dashboard.
    </div>
    """, unsafe_allow_html=True)

    SUGGESTIONS = {
        "— Select a question —": None,
        "Show overall highlights": "key insights summary",
        "Top growers in Top 250": "top growers in Top250",
        "Top growers in Future 50": "top growers in Future50",
        "Steepest declining chains": "declining chains Top250",
        "Largest chains by sales": "largest chains by sales",
        "Largest independent restaurants": "largest independents by sales",
        "Which segments are growing?": "segment growth performance",
        "Franchising in Future 50": "franchising Future50",
        "Top states for independents": "top states geography",
        "Chicken-related chains": "chicken chains growth",
        "How many restaurants in each list?": "how many in each ranking",
    }

    pick = st.selectbox("Quick questions", list(SUGGESTIONS.keys()), index=0)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I’m here to help you explore the rankings.\n\n"
                    "Use the **dropdown** for common questions, or type a restaurant name "
                    "(for example *Shake Shack* or *Raising Cane’s*) in the box below."
                ),
            }
        ]

    # Fire suggested question
    if pick and SUGGESTIONS[pick]:
        if st.button("Ask this question", type="primary", use_container_width=False):
            q = SUGGESTIONS[pick]
            st.session_state.chat_history.append({"role": "user", "content": pick})
            ans = ai_answer(q, f50, ind, top)
            st.session_state.chat_history.append({"role": "assistant", "content": ans})

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Or type a restaurant name / your own question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        answer = ai_answer(prompt, f50, ind, top)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    if st.button("Clear conversation"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Conversation cleared. Pick a question from the dropdown or type a new one."}
        ]
        st.rerun()

# ===========================================================================
# EXPORT
# ===========================================================================
elif page == "Export":
    st.markdown("# Export")
    st.caption("Download cleaned data and a short insight summary.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    st.markdown("### Cleaned datasets")
    c1, c2, c3 = st.columns(3)
    with c1:
        to_csv_download(top, "Top250_clean.csv", "Top 250")
    with c2:
        to_csv_download(ind, "Independence100_clean.csv", "Independence 100")
    with c3:
        to_csv_download(f50, "Future50_clean.csv", "Future 50")

    st.markdown("### Insight summary")
    summary_text = f"""Restaurant Business Rankings 2020 – Insight Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

TOP 250
- Chains: {len(top)}
- High growth (≥10% YOY): {(top['YOY_Sales_pct']>=10).sum()} ({(top['YOY_Sales_pct']>=10).mean()*100:.1f}%)
- Negative growth: {(top['YOY_Sales_pct']<0).sum()}
- Top grower: {top.loc[top['YOY_Sales_pct'].idxmax(), 'Restaurant']} ({top['YOY_Sales_pct'].max():.1f}%)
- Largest by sales: {top.loc[top['Sales_M'].idxmax(), 'Restaurant']} (${top['Sales_M'].max():,.0f}M)

INDEPENDENCE 100
- Restaurants: {len(ind)}
- Average sales: ${ind['Sales_M'].mean():.1f}M
- Average check: ${ind['Avg_Check'].mean():.0f}
- Top state: {ind['State'].value_counts().index[0]}

FUTURE 50
- Concepts: {len(f50)}
- Median YOY sales: {f50['YOY_Sales_pct'].median():.1f}%
- Franchised: {f50['Is_Franchised'].mean()*100:.0f}%
- Top grower: {f50.loc[f50['YOY_Sales_pct'].idxmax(), 'Restaurant']} ({f50['YOY_Sales_pct'].max():.1f}%)

THEMES
- Growth is uneven among large chains; chicken and selected fast-casual segments lead.
- Future 50 concepts grow much faster; franchising is common.
- Independents concentrate in major destination metros.
"""
    st.download_button(
        "Download insight summary (.txt)",
        data=summary_text.encode("utf-8"),
        file_name="RB_2020_insight_summary.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ===========================================================================
# HELP GUIDE
# ===========================================================================
elif page == "Help Guide":
    st.markdown("# Help Guide")
    st.caption("How to use this dashboard and what the numbers mean — in plain language.")
    st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

    st.markdown("### How to navigate")
    st.markdown("""
    <div class="help-card">
    <h4>Top menu</h4>
    <p>Use the buttons at the top of the page to move between sections:
    Overview, Top 250, Independence 100, Future 50, Growth & Models, AI Assistant, Export, and this Help Guide.</p>
    </div>
    <div class="help-card">
    <h4>Filters</h4>
    <p>On explorer pages you can narrow the list by segment, growth band, sales range, state, or franchising.
    KPI cards and charts update to match your filters. Use <strong>Download filtered data</strong> to save the current view.</p>
    </div>
    <div class="help-card">
    <h4>AI Assistant</h4>
    <p>Open <strong>AI Assistant</strong>, pick a ready-made question from the dropdown, and click <em>Ask this question</em>.
    You can also type a restaurant name or a short free-text question. Answers always use the data in this app.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### What the rankings mean")
    st.markdown("""
    <div class="help-card">
    <h4>Top 250</h4>
    <p>The largest restaurant chains in the U.S. by system sales (company-owned + franchised).
    Useful for comparing scale, growth, and segment performance among big brands.</p>
    </div>
    <div class="help-card">
    <h4>Independence 100</h4>
    <p>High-performing independent (or small multi-unit) restaurants ranked by sales.
    Useful for understanding destination restaurants and city-level concentration.</p>
    </div>
    <div class="help-card">
    <h4>Future 50</h4>
    <p>Emerging concepts with strong recent growth. They are usually smaller in total sales
    than Top 250 chains but expand much faster. Many use franchising.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### KPI and field glossary")
    st.markdown("""
    <div class="help-card">
    <h4>Sales / Sales_M</h4>
    <p><strong>System sales</strong> in millions of dollars (Top 250 and Future 50) or full dollars converted to millions (Independence 100).
    Higher = larger brand or restaurant.</p>
    </div>
    <div class="help-card">
    <h4>YOY Sales % (YOY_Sales_pct)</h4>
    <p><strong>Year-over-year sales growth</strong>. Positive means sales rose versus the prior year; negative means sales fell.
    Example: 15% means sales grew about 15%.</p>
    </div>
    <div class="help-card">
    <h4>Units / YOY Units %</h4>
    <p><strong>Units</strong> = number of locations. <strong>YOY Units %</strong> = change in location count versus the prior year.
    Growing unit counts often support sales growth for expanding brands.</p>
    </div>
    <div class="help-card">
    <h4>Unit volume (Future 50)</h4>
    <p>Approximate average sales per location. Higher unit volume often means stronger individual restaurant performance.</p>
    </div>
    <div class="help-card">
    <h4>Average check (Independence 100)</h4>
    <p>Typical amount a guest spends per visit. Higher checks often mean more premium dining; lower checks often mean higher volume.</p>
    </div>
    <div class="help-card">
    <h4>Meals served (Independence 100)</h4>
    <p>Estimated number of meals/covers in the ranking period — a measure of volume.</p>
    </div>
    <div class="help-card">
    <h4>Segment / Segment_Standard</h4>
    <p>Category of the concept (for example Quick Service & Burger, Casual Dining & Steak, Fast Casual & Chicken).
    Used to compare similar types of restaurants.</p>
    </div>
    <div class="help-card">
    <h4>Growth band</h4>
    <p>Simple grouping of YOY sales growth:<br>
    • High ≥ 20% &nbsp;·&nbsp; Moderate 5–20% &nbsp;·&nbsp; Low 0–5% &nbsp;·&nbsp; Negative &lt; 0%</p>
    </div>
    <div class="help-card">
    <h4>Franchising / Is_Franchised</h4>
    <p>Whether the concept uses franchising (Yes) or is mainly company-operated (No). Common in Future 50.</p>
    </div>
    <div class="help-card">
    <h4>High growth (models)</h4>
    <p>For modelling we label a Top 250 chain as “high growth” when YOY sales growth is at least 10%.
    The model tries to estimate that label from size and segment only — useful as a signal, not a guarantee.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Tips")
    st.markdown("""
    <div class="help-card">
    <h4>Get the most from the dashboard</h4>
    <ul>
    <li>Start on <strong>Overview</strong> for the big picture.</li>
    <li>Use filters on each ranking page, then download the filtered table.</li>
    <li>Compare segments on <strong>Growth & Models</strong>.</li>
    <li>Use the <strong>AI Assistant</strong> dropdown when you want a fast answer without writing a question.</li>
    <li>Use <strong>Export</strong> for full datasets and a text summary you can share.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer (no phase numbers)
# ---------------------------------------------------------------------------
st.markdown("""
<div class="footer">
Restaurant Business Rankings 2020 · Analytical Dashboard · Python & Streamlit<br>
Data-driven insights · Cleaned rankings · Interactive exploration
</div>
""", unsafe_allow_html=True)
