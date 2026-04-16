import wrds
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io

# --- Page Configuration ---
st.set_page_config(page_title="Financial Analysis Dashboard", layout="wide")

st.title("📊 Corporate Financial Analysis Tool")
st.markdown("""
This tool analyzes financial metrics (ROA, ROE, Profit Margin, etc.) for Chinese listed companies using WRDS data.
""")

# --- Sidebar for Inputs ---
st.sidebar.header("Configuration")

# 1. Username Input (Using secrets for security in production, or input for demo)
# Ideally, set your username in Streamlit Cloud Secrets as 'WRDS_USERNAME'
# For local testing, you can type it here.
username = st.sidebar.text_input("WRDS Username", value="yycc", type="password")

# 2. Company Input
st.sidebar.subheader("Add Companies")
st.sidebar.write("Format: StockCode,CompanyName (e.g., 000333,Midea)")

# Session state to store the list of companies
if 'stock_code_map' not in st.session_state:
    st.session_state.stock_code_map = {}

# Input fields for a new company
new_code = st.sidebar.text_input("Stock Code")
new_name = st.sidebar.text_input("Company Name")

if st.sidebar.button("Add Company"):
    if new_code and new_name:
        st.session_state.stock_code_map[new_code.strip()] = new_name.strip()
        st.sidebar.success(f"Added {new_name}!")
        # Clear input after adding (optional, in Streamlit we usually just let user overwrite)
    else:
        st.sidebar.error("Please enter both Code and Name.")

# Display current list
st.sidebar.subheader("Current Selection")
if st.session_state.stock_code_map:
    for code, name in st.session_state.stock_code_map.items():
        st.sidebar.text(f"{code} -> {name}")
    
    if st.sidebar.button("Clear All"):
        st.session_state.stock_code_map = {}
        st.experimental_rerun()
else:
    st.sidebar.warning("No companies added yet.")

# --- Main Analysis Logic ---
if st.session_state.stock_code_map:
    stock_code_map = st.session_state.stock_code_map
    
    if st.button("Run Analysis", type="primary"):
        with st.spinner("Connecting to WRDS and fetching data..."):
            try:
                # 1. Database Connection
                db = wrds.Connection(wrds_username=username)
                
                # 2. Prepare Query
                stock_code_list = list(stock_code_map.keys())
                start_date = "2020-01-01"
                end_date = "2025-12-31"
                
                selected_columns = "stkcd, accper, typrep, b002000000, a001000000, a001100000, a003000000, b001100000, a002000000, a002100000"

                if len(stock_code_list) == 1:
                    sql_query = f"""
                    SELECT {selected_columns}
                    FROM csmar.wrds_csmar_financial_master
                    WHERE stkcd = '{stock_code_list[0]}'
                    AND accper BETWEEN '{start_date}' AND '{end_date}'
                    AND typrep = 'A'
                    """
                else:
                    sql_query = f"""
                    SELECT {selected_columns}
                    FROM csmar.wrds_csmar_financial_master
                    WHERE stkcd IN {tuple(stock_code_list)}
                    AND accper BETWEEN '{start_date}' AND '{end_date}'
                    AND typrep = 'A'
                    """
                
                raw_data = db.raw_sql(sql_query, date_cols=["accper"])
                db.close()
                
                # 3. Data Processing
                raw_data = raw_data.rename(columns={
                    "b002000000": "Net Profit",
                    "a001000000": "Total Assets",
                    "a001100000": "Total Current Assets",
                    "a003000000": "Equity",
                    "b001100000": "Revenue",
                    "a002000000": "Total Liabilities",
                    "a002100000": "Total Current Liabilities"
                })

                required_cols = ['Net Profit', 'Total Assets', 'Total Current Assets', 'Equity', 'Revenue', 'Total Liabilities', 'Total Current Liabilities']
                clean_data = raw_data.dropna(subset=required_cols).copy()
                clean_data = clean_data[clean_data['accper'].dt.month == 12]

                clean_data['stkcd'] = clean_data['stkcd'].astype(str)
                clean_data['company_name'] = clean_data['stkcd'].replace(stock_code_map)
                clean_data = clean_data.dropna(subset=['company_name'])

                if clean_data.empty:
                    st.error("No data found for the selected companies/date range.")
                else:
                    clean_data['fiscal_year'] = clean_data['accper'].dt.year

                    # Calculate Ratios
                    clean_data['ROA'] = (clean_data['Net Profit'] / clean_data['Total Assets']) * 100
                    clean_data['ROE'] = (clean_data['Net Profit'] / clean_data['Equity']) * 100 
                    clean_data['Net Profit Margin'] = (clean_data['Net Profit'] / clean_data['Revenue']) * 100 
                    clean_data['Current Ratio'] = clean_data['Total Current Assets'] / clean_data['Total Current Liabilities'] 
                    clean_data['Total Debt Ratio'] = (clean_data['Total Liabilities'] / clean_data['Total Assets']) * 100 

                    final_cols = ['company_name', 'fiscal_year', 'ROA', 'ROE', 'Net Profit Margin', 'Current Ratio', 'Total Debt Ratio']
                    final_data = clean_data[final_cols].sort_values(['company_name', 'fiscal_year'])

                    # --- Display Results ---
                    st.success("Analysis Complete!")
                    
                    # 1. Data Table
                    st.subheader("Financial Data Summary")
                    st.dataframe(final_data)

                    # 2. Download Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        final_data.to_excel(writer, index=False, sheet_name='Analysis')
                    st.download_button(
                        label="Download Excel File",
                        data=output.getvalue(),
                        file_name="WRDS_Financial_Analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                    # 3. Charts
                    st.subheader("Trend Analysis")
                    
                    # Plotting settings
                    plt.style.use('seaborn-v0_8-whitegrid')
                    plt.rcParams['font.size'] = 10
                    # Note: SimHei might not be installed on Streamlit Cloud. 
                    # We use standard fonts or try to load it.
                    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial'] 
                    plt.rcParams['axes.unicode_minus'] = False

                    # Create columns for layout
                    col1, col2 = st.columns(2)

                    metrics = [
                        ("Net Profit Margin", "Profit Margin (%)"),
                        ("ROA", "ROA (%)"),
                        ("ROE", "ROE (%)"),
                        ("Current Ratio", "Current Ratio (Times)"),
                        ("Total Debt Ratio", "Debt Ratio (%)")
                    ]

                    for i, (metric, ylabel) in enumerate(metrics):
                        fig, ax = plt.subplots(figsize=(6, 4))
                        
                        for company in final_data['company_name'].unique():
                            temp = final_data[final_data.company_name == company]
                            ax.plot(temp.fiscal_year, temp[metric], marker='o', label=company, linewidth=2)
                        
                        ax.set_title(f"{metric} ({start_date[:4]}-{end_date[:4]})")
                        ax.set_ylabel(ylabel)
                        ax.legend()
                        
                        # Use columns to place charts side by side
                        if i % 2 == 0:
                            with col1:
                                st.pyplot(fig)
                        else:
                            with col2:
                                st.pyplot(fig)
                        
                        plt.close(fig)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
else:
    st.info("👈 Please add companies from the sidebar to begin.")
