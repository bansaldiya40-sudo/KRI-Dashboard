"""
================================================================================
 BUSINESS KRI (KEY RISK INDICATOR) DASHBOARD
================================================================================
A professional, executive-level Streamlit application for enterprise risk
monitoring. Built with Plotly for all visualizations.

Run with:
    streamlit run app.py

To connect real data, replace `generate_risk_data()` with a loader that
reads from your GRC system, database, or CSV export. The rest of the app
consumes a DataFrame with the same column names, so no other code needs
to change as long as columns match.
================================================================================
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Business KRI Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# Light custom CSS for a cleaner, more "executive" look
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
        div[data-testid="stMetric"] {
            background-color: #f8f9fb;
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            padding: 14px 16px 10px 16px;
        }
        div[data-testid="stMetricLabel"] {font-weight: 600;}
        .risk-alert-box {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 8px;
            border-left: 5px solid;
        }
        .risk-alert-critical {background-color: #fdecea; border-color: #E45756;}
        .risk-alert-warning {background-color: #fff8e6; border-color: #F2B701;}
        .risk-alert-info {background-color: #eaf2fb; border-color: #4C78A8;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Color palette used consistently across all charts
COLOR_MAP = {"Low": "#54A24B", "Medium": "#F2B701", "High": "#E45756"}
LEVEL_ORDER = ["Low", "Medium", "High"]
STATUS_OPTIONS = ["Open", "In Progress", "Mitigated", "Closed", "Overdue"]


# ==============================================================================
# 2. SYNTHETIC DATA GENERATION (cached — replace with real data source)
# ==============================================================================
@st.cache_data
def generate_risk_data(n_rows: int = 2200, seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic synthetic risk register spanning ~2 years.
    Each row represents one tracked risk item with an assessment date,
    impact/probability scoring, ownership, and mitigation status.
    """
    rng = np.random.default_rng(seed)

    departments = ["Finance", "Operations", "IT & Security", "Compliance", "HR", "Sales", "Supply Chain"]
    regions = ["North America", "Europe", "APAC", "Latin America", "Middle East & Africa"]
    categories = [
        "Financial Risk", "Operational Risk", "Cyber Risk", "Compliance Risk",
        "Strategic Risk", "Reputational Risk", "People Risk", "Supply Chain Risk",
    ]
    owners = [
        "A. Sharma", "J. Lee", "M. Fernandez", "S. Patel", "R. Kim", "L. Novak",
        "T. Okafor", "D. Rossi", "C. Nguyen", "E. Müller", "P. Singh", "K. Brown",
    ]
    risk_name_templates = {
        "Financial Risk": ["Currency Exposure", "Budget Overrun", "Cash Flow Shortfall", "Credit Default Risk", "Interest Rate Volatility"],
        "Operational Risk": ["Process Failure", "Equipment Downtime", "Quality Control Gap", "Capacity Constraint", "Vendor Delay"],
        "Cyber Risk": ["Data Breach Exposure", "Phishing Vulnerability", "Unpatched System", "Ransomware Exposure", "Access Control Gap"],
        "Compliance Risk": ["Regulatory Non-Compliance", "License Expiry", "Audit Finding", "Policy Violation", "Reporting Delay"],
        "Strategic Risk": ["Market Share Erosion", "Competitive Disruption", "M&A Integration Risk", "Product Obsolescence", "Brand Positioning Risk"],
        "Reputational Risk": ["Negative Media Coverage", "Customer Complaint Surge", "Social Media Backlash", "ESG Controversy", "Executive Misconduct"],
        "People Risk": ["Key Talent Attrition", "Skills Gap", "Workplace Safety Incident", "Succession Planning Gap", "Employee Engagement Decline"],
        "Supply Chain Risk": ["Single-Source Dependency", "Logistics Disruption", "Raw Material Shortage", "Supplier Insolvency", "Freight Cost Spike"],
    }

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_span = (end_date - start_date).days

    rows = []
    for i in range(n_rows):
        category = rng.choice(categories)
        dept = rng.choice(departments)
        region = rng.choice(regions)
        owner = rng.choice(owners)
        name = f"{rng.choice(risk_name_templates[category])} #{rng.integers(100, 999)}"

        assessed_date = start_date + timedelta(days=int(rng.integers(0, date_span)))

        # Impact & Probability on a 1-5 scale drive the composite risk score
        impact = int(rng.integers(1, 6))
        probability = int(rng.integers(1, 6))
        risk_score = impact * probability  # 1-25 scale

        if risk_score >= 15:
            level = "High"
        elif risk_score >= 7:
            level = "Medium"
        else:
            level = "Low"

        status = rng.choice(STATUS_OPTIONS, p=[0.20, 0.25, 0.25, 0.20, 0.10])

        # Mitigation due dates: some in the past (may be overdue), some future
        due_offset = int(rng.integers(-120, 180))
        mitigation_due = assessed_date + timedelta(days=due_offset)
        is_overdue = (status not in ("Mitigated", "Closed")) and (mitigation_due < datetime(2025, 12, 31)) and due_offset < 0

        mitigation_plans = [
            "Implement additional controls and monitoring",
            "Engage third-party audit for validation",
            "Diversify supplier/vendor base",
            "Deploy automated monitoring tooling",
            "Conduct staff training and awareness program",
            "Escalate to executive risk committee",
            "Renegotiate contractual terms",
            "Increase reserve/contingency allocation",
            "Patch and harden affected systems",
            "Formalize policy and update documentation",
        ]
        mitigation_plan = rng.choice(mitigation_plans)

        compliant = rng.random() > (0.35 if category == "Compliance Risk" else 0.12)

        rows.append(
            {
                "risk_id": f"RSK-{10000 + i}",
                "risk_name": name,
                "department": dept,
                "region": region,
                "owner": owner,
                "category": category,
                "impact": impact,
                "probability": probability,
                "risk_score": risk_score,
                "risk_level": level,
                "status": status,
                "is_overdue": is_overdue,
                "compliant": compliant,
                "assessed_date": assessed_date,
                "mitigation_due": mitigation_due,
                "mitigation_plan": mitigation_plan,
            }
        )

    df = pd.DataFrame(rows)
    df["month"] = df["assessed_date"].values.astype("datetime64[M]")
    df["year"] = df["assessed_date"].dt.year
    df["month_name"] = df["assessed_date"].dt.strftime("%b")
    df["month_num"] = df["assessed_date"].dt.month
    return df


