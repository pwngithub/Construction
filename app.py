
import streamlit as st
import pandas as pd

st.title("Fiber Pay Summary Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    df["Hours Worked"] = pd.to_numeric(df["Hours Worked"], errors="coerce")

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
    filtered_df.columns = filtered_df.columns.str.strip()

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
    total_hours = filtered_df['Hours Worked'].sum() if not filtered_df.empty and "Hours Worked" in filtered_df.columns else 0.00
    st.metric("Total Hours Worked", f"{total_hours:.2f}")

    st.subheader("📊 Summary by Technician")
    employee_data = []
    for _, row in filtered_df.iterrows():
        for col in emp_cols:
            tech = row.get(col)
            if pd.notna(tech):
                employee_data.append({
                    "Tech": tech,
                    "Hours Worked": row.get("Hours Worked", 0),
                    "Date": row.get("Date")
                })

    tech_df = pd.DataFrame(employee_data)

    if not tech_df.empty:
        summary = tech_df.groupby("Tech")["Hours Worked"].sum().reset_index().sort_values(by="Hours Worked", ascending=False)
        st.dataframe(summary)
        st.bar_chart(summary.set_index("Tech"))
    else:
        st.write("No technician data available for current filters.")

    st.subheader("📆 Daily Hours Trend")
    if not tech_df.empty:
        daily_summary = tech_df.groupby("Date")["Hours Worked"].sum().reset_index()
        st.line_chart(daily_summary.set_index("Date"))
    else:
        st.write("No data to show for daily trend.")

    st.subheader("📁 Project-Based Summary")
    if "Project" in filtered_df.columns:
        project_summary = filtered_df.groupby("Project")["Hours Worked"].sum().reset_index().sort_values(by="Hours Worked", ascending=False)
        st.dataframe(project_summary)
        st.bar_chart(project_summary.set_index("Project"))
    else:
        st.write("No project data found.")

    st.subheader("⬇️ Export Filtered Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered Data as CSV", data=csv, file_name="filtered_fiber_pay.csv", mime="text/csv")


    st.subheader("🔍 Summary by Keyword Mentions in Notes")
    keyword_counts = {
        "FAT": 0,
        "Splice enclosure": 0,
        "Patch panel": 0
    }

    for kw in keyword_counts:
        count = df["Notes:"].astype(str).str.contains(kw, case=False, na=False).sum()
        count += df["Amy's Notes"].astype(str).str.contains(kw, case=False, na=False).sum()
        keyword_counts[kw] = count

    summary_df = pd.DataFrame(keyword_counts.items(), columns=["Keyword", "Occurrences"])
    st.dataframe(summary_df)
    st.bar_chart(summary_df.set_index("Keyword"))
