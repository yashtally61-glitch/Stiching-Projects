import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_master_report():
    """
    Generate Master Report using SAMPLE DATA (No CSV Required)
    """
    
    print("=" * 70)
    print("STITCHING PROJECT - MASTER REPORT GENERATOR (SAMPLE DATA)")
    print("=" * 70)
    
    # --- 1. CREATE SAMPLE DATA ---
    print("\n[Step 1] Creating sample issue records...")
    
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
    
    df_issues = pd.DataFrame(data)
    
    print(f"✓ Sample data created ({len(df_issues)} records)")
    
    # --- 2. STYLE-WISE ANALYSIS ---
    print("\n[Step 2] Analyzing Style Profitability...")
    
    style_analysis = df_issues.groupby('Names Of Style').agg({
        'Total issue': 'sum',
        'Recevided': 'sum',
        'Total Expenses': 'sum',
        'Stiching Cost Accrued': 'mean',
        'Total Cost': 'mean',
        'Comparison Costing': 'mean',
        'Difference From Comparison Costing': 'sum',
        'Outsider Cost': 'mean'
    }).reset_index()
    
    style_analysis['Profit_Loss'] = style_analysis['Difference From Comparison Costing']
    style_analysis['Cost_Per_Piece'] = style_analysis['Total Expenses'] / style_analysis['Total issue']
    style_analysis['Efficiency_Ratio'] = (
        style_analysis['Recevided'] / style_analysis['Total issue'] * 100
    ).round(2)
    
    print("✓ Style analysis completed")
    print(style_analysis)
    
    # --- 3. MONTHLY TRENDS ---
    print("\n[Step 3] Monthly Trend Analysis...")
    
    df_issues['Year_Month'] = df_issues['Date Of Issue'].dt.to_period('M')
    
    monthly_trends = df_issues.groupby('Year_Month').agg({
        'Total issue': 'sum',
        'Recevided': 'sum',
        'Total Expenses': 'sum',
        'Difference From Comparison Costing': 'sum'
    }).reset_index()
    
    print("✓ Monthly trends completed")
    print(monthly_trends)
    
    # --- 4. COST SUMMARY ---
    print("\n[Step 4] Cost Dynamics Summary...")
    
    summary = {
        "Total Issues": df_issues["Total issue"].sum(),
        "Total Received": df_issues["Recevided"].sum(),
        "Total Expenses": df_issues["Total Expenses"].sum(),
        "Overall Profit/Loss": df_issues["Difference From Comparison Costing"].sum(),
        "Overall Efficiency %": (df_issues["Recevided"].sum() / df_issues["Total issue"].sum()) * 100
    }
    
    print(summary)
    
    # --- 5. FINISH ---
    print("\n" + "=" * 70)
    print("REPORT GENERATED SUCCESSFULLY! 🎉 (Sample Data)")
    print("=" * 70)

if __name__ == "__main__":
    generate_master_report()
