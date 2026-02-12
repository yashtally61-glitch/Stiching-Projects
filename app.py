import pandas as pd

# -----------------------------
# 1. Load all Excel files
# -----------------------------
rate_sheet = pd.read_excel('/mnt/data/Rate Sheet.xlsx')
style_sheet = pd.read_excel('/mnt/data/Karihgar Style.xlsx')
daily_report = pd.read_excel('/mnt/data/Daily SKU wise Report.xlsx')
costing_working = pd.read_excel('/mnt/data/Costing Working.xlsx')
cost_file = pd.read_excel('/mnt/data/Cost.xlsx')

# -----------------------------
# 2. Clean column names (Optional)
# -----------------------------
rate_sheet.columns = rate_sheet.columns.str.strip().str.lower()
style_sheet.columns = style_sheet.columns.str.strip().str.lower()
daily_report.columns = daily_report.columns.str.strip().str.lower()

# -----------------------------
# 3. Merge Style Sheet with Rate Sheet
# -----------------------------
merged_style = pd.merge(
    style_sheet, 
    rate_sheet, 
    on='operation',        # ex: Stitch, Overlock etc.
    how='left'
)

# Operation Cost = Rate * Qty
merged_style['operation_cost'] = merged_style['rate'] * merged_style['qty']

# -----------------------------
# 4. Calculate Total Operation Cost per Style
# -----------------------------
style_cost = merged_style.groupby('style')['operation_cost'].sum().reset_index()
style_cost = style_cost.rename(columns={'operation_cost': 'total_stitching_cost'})

# -----------------------------
# 5. Merge with Daily Production Report
# -----------------------------
production = daily_report.groupby(['style'])['output qty'].sum().reset_index()

final_cost = pd.merge(style_cost, production, on='style', how='left')

# -----------------------------
# 6. Final Costing Formula
# -----------------------------
# Assuming: costing_working contains trims, fabric, packing etc.

final = pd.merge(final_cost, costing_working, on='style', how='left')

final['final_cost_per_piece'] = (
    final['total_stitching_cost'] 
    + final['fabric_cost']
    + final['trims_cost']
    + final['packing_cost']
    + final['overhead_cost']
) / final['output qty']

# -----------------------------
# 7. Save Final Output
# -----------------------------
final.to_excel('/mnt/data/Final_Costing_Output.xlsx', index=False)

print("Costing completed. File saved as Final_Costing_Output.xlsx")
