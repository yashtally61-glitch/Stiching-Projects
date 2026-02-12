import pandas as pd
import numpy as np

def generate_master_report():
    # --- 1. LOAD & PARSE COST.XLSX (The "Block" Format) ---
    print("Parsing Cost.xlsx...")
    try:
        df_raw = pd.read_csv('Cost.xlsx - Sheet1.csv', header=None)
        records = []
        current_sku = None
        block_data = {}

        for i in range(len(df_raw)):
            row = df_raw.iloc[i]
            # Detect Start of a Cost Block (SKU Name in Column 1)
            if pd.notna(row[0]) and isinstance(row[1], str) and len(row[1]) > 3:
                # Save previous block
                if current_sku and block_data:
                    records.append(block_data)
                
                current_sku = str(row[1]).strip()
                block_data = {'SKU': current_sku}
                
                # Look ahead 15 rows for key metrics
                for offset in range(1, 15):
                    if i + offset >= len(df_raw): break
                    sub_row = df_raw.iloc[i + offset]
                    
                    # Extract expenses
                    key = str(sub_row[1]).strip()
                    if key in ['Total Expenses', 'Refreshment', 'Line Man', 'Dharmendar Ji', 'Opretion Members', 'Cost Per Pcs']:
                        block_data[key] = pd.to_numeric(sub_row[2], errors='coerce')
                    
                    # Extract Rates (often in Column 4 or 5)
                    for col_idx in [4, 5]:
                        key2 = str(sub_row[col_idx]).strip()
                        if key2 in ['Rate', 'Cost Accrued', 'Karigar Cost Without Expenses', 'More Cost']:
                            val = pd.to_numeric(sub_row[col_idx+1], errors='coerce')
                            if pd.notna(val): block_data[key2] = val
                            
        if current_sku and block_data: records.append(block_data)
        df_costs = pd.DataFrame(records)
    except Exception as e:
        print(f"Error parsing Cost.xlsx: {e}")
        return

    # --- 2. PARSE WORKER DATA (Link Workers to SKUs) ---
    print("Parsing Working.csv...")
    try:
        df_work = pd.read_csv('Karihgar Style.xlsx - Working.csv', header=None)
        # Headers are in Row 0, SKUs start from Column 14
        sku_headers = df_work.iloc[0, 14:].values
        workers = df_work.iloc[1:, 1].values # Worker Names in Col 1
        
        sku_worker_map = []
        for i, sku in enumerate(sku_headers):
            if pd.isna(sku) or str(sku).strip() in ['', 'Total', 'Diff', 'Charges']: continue
            
            # Get output values for this SKU column
            col_idx = 14 + i
            if col_idx >= df_work.shape[1]: break
            outputs = pd.to_numeric(df_work.iloc[1:, col_idx], errors='coerce').fillna(0)
            
            # Find workers with Output > 0
            active_workers = workers[outputs > 0]
            unique_workers = list(set([str(w).strip() for w in active_workers if pd.notna(w)]))
            
            if unique_workers:
                sku_worker_map.append({'SKU': str(sku).strip(), 'Worker_Team': unique_workers})
                
        df_workers = pd.DataFrame(sku_worker_map)
    except Exception as e:
        print(f"Error parsing Working.csv: {e}")
        df_workers = pd.DataFrame(columns=['SKU', 'Worker_Team'])

    # --- 3. MERGE & CALCULATE METRICS ---
    print("Merging Data...")
    df_costs['SKU_Clean'] = df_costs['SKU'].astype(str).str.strip().str.upper()
    if not df_workers.empty:
        df_workers['SKU_Clean'] = df_workers['SKU'].astype(str).str.strip().str.upper()
        df_master = pd.merge(df_costs, df_workers, on='SKU_Clean', how='left')
    else:
        df_master = df_costs.copy()

    # Rename & Calculate Final Columns
    df_master = df_master.rename(columns={
        'Rate': 'Software_Rate',
        'Cost Accrued': 'Actual_Total_Cost',
        'Karigar Cost Without Expenses': 'Base_Karigar_Cost',
        'More Cost': 'Variance_Per_Pc'
    })
    
    # Calculate Overhead (The "Hidden" Cost)
    df_master['Overhead_Per_Pc'] = df_master['Actual_Total_Cost'] - df_master['Base_Karigar_Cost']
    
    # Select Final Columns for Interface
    final_cols = ['SKU', 'Software_Rate', 'Base_Karigar_Cost', 'Overhead_Per_Pc', 'Actual_Total_Cost', 'Variance_Per_Pc', 'Worker_Team']
    df_final = df_master[[c for c in final_cols if c in df_master.columns]]
    
    df_final.to_csv('Master_Resolution_Report.csv', index=False)
    print("Success! 'Master_Resolution_Report.csv' created.")

if __name__ == "__main__":
    generate_master_report()
