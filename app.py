import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_master_report():

    st.title("🧵 Stitching Project - Master Report Generator (Sample Data)")

    # --- 1. CREATE SAMPLE DATA ---
    st.subheader("Step 1: Sample Issue Records Created")

    data = {
        "Date Of Issue": pd.date_range(start="2024-01-01", periods=10, freq="15D"),
        "Names Of Style": ["Style A", "Style B", "Style C", "Style A", "Style B",
                           "Style C", "Style A", "Style B", "Style C", "Style A"],
        "Total issue": [500, 600, 450, 700, 800, 650, 400, 300, 550, 900],
        "Recevided": [480, 590, 430, 650, 790, 620, 380, 290, 530, 870],
        "Remanin": [20, 10, 20, 50, 10, 30, 20, 10, 20, 30],
        "Total Expenses": [25000, 30000, 23000, 35000, 38000, 31000, 20000, 15000, 27000, 45000],
        "Stiching Cost Accrued": [45, 50, 48, 47, 52, 49, 44, 40, 50, 55],
        "5 Thread Cost": [5, 6, 5, 5, 6, 5, 4, 4, 6, 7],
        "Total Cost": [50, 56, 53, 52, 58, 54, 48, 44, 56, 62],
        "Comparison Costing": [55, 60, 55, 56, 60, 56, 50, 48, 60, 65],
        "Difference From Comparison Costing": [-5, -4, -2, -4, -2, -2, -2, -4, -4, -3],
        "Outsider Cost": [12, 14, 13, 15, 16, 14, 11, 10, 14, 17],
        "Issue Chalan Number": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    }

    df = pd.DataFrame(data)
    st.dataframe(df)

    # --- 2. STYLE-WISE ANALYSIS ---
    st.subheader("Step 2: Style Profitability Analysis")

    style_analysis = df.groupby("Names Of Style").agg({
        "Total issue": "sum",
        "Recevided": "sum",
        "Total Expenses": "sum",
        "Stiching Cost Accrued": "mean",
        "Total Cost": "mean",
        "Comparison Costing": "mean",
        "Difference From Comparison Costing": "sum",
        "Outsider Cost": "mean"
    }).reset_index()

    style_analysis["Cost_Per_Piece"] = style_analysis["Total Expenses"] / style_analysis["Total issue"]
    style_analysis["Efficiency_Ratio"] = (
        style_analysis["Recevided"] / style_analysis["Total issue"] * 100
    )

    st.dataframe(style_analysis)

    # --- 3. MONTHLY TRENDS ---
    st.subheader("Step 3: Monthly Trends")

    df["Year_Month"] = df["Date Of Issue"].dt.to_period("M")
    monthly_trends = df.groupby("Year_Month").agg({
        "Total issue": "sum",
        "Recevided": "sum",
        "Total Expenses": "sum",
        "Difference From Comparison Costing": "sum"
    }).reset_index()

    st.dataframe(monthly_trends)

    # --- 4. SUMMARY BOX ---
    st.subheader("Step 4: Cost Summary")

    total_issues = df["Total issue"].sum()
    total_received = df["Recevided"].sum()
    total_expense = df["Total Expenses"].sum()
    total_profit = df["Difference From Comparison Costing"].sum()
    efficiency = (total_received / total_issues) * 100

    st.metric("Total Issues", total_issues)
    st.metric("Total Received", total_received)
    st.metric("Total Expenses", total_expense)
    st.metric("Overall Loss/Profit", total_profit)
    st.metric("Production Efficiency (%)", round(efficiency, 2))


st.set_page_config(layout="wide")
generate_master_report()