# ==============================================================================
# 3. HELPER FUNCTIONS
# ==============================================================================
def format_number(value: float) -> str:
    """Compact number formatting, e.g. 1,240 -> 1.2K"""
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:,.1f}K"
    return f"{value:,.0f}"


def risk_exposure(frame: pd.DataFrame) -> float:
    """
    A simple monetary-style exposure proxy: risk_score acts as a weight
    on a nominal per-risk base exposure. Swap in real $ exposure data
    if available in your source system.
    """
    base_exposure_per_point = 4200  # nominal $ per risk-score point
    return (frame["risk_score"] * base_exposure_per_point).sum()


def build_month_year_options(frame: pd.DataFrame):
    years = sorted(frame["year"].unique())
    months = list(range(1, 13))
    month_labels = pd.to_datetime([f"2000-{m:02d}-01" for m in months]).strftime("%b").tolist()
    return years, month_labels


# ==============================================================================
# 4. LOAD DATA
# ==============================================================================
raw_df = generate_risk_data()

# ==============================================================================
# 5. SIDEBAR — INTERACTIVE FILTERS
# ==============================================================================
st.sidebar.title("🔎 Filters")

all_years, month_labels = build_month_year_options(raw_df)
selected_years = st.sidebar.multiselect("Year", all_years, default=all_years)
selected_months = st.sidebar.multiselect("Month", month_labels, default=month_labels)

all_departments = sorted(raw_df["department"].unique())
selected_departments = st.sidebar.multiselect("Department", all_departments, default=all_departments)

all_regions = sorted(raw_df["region"].unique())
selected_regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)

all_categories = sorted(raw_df["category"].unique())
selected_categories = st.sidebar.multiselect("Risk Category", all_categories, default=all_categories)

selected_levels = st.sidebar.multiselect("Risk Level", LEVEL_ORDER, default=LEVEL_ORDER)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset all filters"):
    st.rerun()

st.sidebar.caption(
    "Risk Score = Impact (1-5) × Probability (1-5). "
    "Low: 1-6 · Medium: 7-14 · High: 15-25."
)

# ------------------------------------------------------------------------------
# Apply filters
# ------------------------------------------------------------------------------
mask = (
    raw_df["year"].isin(selected_years)
    & raw_df["month_name"].isin(selected_months)
    & raw_df["department"].isin(selected_departments)
    & raw_df["region"].isin(selected_regions)
    & raw_df["category"].isin(selected_categories)
    & raw_df["risk_level"].isin(selected_levels)
)
df = raw_df.loc[mask].copy()

# ==============================================================================
# 6. HEADER
# ==============================================================================
st.title("🛡️ Business KRI Dashboard")
st.caption(
    f"Enterprise risk overview · {len(selected_departments)} department(s) · "
    f"{len(selected_regions)} region(s) · {len(df):,} risk records in view"
)

if df.empty:
    st.warning("No records match the current filters. Try widening your selection.")
    st.stop()

