
import streamlit as st
import pandas as pd
import re

st.title("Fiber Pay Summary Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Define employee columns
    emp_cols = [col for col in df.columns if col.startswith('Employee')]
    all_employees = pd.unique(df[emp_cols].values.ravel('K'))
    all_employees = [e for e in all_employees if pd.notna(e)]

    # Dropdown filters
    date_options = sorted(df['Date'].dropna().unique())
    project_options = sorted(df['Project'].dropna().unique())

    selected_date = st.selectbox("Filter by Date", ["All"] + list(date_options))
    selected_project = st.selectbox("Filter by Project", ["All"] + list(project_options))
    selected_employee = st.selectbox("Filter by Employee", ["All"] + list(all_employees))
    keyword_filter = st.multiselect("Filter by Keywords in Notes", ["FAT", "Splice enclosure", "Patch panel"])

    # Apply filters
    filtered_df = df.copy()
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project"] == selected_project]
    if selected_employee != "All":
        filtered_df = filtered_df[df[emp_cols].isin([selected_employee]).any(axis=1)]
    if keyword_filter:
        keyword_regex = "|".join(keyword_filter)
        filtered_df = filtered_df[
            filtered_df.get("Notes:", "").astype(str).str.contains(keyword_regex, case=False, na=False) |
            filtered_df.get("Amy's Notes", "").astype(str).str.contains(keyword_regex, case=False, na=False)
        ]

    st.subheader("Filtered Results")
    st.dataframe(filtered_df)

    st.subheader("Summary")
    total_hours = filtered_df['Hours Worked'].sum()
    st.metric("Total Hours Worked", f"{total_hours:.2f}")

    
    else:
        st.write("No numbers found in notes.")
