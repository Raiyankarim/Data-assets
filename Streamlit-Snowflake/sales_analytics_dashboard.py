import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, sum as _sum, count_distinct, avg
from snowflake.snowpark.functions import when

# Get Snowpark session
session = get_active_session()

# App configuration
st.set_page_config(layout="wide")
st.title("Sales Analytics Dashboard")

# Load filter values
date_df = session.table("RAW_DATA.Date").select("YearMonth").distinct().sort("YearMonth").to_pandas()
category_df = session.table("RAW_DATA.Product").select("CategoryName").distinct().to_pandas()
country_df = session.table("RAW_DATA.Store").select("CountryName").distinct().to_pandas()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_months = st.multiselect("Select Month(s)", date_df["YEARMONTH"], default=date_df["YEARMONTH"].tolist()[-6:])
    selected_categories = st.multiselect("Product Categories", category_df["CATEGORYNAME"], default=category_df["CATEGORYNAME"].tolist())
    selected_countries = st.multiselect("Countries", country_df["COUNTRYNAME"], default=country_df["COUNTRYNAME"].tolist())

# Load tables
sales = session.table("RAW_DATA.Sales")
product = session.table("RAW_DATA.Product")
store = session.table("RAW_DATA.Store")
date = session.table("RAW_DATA.Date")
customer = session.table("RAW_DATA.Customer")

# Join and filter sales data
filtered_sales = (
    sales.join(product, sales["ProductKey"] == product["ProductKey"])
         .join(store, sales["StoreKey"] == store["StoreKey"])
         .join(date, sales["OrderDate"] == date["Date"])
         .filter(col("YearMonth").isin(selected_months))
         .filter(col("CategoryName").isin(selected_categories))
         .filter(col("CountryName").isin(selected_countries))
)



# KPIs
total_sales = filtered_sales.agg(_sum("NetPrice").alias("TotalSales")).collect()[0]["TOTALSALES"]
total_orders = filtered_sales.select("OrderKey").distinct().count()
total_units = filtered_sales.agg(_sum("Quantity").alias("TotalUnits")).collect()[0]["TOTALUNITS"]
avg_order_value = total_sales / total_orders if total_orders else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric(" Total Sales", f"${total_sales:,.2f}")
col2.metric(" Total Orders", total_orders)
col3.metric(" Units Sold", total_units)
col4.metric(" Avg Order Value", f"${avg_order_value:,.2f}")
# Sales Trend
sales_trend_df = (
    filtered_sales.group_by("YearMonth")
                  .agg(_sum("NetPrice").alias("Sales"))
                  .sort("YearMonth")
                  .to_pandas()
)

st.subheader(" Sales Trend")
st.line_chart(sales_trend_df.set_index("YEARMONTH"))

# Top Products
top_products_df = (
    filtered_sales.group_by("ProductName")
                  .agg(_sum("NetPrice").alias("Revenue"))
                  .sort(col("Revenue").desc())
                  .limit(10)
                  .to_pandas()
)

st.subheader(" Top 10 Products")
st.bar_chart(top_products_df.set_index("PRODUCTNAME"))

# Sales by Country
country_sales_df = (
    filtered_sales.group_by("CountryName")
                  .agg(_sum("NetPrice").alias("Revenue"))
                  .sort(col("Revenue").desc())
                  .to_pandas()
)

st.subheader(" Sales by Country")
st.bar_chart(country_sales_df.set_index("COUNTRYNAME"))

# Sales by Age Group
# Define age group logic using Snowpark case()
age_group_case = (
    when(col("Age") < 25, "Under 25")
    .when((col("Age") >= 25) & (col("Age") < 35), "25-34")
    .when((col("Age") >= 35) & (col("Age") < 50), "35-49")
    .when(col("Age") >= 50, "50+")
    .otherwise("Unknown")
)

age_sales_df = (
    filtered_sales.join(customer, filtered_sales["CustomerKey"] == customer["CustomerKey"])
                  .with_column("AgeGroup", age_group_case)
                  .group_by("AgeGroup")
                  .agg(_sum("NetPrice").alias("Revenue"))
                  .to_pandas()
)
st.subheader(" Sales by Age Group")
st.bar_chart(age_sales_df.set_index("AGEGROUP"))

