import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
st.title("Construction Daily Workflow Dashboard")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%b %-d, %Y")
    employee_cols = ["Employee", "Employee.1", "Employee.2", "Employee.3", "Employee.4", "Employee.5"]
    all_employees = pd.unique(df[employee_cols].values.ravel("K"))
    all_employees = [e for e in all_employees if pd.notna(e)]
    techs = sorted(df["Who filled this out?"].dropna().unique())
    projects = sorted(df["Project or labor?"].dropna().unique())
    trucks = sorted(df["What Truck?"].dropna().unique())
    full_dates = df["Date"].dropna().unique()
    dates = sorted(full_dates)
    st.sidebar.header("Filter Options")
    selected_techs = st.sidebar.multiselect("Filter by Technicians (Any Match)", all_employees, key="filter_tech")
    require_all_techs = st.sidebar.toggle("Require All Selected Techs", key="toggle_all_techs")
    selected_proj = st.sidebar.selectbox("Filter by Project", ["All"] + projects, key="filter_project")
    selected_truck = st.sidebar.selectbox("Filter by Truck", ["All"] + trucks, key="filter_truck")
    selected_date = st.sidebar.selectbox("Filter by Date", ["All"] + dates, key="filter_date")
    filtered_df = df.copy()
    if selected_proj != "All":
        filtered_df = filtered_df[filtered_df["Project or labor?"] == selected_proj]
    if selected_truck != "All":
        filtered_df = filtered_df[filtered_df["What Truck?"] == selected_truck]
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if selected_techs:
        if require_all_techs:
            filtered_df = filtered_df[
                filtered_df[employee_cols].apply(lambda row: all(emp in row.values for emp in selected_techs), axis=1)
            ]
        else:
            filtered_df = filtered_df[
                filtered_df[employee_cols].apply(lambda row: any(emp in row.values for emp in selected_techs), axis=1)
            ]
    def extract_footage_by_activity(row):
        activity = str(row.get("What did you do.", "")).lower()
        source_col = None
        if "lashed fiber" in activity:
            source_col = "Fiber Lash Info."
        elif "pulled fiber" in activity:
            source_col = "Fiber pull Info."
        elif "strand" in activity:
            source_col = "Stand info"
        elif "drive off" in activity:
            source_col = "Fiber Lash Info."
        if source_col and source_col in row:
            text = str(row.get(source_col, ""))
            if "strand" in activity:
                matches = re.findall(r'(\d+(?:,\d+)?)', text)
                if matches:
                    try:
                        return float(matches[-1].replace(",", ""))
                    except:
                        return 0
            else:
                match = re.search(r'Footage[:\-]?\s*([0-9,]+)', text, re.IGNORECASE)
                if match:
                    try:
                        return float(match.group(1).replace(",", ""))
                    except:
                        return 0
        return 0
    def assign_footage(data):
        data = data.copy()
        data["Footage"] = data.apply(extract_footage_by_activity, axis=1)
        return data
    filtered_df = assign_footage(filtered_df)
    lash_df = filtered_df[filtered_df["What did you do."].str.contains("Lashed Fiber", na=False)]
    pull_df = filtered_df[filtered_df["What did you do."].str.contains("Pulled Fiber", na=False)]
    strand_df = filtered_df[filtered_df["What did you do."].str.contains("Strand", na=False)]
    drive_df = filtered_df[filtered_df["What did you do."].str.contains("Drive off", na=False)]
    st.subheader("Summary")
    st.write({
        "Fiber Lash Footage": lash_df["Footage"].sum(),
        "Fiber Pull Footage": pull_df["Footage"].sum(),
        "Strand Footage": strand_df["Footage"].sum(),
        "Drive Off Footage": drive_df["Footage"].sum()
    })
    st.subheader("Footage Bar Charts per Technician")
    def plot_footage(data, label):
        tech_footage = data.groupby("Who filled this out?")["Footage"].sum()
        if not tech_footage.empty:
            st.write(f"### {label}")
            fig, ax = plt.subplots()
            tech_footage.plot(kind="bar", ax=ax)
            ax.set_ylabel("Footage")
            ax.set_xlabel("Technician")
            st.pyplot(fig)
    plot_footage(lash_df, "Fiber Lash")
    plot_footage(pull_df, "Fiber Pull")
    plot_footage(strand_df, "Strand")
    plot_footage(drive_df, "Drive Off")
    st.subheader("Work Summary (Grouped by Date and Project)")
    def build_summary_from_row(row):
        employees = [row.get(f"Employee{i}" if i > 0 else "Employee") for i in range(6)]
        employees = [str(emp) for emp in employees if pd.notna(emp)]
        employee_str = ", ".join(employees[:-1]) + f" and {employees[-1]}" if len(employees) > 1 else employees[0] if employees else "Unknown"
        truck = row.get("What Truck?", "Unknown Truck")
        action = row.get("What did you do.", "Unknown Action")
        fiber = row.get("Fiber", "Unknown Fiber")
        footage = row.get("Footage", 0)
        if employees and footage > 0:
            return f"{employee_str} used {truck} to do {action} with {fiber} for {int(footage)} feet."
        return None
    summary_groups = []
    for (date, project), group in filtered_df.groupby(["Date", "Project or labor?"], dropna=False):
        group_summary = []
        for _, row in group.iterrows():
            sentence = build_summary_from_row(row)
            if sentence:
                group_summary.append(sentence)
        if group_summary:
            summary_groups.append((date, project, group_summary))
    if summary_groups:
        for date, project, summaries in summary_groups:
            st.markdown(f"### 📅 {date} — 📁 {project if pd.notna(project) else 'Unspecified'}")
            for line in summaries:
                st.markdown(f"- {line}")
    else:
        st.write("No grouped summaries found for the selected filters.")
    st.subheader("Export Filtered Results")
    @st.cache_data
    # Removed CSV export logic
            # Removed csv_data assignment         with st.container():
            data=csv_data,
        )
    st.subheader("Export Filtered Results")
    @st.cache_data
    # Removed CSV export logic
    def         from 
        def safe(text):
            return text.replace("—", "-")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_title("Filtered Construction Summary Report")
        pdf.cell(200, 10, txt="Filtered Construction Summary Report", ln=True, align='C')
        pdf.ln(5)
        for date, project, summaries in groups:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=safe(f"{date} - {project if pd.notna(project) else 'Unspecified'}"), ln=True)
            pdf.set_font("Arial", size=11)
            for summary in summaries:
                pdf.multi_cell(0, 8, txt=safe(f"- {summary}"))
            pdf.ln(2)
        output_path = "/mnt/data/filtered_construction_summary.pdf"
        pdf.output(output_path)
        return output_path
            # Removed csv_data assignment         with st.container():
            data=csv_data,
        )
                            label="📄 Download Filtered Summary as PDF",
                data=f,
                                            )