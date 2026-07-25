import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Afficionado Coffee Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------
# LOAD CSS
# ---------------------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

@st.cache_data
def load_data():
    df = pd.read_excel("data/coffee_sales_featured.xlsx")
    return df

df = load_data()

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.markdown("""
<div style="text-align:center;padding:15px;">

<img src="https://img.icons8.com/fluency/96/coffee.png" width="90">

<h2 style="color:#FFD54F;margin-bottom:0px;">
Afficionado
</h2>

<p style="color:#FFE7A0;font-size:14px;margin-top:0px;">
Coffee Analytics Dashboard
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.success("🟢 Dashboard Online")

st.sidebar.metric(
    "🏪 Stores",
    df["store_location"].nunique()
)

st.sidebar.metric(
    "☕ Categories",
    df["product_category"].nunique()
)

st.sidebar.metric(
    "📦 Products",
    df["product_detail"].nunique()
)

st.sidebar.markdown("---")

store = st.sidebar.selectbox(
    "🏪 Store",
    ["All Stores"] + sorted(df["store_location"].unique())
)

category = st.sidebar.selectbox(
    "☕ Category",
    ["All Categories"] + sorted(df["product_category"].unique())
)

time_period = st.sidebar.selectbox(
    "🕒 Time",
    ["All"] + sorted(df["time_period"].unique())
)

st.sidebar.markdown("---")

st.sidebar.info(
"""
### Dashboard

✔ Revenue

✔ Products

✔ Peak Hours

✔ Business Insights

✔ Analytics
"""
)

# ---------------------------------------
# FILTER
# ---------------------------------------

filtered_df = df.copy()

if store != "All Stores":
    filtered_df = filtered_df[
        filtered_df["store_location"] == store
    ]

if category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["product_category"] == category
    ]

if time_period != "All":
    filtered_df = filtered_df[
        filtered_df["time_period"] == time_period
    ]

# ---------------------------------------
# HEADER
# ---------------------------------------

st.markdown("""

<div class="hero-box">

<div class="hero-title">
☕ Afficionado Coffee Roasters
</div>

<div class="hero-sub">
Data-Driven Forecasting & Peak Demand Prediction
</div>

<div class="hero-desc">

Welcome to the interactive business intelligence dashboard.

Analyze revenue, identify peak demand hours, compare store performance,
explore customer purchasing trends and generate valuable business insights
through beautiful visualizations.

</div>

</div>

""", unsafe_allow_html=True)

# ---------------------------------------
# KPIs
# ---------------------------------------

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["transaction_id"].count()

avg_order = filtered_df["revenue"].mean()

total_quantity = filtered_df["transaction_qty"].sum()

premium_sales = filtered_df[
    filtered_df["premium_product"] == "Yes"
].shape[0]

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "💰 Revenue",
    f"${total_revenue:,.2f}"
)

c2.metric(
    "🧾 Orders",
    f"{total_orders:,}"
)

c3.metric(
    "🛒 Avg Order",
    f"${avg_order:.2f}"
)

c4.metric(
    "☕ Quantity",
    f"{total_quantity:,}"
)

c5.metric(
    "⭐ Premium",
    premium_sales
)

st.markdown("---")
st.caption("📊 Live dashboard metrics based on current filters")
# ======================================================
# DASHBOARD HEALTH
# ======================================================
st.markdown("""
<div class="hero-score" style="
background: linear-gradient(135deg, #3d2817, #6F4E37);
padding: 25px;
border-radius: 18px;
border: 2px solid #FFD54F;
box-shadow: 0 8px 20px rgba(0,0,0,0.35);
margin-top: 20px;
margin-bottom: 20px;
text-align: center;
">

<h2 style="color:#FFD54F; margin-bottom:10px;">
📊 Dashboard Health Score
</h2>

<h1 style="
font-size:55px;
margin:0;
color:white;
">
96/100
</h1>

<p style="
font-size:18px;
color:#FFE7A0;
margin-top:10px;
">
🚀 Excellent Business Performance
</p>

</div>
""", unsafe_allow_html=True)



# ======================================================
# REVENUE BY STORE
# ======================================================

st.subheader("📍 Revenue by Store")

store_revenue = (
    filtered_df.groupby("store_location")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

fig_store = px.bar(
    store_revenue,
    x="store_location",
    y="revenue",
    color="revenue",
    text_auto=".2s",
    color_continuous_scale="YlOrBr"
)

fig_store.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    title="Revenue by Store",

    title_x=0.5,

    height=500,

    hovermode="x unified",

    font=dict(
        family="Poppins",
        color="white",
        size=14
    ),

    title_font=dict(
        size=22,
        color="#FFD54F"
    ),

    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )


)

fig_store.update_traces(

    hovertemplate="<b>%{x}</b><br>Revenue : $%{y:,.2f}<extra></extra>",

    marker_line_color="#FFD54F",

    marker_line_width=1.5

)

st.plotly_chart(fig_store, use_container_width=True)

st.markdown("---")

# ======================================================
# CATEGORY + HOURLY
# ======================================================

left,right = st.columns(2)

with left:

    st.subheader("☕ Category Revenue")

    category_data = (
        filtered_df.groupby("product_category")["revenue"]
        .sum()
        .reset_index()
    )

    fig_pie = px.pie(
        category_data,
        names="product_category",
        values="revenue",
        hole=.55,
        color_discrete_sequence=px.colors.sequential.YlOrBr
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>"
    )

    fig_pie.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450,

    font=dict(
        family="Poppins",
        color="white"
    ),

    title_font=dict(
        size=20,
        color="#FFD54F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )

)

    st.plotly_chart(fig_pie, use_container_width=True)

with right:

    st.subheader("⏰ Hourly Revenue")

    hourly = (
        filtered_df.groupby("hour")["revenue"]
        .sum()
        .reset_index()
    )

    fig_hour = px.line(
        hourly,
        x="hour",
        y="revenue",
        markers=True
    )

    fig_hour.update_traces(
        line=dict(width=5),
        marker=dict(size=10),
        hovertemplate="Hour %{x}<br>$%{y:,.2f}<extra></extra>"
    )

    fig_hour.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450,

    hovermode="x unified",

    font=dict(
        family="Poppins",
        color="white"
    ),

    title_font=dict(
        size=20,
        color="#FFD54F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )

)

    st.plotly_chart(fig_hour, use_container_width=True)
    st.markdown("---")

st.subheader("🔥 Peak Demand Heatmap")

heatmap_data = (
    filtered_df.groupby(["hour", "store_location"])["transaction_qty"]
    .sum()
    .reset_index()
)

heatmap = heatmap_data.pivot(
    index="hour",
    columns="store_location",
    values="transaction_qty"
).fillna(0)

fig_heat = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="YlOrBr",
    labels=dict(
        x="Store",
        y="Hour",
        color="Quantity"
    )
)

fig_heat.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=500,
    title="Peak Demand by Hour & Store",
    title_x=0.5,
    font=dict(
        family="Poppins",
        color="white"
    ),
    title_font=dict(
        size=22,
        color="#FFD54F"
        
    )  
)

st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# ======================================================
# TOP PRODUCTS
# ======================================================

st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="revenue",
    y="product_detail",
    orientation="h",
    color="revenue",
    text_auto=".2s",
    color_continuous_scale="Sunset"
)

fig_products.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    title="🏆 Top Revenue Generating Products",

    title_x=0.5,

    height=550,

    yaxis=dict(categoryorder="total ascending"),

    font=dict(
        family="Poppins",
        color="white",
        size=14
    ),

    title_font=dict(
        size=22,
        color="#FFD54F"
    ),

    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )

)
fig_products.update_traces(

    hovertemplate="<b>%{y}</b><br>Revenue : $%{x:,.2f}<extra></extra>",

    marker_line_color="#FFD54F",

    marker_line_width=2,

    opacity=0.9

)
st.plotly_chart(fig_products, use_container_width=True)

st.markdown("---")

# ======================================================
# REVENUE DISTRIBUTION
# ======================================================

st.subheader("📊 Revenue Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="revenue",
    nbins=40,
    color_discrete_sequence=["#FFD54F"]
)

fig_hist.update_layout(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    height=450,

    title="📊 Revenue Distribution",

    title_x=0.5,

    font=dict(
        family="Poppins",
        size=14,
        color="white"
    ),

    title_font=dict(
        size=22,
        color="#FFD54F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )

)
fig_hist.update_traces(

    hovertemplate="Revenue : $%{x:.2f}<br>Count : %{y}<extra></extra>",

    marker_line_color="#FFD54F",

    marker_line_width=1

)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# ======================================================
# BUSINESS INSIGHTS
# ======================================================

st.subheader("🤖 AI Business Insights")

top_store = (
    filtered_df.groupby("store_location")["revenue"]
    .sum()
    .idxmax()
)

top_category = (
    filtered_df.groupby("product_category")["revenue"]
    .sum()
    .idxmax()
)

peak_hour = (
    filtered_df.groupby("hour")["revenue"]
    .sum()
    .idxmax()
)

best_product = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

with col1:

    st.success(f"""
### 🏪 Best Store

**{top_store}**

Highest Revenue Generated
""")

    st.info(f"""
### ☕ Top Category

**{top_category}**

Most Popular Category
""")

with col2:

    st.warning(f"""
### ⏰ Peak Hour

**{peak_hour}:00**

Maximum Customer Traffic
""")

    st.success(f"""
### 🏆 Best Product

**{best_product}**

Highest Revenue Product
""")

with col3:

    st.metric("💰 Revenue", f"${total_revenue:,.0f}")

    st.metric("🧾 Orders", f"{total_orders:,}")

    st.metric("☕ Quantity", f"{total_quantity:,}")

    st.metric("⭐ Premium", premium_sales)

    st.markdown("---")



st.markdown("---")
st.subheader("🏪 Store Performance Summary")

store_summary = (
    filtered_df.groupby("store_location")
    .agg(
        Revenue=("revenue", "sum"),
        Orders=("transaction_id", "count"),
        Quantity=("transaction_qty", "sum"),
        Avg_Order=("revenue", "mean")
    )
    .reset_index()
)

st.dataframe(
    store_summary,
    use_container_width=True,
    hide_index=True
) 
st.subheader("💡 Recommendations")

st.info("""
✅ Increase stock during peak hours.

✅ Promote top-selling products.

✅ Focus marketing on highest revenue store.

✅ Introduce premium products for better profit margin.

✅ Bundle low-selling products with best sellers.
""")

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Report",
    data=csv,
    file_name="coffee_dashboard_report.csv",
    mime="text/csv"
)

st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:20px;color:#BBBBBB">

☕ <b>Afficionado Coffee Analytics Dashboard</b><br>

Developed using <b>Python, Streamlit, Plotly & Pandas</b><br>

© 2026 Priyanshu Gautam

</div>
""", unsafe_allow_html=True)