# ==============================================================================
# 7. KPI CARDS
# ==============================================================================
total_risks = len(df)
high_risks = (df["risk_level"] == "High").sum()
medium_risks = (df["risk_level"] == "Medium").sum()
low_risks = (df["risk_level"] == "Low").sum()
overall_risk_score = df["risk_score"].mean()
compliance_pct = df["compliant"].mean() * 100
exposure = risk_exposure(df)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
c1.metric("Total Risks", f"{total_risks:,}")
c2.metric("High Risks", f"{high_risks:,}", f"{high_risks/total_risks*100:.0f}% of total")
c3.metric("Medium Risks", f"{medium_risks:,}", f"{medium_risks/total_risks*100:.0f}% of total")
c4.metric("Low Risks", f"{low_risks:,}", f"{low_risks/total_risks*100:.0f}% of total")
c5.metric("Overall Risk Score", f"{overall_risk_score:.1f} / 25")
c6.metric("Compliance %", f"{compliance_pct:.1f}%")
c7.metric("Risk Exposure", f"${format_number(exposure)}")

st.markdown("---")

# ==============================================================================
# 8. RISK ALERTS
# ==============================================================================
st.subheader("🚨 Risk Alerts")

critical_risks_df = df[(df["risk_level"] == "High") & (~df["status"].isin(["Mitigated", "Closed"]))]
overdue_df = df[df["is_overdue"]]
compliance_issues_df = df[~df["compliant"]]

a1, a2, a3 = st.columns(3)
with a1:
    st.markdown(
        f"<div class='risk-alert-box risk-alert-critical'>"
        f"<b>🔴 Critical Risks (Open High-severity)</b><br>"
        f"<span style='font-size:1.6rem;font-weight:700;'>{len(critical_risks_df):,}</span> "
        f"active risks require immediate attention.</div>",
        unsafe_allow_html=True,
    )
with a2:
    st.markdown(
        f"<div class='risk-alert-box risk-alert-warning'>"
        f"<b>🟠 Overdue Mitigations</b><br>"
        f"<span style='font-size:1.6rem;font-weight:700;'>{len(overdue_df):,}</span> "
        f"mitigation plans have passed their due date.</div>",
        unsafe_allow_html=True,
    )
