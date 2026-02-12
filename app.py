import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def generate_master_report():
    """
    Generate Master Report from Stitching Cost Data
    Analyzes: Style Profitability, Worker Performance, Cost Dynamics
    """
    
    print("=" * 70)
    print("STITCHING PROJECT - MASTER REPORT GENERATOR")
    print("=" * 70)
    
    # --- 1. LOAD ISSUE RECORDS (Main Costing Data) ---
    print("\n[Step 1] Loading Issue Records from issue_records_2025.csv...")
    try:
        df_issues = pd.read_csv('issue_records_2025.csv')
        
        # Clean column names
        df_issues.columns = df_issues.columns.str.strip()
        
        print(f"✓ Loaded {len(df_issues)} issue records")
        print(f"✓ Columns: {list(df_issues.columns)}")
        
    except Exception as e:
        print(f"✗ Error loading issue records: {e}")
        return
    
    # --- 2. DATA CLEANING & TRANSFORMATION ---
    print("\n[Step 2] Cleaning and transforming data...")
    
    # Convert numeric columns
    numeric_cols = ['Total issue', 'Recevided', 'Remanin', 'Total Expenses', 
                   'Stiching Cost Accrued', '5 Thread Cost', 'Total Cost', 
                   'Comparison Costing', 'Difference From Comparison Costing']
    
    for col in numeric_cols:
        if col in df_issues.columns:
            df_issues[col] = pd.to_numeric(df_issues[col], errors='coerce')
    
    # Convert date
    if 'Date Of Issue' in df_issues.columns:
        df_issues['Date Of Issue'] = pd.to_datetime(df_issues['Date Of Issue'], 
                                                     format='%d/%m/%Y', errors='coerce')
    
    # Remove rows with #N/A or missing critical data
    df_issues = df_issues[df_issues['Names Of Style'].notna()]
    df_issues = df_issues[df_issues['Total issue'] > 0]
    
    print(f"✓ Valid records after cleaning: {len(df_issues)}")
    
    # --- 3. STYLE-WISE ANALYSIS ---
    print("\n[Step 3] Analyzing Style Profitability...")
    
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
    
    # Calculate additional metrics
    style_analysis['Profit_Loss'] = style_analysis['Difference From Comparison Costing']
    style_analysis['Cost_Per_Piece'] = style_analysis['Total Expenses'] / style_analysis['Total issue']
    style_analysis['Software_Rate'] = style_analysis['Comparison Costing']
    style_analysis['Actual_Cost_Per_Piece'] = style_analysis['Total Cost']
    style_analysis['Efficiency_Ratio'] = (style_analysis['Recevided'] / 
                                          style_analysis['Total issue'] * 100).round(2)
    
    # Identify top performers and problem areas
    top_profitable = style_analysis.nlargest(10, 'Profit_Loss')
    top_losses = style_analysis.nsmallest(10, 'Profit_Loss')
    
    # Save style analysis
    style_analysis_output = style_analysis[[
        'Names Of Style', 'Total issue', 'Recevided', 'Efficiency_Ratio',
        'Cost_Per_Piece', 'Software_Rate', 'Actual_Cost_Per_Piece', 
        'Profit_Loss', 'Outsider Cost'
    ]].sort_values('Profit_Loss', ascending=False)
    
    style_analysis_output.to_csv('style_analysis_report.csv', index=False)
    print(f"✓ Style analysis saved: style_analysis_report.csv")
    print(f"\n📊 TOP 5 PROFITABLE STYLES:")
    print(top_profitable[['Names Of Style', 'Profit_Loss']].to_string())
    print(f"\n⚠️  TOP 5 LOSS-MAKING STYLES:")
    print(top_losses[['Names Of Style', 'Profit_Loss']].to_string())
    
    # --- 4. DATE-WISE TREND ANALYSIS ---
    print("\n[Step 4] Analyzing Monthly Trends...")
    
    df_issues['Year_Month'] = df_issues['Date Of Issue'].dt.to_period('M')
    
    monthly_trends = df_issues.groupby('Year_Month').agg({
        'Total issue': 'sum',
        'Recevided': 'sum',
        'Total Expenses': 'sum',
        'Difference From Comparison Costing': 'sum',
        'Total Cost': 'mean'
    }).reset_index()
    
    monthly_trends.columns = ['Month', 'Total_Issued', 'Total_Received', 
                             'Total_Expenses', 'Total_Profit_Loss', 'Avg_Cost_Per_Piece']
    
    monthly_trends.to_csv('monthly_trends_report.csv', index=False)
    print(f"✓ Monthly trends saved: monthly_trends_report.csv")
    
    # --- 5. COST DYNAMICS ANALYSIS ---
    print("\n[Step 5] Analyzing Cost Dynamics...")
    
    cost_summary = {
        'Total_Issues': df_issues['Total issue'].sum(),
        'Total_Received': df_issues['Recevided'].sum(),
        'Remaining': df_issues['Remanin'].sum(),
        'Overall_Efficiency_%': (df_issues['Recevided'].sum() / 
                                df_issues['Total issue'].sum() * 100),
        'Total_Expenses': df_issues['Total Expenses'].sum(),
        'Avg_Stitching_Cost': df_issues['Stiching Cost Accrued'].mean(),
        'Avg_Thread_Cost': df_issues['5 Thread Cost'].mean(),
        'Avg_Total_Cost_Per_Pc': df_issues['Total Cost'].mean(),
        'Avg_Software_Rate': df_issues['Comparison Costing'].mean(),
        'Overall_Profit_Loss': df_issues['Difference From Comparison Costing'].sum(),
        'Outsider_Avg_Cost': df_issues['Outsider Cost'].mean()
    }
    
    cost_df = pd.DataFrame([cost_summary])
    cost_df.to_csv('cost_dynamics_summary.csv', index=False)
    
    print(f"\n💰 COST DYNAMICS SUMMARY:")
    for key, value in cost_summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value:,}")
    
    # --- 6. ISSUE CHALAN TRACKING ---
    print("\n[Step 6] Processing Issue Chalan Records...")
    
    chalan_data = df_issues[['Date Of Issue', 'Issue Chalan Number', 'Names Of Style', 
                            'Total issue', 'Recevided', 'Remanin', 'Total Expenses',
                            'Stiching Cost Accrued', '5 Thread Cost', 'Total Cost',
                            'Comparison Costing', 'Difference From Comparison Costing']].copy()
    
    chalan_data = chalan_data.sort_values('Date Of Issue', ascending=False)
    chalan_data.to_csv('issue_chalan_tracking.csv', index=False)
    print(f"✓ Chalan tracking saved: issue_chalan_tracking.csv")
    
    # --- 7. GENERATE FINAL MASTER REPORT ---
    print("\n[Step 7] Generating Master Resolution Report...")
    
    master_report = {
        'Report_Generated': pd.Timestamp.now(),
        'Total_Records': len(df_issues),
        'Date_Range': f"{df_issues['Date Of Issue'].min().date()} to {df_issues['Date Of Issue'].max().date()}",
        'Unique_Styles': df_issues['Names Of Style'].nunique(),
        'Overall_Profit_Loss': df_issues['Difference From Comparison Costing'].sum(),
        'Cost_Variance_Percentage': (
            (df_issues['Total Cost'].sum() - df_issues['Comparison Costing'].sum()) / 
            df_issues['Comparison Costing'].sum() * 100 if df_issues['Comparison Costing'].sum() > 0 else 0
        ),
        'Production_Efficiency': (df_issues['Recevided'].sum() / df_issues['Total issue'].sum() * 100)
    }
    
    master_df = pd.DataFrame([master_report])
    master_df.to_csv('Master_Resolution_Report.csv', index=False)
    
    print(f"\n✓ Master Resolution Report created!")
    print(f"\n📋 MASTER REPORT SUMMARY:")
    for key, value in master_report.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    
    # --- 8. GENERATE VISUALIZATIONS ---
    print("\n[Step 8] Generating Visualizations...")
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        sns.set_style("whitegrid")
        
        # Plot 1: Top Profitable vs Loss-Making Styles
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        top_profit = style_analysis_output.head(10)
        top_loss = style_analysis_output.tail(10)
        
        axes[0].barh(top_profit['Names Of Style'], top_profit['Profit_Loss'], color='green', alpha=0.7)
        axes[0].set_xlabel('Profit/Loss Amount')
        axes[0].set_title('Top 10 Most Profitable Styles')
        axes[0].axvline(x=0, color='red', linestyle='--', linewidth=0.8)
        
        axes[1].barh(top_loss['Names Of Style'], top_loss['Profit_Loss'], color='red', alpha=0.7)
        axes[1].set_xlabel('Profit/Loss Amount')
        axes[1].set_title('Top 10 Loss-Making Styles')
        axes[1].axvline(x=0, color='red', linestyle='--', linewidth=0.8)
        
        plt.tight_layout()
        plt.savefig('style_profitability_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved: style_profitability_analysis.png")
        
        # Plot 2: Monthly Trends
        fig, ax = plt.subplots(figsize=(14, 6))
        ax2 = ax.twinx()
        
        ax.plot(monthly_trends['Month'].astype(str), monthly_trends['Total_Issued'], 
               marker='o', color='blue', label='Total Issued', linewidth=2)
        ax2.plot(monthly_trends['Month'].astype(str), monthly_trends['Total_Profit_Loss'], 
                marker='s', color='green', label='Profit/Loss', linewidth=2)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Quantity', color='blue')
        ax2.set_ylabel('Profit/Loss', color='green')
        ax.set_title('Monthly Production & Profitability Trends')
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('monthly_trends_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved: monthly_trends_analysis.png")
        
        plt.close('all')
        
    except ImportError:
        print("⚠️  Matplotlib not installed. Skipping visualizations.")
    
    # --- 9. FINAL SUMMARY ---
    print("\n" + "=" * 70)
    print("REPORT GENERATION COMPLETE!")
    print("=" * 70)
    print("\n📁 Generated Files:")
    print("  1. style_analysis_report.csv - Style-wise profitability analysis")
    print("  2. monthly_trends_report.csv - Monthly production trends")
    print("  3. cost_dynamics_summary.csv - Overall cost summary")
    print("  4. issue_chalan_tracking.csv - Detailed chalan records")
    print("  5. Master_Resolution_Report.csv - Executive summary")
    print("  6. style_profitability_analysis.png - Visualization")
    print("  7. monthly_trends_analysis.png - Trend visualization")
    print("=" * 70)

if __name__ == "__main__":
    generate_master_report()
