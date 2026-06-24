import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
sales = pd.read_csv("retail_sales_cleaned.csv")

sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

# Date Range Filter
start_date = sales['OrderDate'].min()
end_date = sales['OrderDate'].max()

date_range = st.sidebar.date_input(
    "Date Range",
    value=[start_date, end_date]
)

# Region Filter
region = st.sidebar.multiselect(
    "Region",
    options=sales['Region'].unique(),
    default=sales['Region'].unique()
)

# Category Filter
category = st.sidebar.multiselect(
    "Category",
    options=sales['Category'].unique(),
    default=sales['Category'].unique()
)

# Segment Filter
segment = st.sidebar.multiselect(
    "Segment",
    options=sales['Segment'].unique(),
    default=sales['Segment'].unique()
)

# ----------------------------
# APPLY FILTERS
# ----------------------------
filtered = sales[
    (sales['Region'].isin(region)) &
    (sales['Category'].isin(category)) &
    (sales['Segment'].isin(segment))
]

if len(date_range) == 2:
    filtered = filtered[
        (filtered['OrderDate'] >= pd.to_datetime(date_range[0])) &
        (filtered['OrderDate'] <= pd.to_datetime(date_range[1]))
    ]

# ----------------------------
# KPI CARDS
# ----------------------------
revenue = filtered['Sales'].sum()
profit = filtered['Profit'].sum()
orders = filtered['OrderID'].nunique()
aov = revenue / orders if orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"${revenue:,.0f}")
col2.metric("Profit", f"${profit:,.0f}")
col3.metric("AOV", f"${aov:,.2f}")
col4.metric("Orders", f"{orders:,}")

# ----------------------------
# CHARTS IN 2 x 2 LAYOUT
# ----------------------------

colA, colB = st.columns(2)

with colA:
    monthly_sales = filtered.groupby(
        filtered['OrderDate'].dt.to_period('M')
    )['Sales'].sum().reset_index()

    monthly_sales['OrderDate'] = monthly_sales['OrderDate'].astype(str)

    fig1 = px.line(
        monthly_sales,
        x='OrderDate',
        y='Sales',
        title='Monthly Sales Trend'
    )

    st.plotly_chart(fig1, use_container_width=True)

with colB:
    category_sales = (
        filtered.groupby('Category')['Sales']
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_sales,
        x='Category',
        y='Sales',
        title='Sales by Category'
    )

    st.plotly_chart(fig2, use_container_width=True)

colC, colD = st.columns(2)

with colC:
    top_customers = (
        filtered.groupby('CustomerName')['Sales']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top_customers,
        x='CustomerName',
        y='Sales',
        title='Top 10 Customers'
    )

    st.plotly_chart(fig3, use_container_width=True)

with colD:
    region_sales = (
        filtered.groupby('Region')['Sales']
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        title='Region Comparison'
    )

    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.subheader("Filtered Data Table")

st.dataframe(filtered, use_container_width=True)