with a3:
    st.markdown(
        f"<div class='risk-alert-box risk-alert-info'>"
        f"<b>🔵 Compliance Issues</b><br>"
        f"<span style='font-size:1.6rem;font-weight:700;'>{len(compliance_issues_df):,}</span> "
        f"records flagged as non-compliant.</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==============================================================================
# 9. CHARTS — ROW 1: Risk Trend & Distribution
# ==============================================================================
row1_left, row1_right = st.columns([2, 1])

with row1_left:
    st.subheader("📈 Risk Trend Over Time")
    trend = df.groupby("month", as_index=False).agg(risk_count=("risk_id", "count"))
    fig_trend = px.area(
        trend,
        x="month",
        y="risk_count",
        markers=True,
        color_discrete_sequence=["#4C78A8"],
    )
    fig_trend.update_traces(
        hovertemplate="Month: %{x|%b %Y}<br>Risks Logged: %{y}<extra></extra>"
    )
    fig_trend.update_layout(
        xaxis_title="", yaxis_title="Number of Risks",
        margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with row1_right:
    st.subheader("🍩 Risk Distribution")
    dist = df["risk_level"].value_counts().reindex(LEVEL_ORDER).reset_index()
    dist.columns = ["risk_level", "count"]
    fig_donut = px.pie(
        dist, names="risk_level", values="count", hole=0.55,
        color="risk_level", color_discrete_map=COLOR_MAP,
        category_orders={"risk_level": LEVEL_ORDER},
    )
    fig_donut.update_traces(
        textinfo="percent+label",
        hovertemplate="%{label}: %{value} risks (%{percent})<extra></extra>",
    )
    fig_donut.update_layout(margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

# ==============================================================================
# 10. CHARTS — ROW 2: Risk by Department & Top 10 Risks
# ==============================================================================
row2_left, row2_right = st.columns(2)

with row2_left:
    st.subheader("🏢 Risk by Department")
    dept_summary = (
        df.groupby(["department", "risk_level"]).size().reset_index(name="count")
    )
    fig_dept = px.bar(
        dept_summary, x="department", y="count", color="risk_level",
        color_discrete_map=COLOR_MAP, category_orders={"risk_level": LEVEL_ORDER},
        barmode="stack",
    )
    fig_dept.update_traces(
        hovertemplate="%{x}<br>%{fullData.name}: %{y} risks<extra></extra>"
    )
    fig_dept.update_layout(
        xaxis_title="", yaxis_title="Number of Risks", legend_title="Risk Level",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_dept, use_container_width=True)

with row2_right:
    st.subheader("🔝 Top 10 Risks by Score")
    top10 = df.sort_values("risk_score", ascending=False).drop_duplicates("risk_id").head(10)
    fig_top10 = px.bar(
        top10.sort_values("risk_score"),
        x="risk_score", y="risk_name", orientation="h",
        color="risk_level", color_discrete_map=COLOR_MAP,
        category_orders={"risk_level": LEVEL_ORDER},
        hover_data={"department": True, "owner": True, "status": True},
    )
    fig_top10.update_layout(
        xaxis_title="Risk Score", yaxis_title="", legend_title="Risk Level",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_top10, use_container_width=True)

# ==============================================================================
# 11. CHARTS — ROW 3: Heatmap & Monthly Risk Score Trend
# ==============================================================================
row3_left, row3_right = st.columns(2)

with row3_left:
    st.subheader("🌡️ Risk Heatmap: Impact vs. Probability")
    heat = df.groupby(["probability", "impact"]).size().reset_index(name="count")
    heat_pivot = heat.pivot(index="impact", columns="probability", values="count").fillna(0)
    heat_pivot = heat_pivot.reindex(index=[1, 2, 3, 4, 5], columns=[1, 2, 3, 4, 5], fill_value=0)
    fig_heat = px.imshow(
        heat_pivot,
        labels=dict(x="Probability", y="Impact", color="Risk Count"),
        color_continuous_scale=["#54A24B", "#F2B701", "#E45756"],
        text_auto=True, aspect="auto",
    )
    fig_heat.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)

with row3_right:
    st.subheader("📊 Monthly Risk Score Trend")
    monthly_score = df.groupby("month", as_index=False)["risk_score"].mean()
    fig_score_trend = go.Figure()
    fig_score_trend.add_trace(
        go.Scatter(
            x=monthly_score["month"], y=monthly_score["risk_score"],
            mode="lines+markers", line=dict(color="#E45756", width=3),
            fill="tozeroy", fillcolor="rgba(228,87,86,0.10)",
            hovertemplate="Month: %{x|%b %Y}<br>Avg Score: %{y:.1f}<extra></extra>",
        )
    )
    fig_score_trend.add_hline(y=7, line_dash="dot", line_color="#F2B701", annotation_text="Medium threshold")
    fig_score_trend.add_hline(y=15, line_dash="dot", line_color="#E45756", annotation_text="High threshold")
    fig_score_trend.update_layout(
        xaxis_title="", yaxis_title="Avg Risk Score (1-25)",
        margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
    )
    st.plotly_chart(fig_score_trend, use_container_width=True)

# ==============================================================================
# 12. CHART — Compliance Trend (full width)
# ==============================================================================
st.subheader("✅ Compliance Trend")
compliance_trend = df.groupby("month", as_index=False)["compliant"].mean()
compliance_trend["compliance_pct"] = compliance_trend["compliant"] * 100
fig_compliance = px.line(
    compliance_trend, x="month", y="compliance_pct", markers=True,
    color_discrete_sequence=["#4C78A8"],
)
fig_compliance.add_hline(y=90, line_dash="dot", line_color="#54A24B", annotation_text="Target: 90%")
fig_compliance.update_traces(
    hovertemplate="Month: %{x|%b %Y}<br>Compliance: %{y:.1f}%<extra></extra>"
)
fig_compliance.update_layout(
    xaxis_title="", yaxis_title="Compliance (%)", yaxis_range=[0, 100],
    margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified",
)
st.plotly_chart(fig_compliance, use_container_width=True)

st.markdown("---")

# ==============================================================================
# 13. RISK REGISTER TABLE
# ==============================================================================
st.subheader("📋 Risk Register")

register_cols = {
    "risk_id": "Risk ID",
    "risk_name": "Risk Name",
    "department": "Department",
    "owner": "Owner",
    "category": "Category",
    "risk_score": "Risk Score",
    "status": "Status",
    "mitigation_plan": "Mitigation Plan",
}
register_df = (
    df[list(register_cols.keys())]
    .rename(columns=register_cols)
    .sort_values("Risk Score", ascending=False)
    .reset_index(drop=True)
)

st.dataframe(
    register_df,
    use_container_width=True,
    height=380,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score", min_value=0, max_value=25, format="%d"
        ),
    },
)

# ------------------------------------------------------------------------------
# CSV download
# ------------------------------------------------------------------------------
csv_data = register_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Risk Register as CSV",
    data=csv_data,
    file_name="risk_register.csv",
    mime="text/csv",
)

st.caption(
    "Sample data is randomly generated for demonstration purposes. "
    "Replace `generate_risk_data()` with a real data source to connect "
    "this dashboard to your GRC / risk management system."
)