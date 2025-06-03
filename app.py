
import streamlit as st
import pandas as pd
import re

st.title("Fiber Pay Summary Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalize column names
    df.columns = df.columns.str.strip()

    # Prepare filters
    date_options = sorted(df['Date'].dropna().unique())
    project_options = sorted(df['Project'].dropna().unique())

    # Combine all Employee columns to one list
    emp_cols = [col for col in df.columns if col.startswith('Employee')]
    all_employees = pd.unique(df[emp_cols].values.ravel('K'))
    all_employees = [e for e in all_employees if pd.notna(e)]

    selected_date = st.selectbox("Filter by Date", ["All"] + list(date_options))
    selected_project = st.selectbox("Filter by Project", ["All"] + list(project_options))
    selected_employee = st.selectbox("Filter by Employee", ["All"] + list(all_employees))

    # Apply filters
    filtered_df = df.copy()
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project"] == selected_project]
    if selected_employee != "All":
        filtered_df = filtered_df[df[emp_cols].isin([selected_employee]).any(axis=1)]

    st.subheader("Filtered Results")
    st.dataframe(filtered_df)

    st.subheader("Summary")
    total_hours = filtered_df['Hours Worked'].sum()
    st.metric("Total Hours Worked", f"{total_hours:.2f}")

    # Extract numbers from both Notes columns
    def extract_numbers(text):
        if pd.isna(text):
            return []
        return [int(n) for n in re.findall(r'\b\d+\b', str(text))]

    notes1 = filtered_df.get("Notes:", pd.Series([], dtype=str)).apply(extract_numbers)
    notes2 = filtered_df.get("Amy's Notes", pd.Series([], dtype=str)).apply(extract_numbers)

    all_numbers = [num for sublist in notes1 for num in sublist] +                   [num for sublist in notes2 for num in sublist]

    if all_numbers:
        st.write("📊 Extracted Numbers from Notes:")
        st.write(all_numbers)
        st.write("Sum of Extracted Numbers:", sum(all_numbers))
    else:
        st.write("No numbers found in notes.")
