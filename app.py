import streamlit as st
import pandas as pd

st.title("🧵 Stitching Department Costing Automation")

st.write("This app automatically loads all Excel files, merges them, and calculates costing.")

# --------------------------------------
# 1️⃣ Load All Excel Files
# --------------------------------------
@st.cache_data
def load_data():
    rate_sheet = pd.read_excel('Rate Sheet.xlsx')
    style_sheet = pd.read_excel('Karighar Style.xlsx')
    daily_report = pd.read_excel('Daily SKU wise Report.xlsx')
    costing_working = pd.read_excel('Costing Working.xlsx')
    cost_file = pd.read_excel('Cost.xlsx')

    return rate_sheet, style_sheet, daily_report, costing_working, cost_file

rate_sheet, style_sheet, daily_report, costing_working, cost_file = load_data()

st.success("All Excel files loaded successfully ✔")

# --------------------------------------
# 2️⃣ Clean Column Names
# --------------------------------------
def clean_cols(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

rate_sheet = clean_cols(rate_sheet)
style_sheet = clean_cols(style_sheet)
daily_report = clean_cols(daily_report)
costing_working = clean_cols(costing_working)
cost_file = clean_cols(cost_file)

# --------------------------------------
# 3️⃣ Merge Style Sheet with Rate Sheet
# --------------------------------------
merged_1 = style_sheet.merge(rate_sheet, on="style", how="left")

# --------------------------------------
# 4️⃣ Merge with Daily SKU-wise Report
# --------------------------------------
merged_2 = merged_1.merge(daily_report, on="sku", how="left")

# --------------------------------------
# 5️⃣ Merge with Cost File for Final Costing
# --------------------------------------
final_cost = merged_2.merge(cost_file, on="style", how="left")

# --------------------------------------
# 6️⃣ Show Output
# --------------------------------------
st.subheader("📌 Final Costing Output")
st.dataframe(final_cost)

# --------------------------------------
# 7️⃣ Download Button
# --------------------------------------
@st.cache_data
def convert_df(df):
    return df.to_excel(index=False, engine='openpyxl')

excel_file = convert_df(final_cost)

st.download_button(
    label="⬇ Download Final Costing Excel",
    data=excel_file,
    file_name="Final_Costing.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
