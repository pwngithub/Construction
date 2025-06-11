
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fiber Pay Dashboard", layout="wide")

uploaded_file = st.file_uploader("Upload Fiber Pay Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    df["Hours Worked"] = pd.to_numeric(df["Hours Worked"], errors="coerce")

    st.sidebar.header("Filters")
    projects = df["Project"].dropna().unique()
    selected_project = st.sidebar.selectbox("Select Project", ["All"] + list(projects))
    dates = df["Date"].dropna().astype(str).unique()
    selected_date = st.sidebar.selectbox("Select Date", ["All"] + sorted(dates))

    filtered_df = df.copy()
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project"] == selected_project]
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["Date"].astype(str) == selected_date]

    st.subheader("Summary")
    total_hours = filtered_df['Hours Worked'].sum() if not filtered_df.empty else 0
    st.metric("Total Hours Worked", f"{total_hours:.2f}")

    st.subheader("📊 Summary by Technician")
    tech_summary = filtered_df.groupby("Employee")["Hours Worked"].sum().reset_index()
    st.dataframe(tech_summary)
    st.bar_chart(tech_summary.set_index("Employee"))

    st.subheader("📈 Daily Trend")
    if "Date" in filtered_df.columns:
        trend = filtered_df.groupby("Date")["Hours Worked"].sum().reset_index()
        trend["Date"] = pd.to_datetime(trend["Date"])
        trend = trend.sort_values("Date")
        st.line_chart(trend.set_index("Date"))

    st.subheader("📁 Filtered Data")
    st.dataframe(filtered_df)
