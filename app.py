import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Logistics Business Dashboard",
    layout="wide",
    page_icon="📦"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
    <style>
        .main {background-color: #0E1117;}
        .block-container {padding-top: 1rem;}
        h1, h2, h3 {color: #00BFFF;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Train.csv")
    return df

df = load_data()

# Rename for easier use
df["OnTime"] = df["Reached.on.Time_Y.N"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filter Options")

shipment_mode = st.sidebar.multiselect(
    "Select Shipment Mode",
    options=df["Mode_of_Shipment"].unique(),
    default=df["Mode_of_Shipment"].unique()
)

warehouse = st.sidebar.multiselect(
    "Select Warehouse",
    options=df["Warehouse_block"].unique(),
    default=df["Warehouse_block"].unique()
)

product_importance = st.sidebar.multiselect(
    "Select Product Importance",
    options=df["Product_importance"].unique(),
    default=df["Product_importance"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Apply Filters
filtered_df = df[
    (df["Mode_of_Shipment"].isin(shipment_mode)) &
    (df["Warehouse_block"].isin(warehouse)) &
    (df["Product_importance"].isin(product_importance)) &
    (df["Gender"].isin(gender))
]

# -----------------------------
# Title
# -----------------------------
st.title("📦 Logistics Performance Business Dashboard")
st.markdown("Business KPI Monitoring & Operational Insights")

# -----------------------------
# KPI Calculations
# -----------------------------
total_orders = len(filtered_df)
on_time_rate = (filtered_df["OnTime"].sum() / total_orders) * 100
late_rate = 100 - on_time_rate
avg_discount_late = filtered_df[filtered_df["OnTime"] == 0]["Discount_offered"].mean()
avg_calls_late = filtered_df[filtered_df["OnTime"] == 0]["Customer_care_calls"].mean()

high_value = filtered_df[filtered_df["Cost_of_the_Product"] > filtered_df["Cost_of_the_Product"].median()]
high_value_late_rate = (1 - high_value["OnTime"].mean()) * 100

# -----------------------------
# KPI Section
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📦 Total Orders", f"{total_orders:,}")
col2.metric("✅ On-Time Delivery %", f"{on_time_rate:.2f}%")
col3.metric("❌ Late Delivery %", f"{late_rate:.2f}%")
col4.metric("📞 Avg Calls (Late)", f"{avg_calls_late:.2f}")
col5.metric("💎 High Value Late %", f"{high_value_late_rate:.2f}%")

st.markdown("---")

# -----------------------------
# Main Visualization Section (3 Rows Layout)
# -----------------------------

st.markdown("## 📊 Business Visual Insights")

# =========================
# ROW 1 (3 Charts)
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    fig1 = px.histogram(
        filtered_df,
        x="Mode_of_Shipment",
        color="OnTime",
        barmode="group",
        title="Shipment Mode vs Delivery",
        color_discrete_sequence=["#FF4B4B", "#00C49F"]
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    warehouse_perf = filtered_df.groupby("Warehouse_block")["OnTime"].mean().reset_index()
    fig2 = px.bar(
        warehouse_perf,
        x="Warehouse_block",
        y="OnTime",
        title="Warehouse Performance",
        color="OnTime",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.box(
        filtered_df,
        x="OnTime",
        y="Discount_offered",
        color="OnTime",
        title="Discount vs Delivery",
        color_discrete_sequence=["#FF4B4B", "#00C49F"]
    )
    st.plotly_chart(fig3, use_container_width=True)


# =========================
# ROW 2 (2 Charts)
# =========================
col4, col5 = st.columns(2)

with col4:
    fig4 = px.scatter(
        filtered_df,
        x="Customer_care_calls",
        y="Discount_offered",
        color="OnTime",
        size="Cost_of_the_Product",
        title="Calls vs Discount (Bubble Size = Cost)",
        color_discrete_sequence=["#FF4B4B", "#00C49F"]
    )
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    fig5 = px.imshow(
        filtered_df.select_dtypes(include=np.number).corr(),
        text_auto=True,
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig5, use_container_width=True)

# =========================
# ROW 3 (1 Full Width Chart)
# =========================
st.markdown("### Product Importance Distribution")

fig6 = px.pie(
    filtered_df,
    names="Product_importance",
    title="Product Importance Breakdown"
)
st.plotly_chart(fig6, use_container_width=True)

##########

st.markdown("### 📊 Insights")
st.write("""
- Shipment mode significantly influences delivery time.
- Higher customer calls strongly correlate with late deliveries.
- High discounts often associate with delayed shipments.
- Warehouse performance varies across blocks.
""")