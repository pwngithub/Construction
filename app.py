
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.title("Construction Daily Workflow Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    # Filters
    techs = df["Who filled this out?"].dropna().unique()
    projects = df["Project or labor?"].dropna().unique()
    trucks = df["What Truck?"].dropna().unique()

    selected_tech = st.selectbox("Filter by Technician", ["All"] + list(techs))
    selected_project = st.selectbox("Filter by Project/Labor", ["All"] + list(projects))
    selected_truck = st.selectbox("Filter by Truck", ["All"] + list(trucks))

    filtered_df = df.copy()
    if selected_tech != "All":
        filtered_df = filtered_df[filtered_df["Who filled this out?"] == selected_tech]
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project or labor?"] == selected_project]
    if selected_truck != "All":
        filtered_df = filtered_df[filtered_df["What Truck?"] == selected_truck]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    def extract_footage_from_notes(text):
        if isinstance(text, str):
            match = re.search(r'Footage[:\-]?\s*([0-9,]+)', text, re.IGNORECASE)
            if match:
                num = match.group(1).replace(",", "")
                try:
                    return float(num)
                except:
                    return 0
        return 0

    def assign_footage(data):
        data = data.copy()
        data["Footage"] = data["Notes:"].apply(extract_footage_from_notes)
        return data

    # Identify activity types and extract footage from Notes
    lash_df = assign_footage(filtered_df[filtered_df["What did you do."].str.contains("Lashed Fiber", na=False)])
    pull_df = assign_footage(filtered_df[filtered_df["What did you do."].str.contains("Pulled Fiber", na=False)])
    strand_df = assign_footage(filtered_df[filtered_df["What did you do."].str.contains("Strand", na=False)])

    lash_total = lash_df["Footage"].sum()
    pull_total = pull_df["Footage"].sum()
    strand_total = strand_df["Footage"].sum()

    st.subheader("Summary")
    st.write({
        "Fiber Lash Footage": lash_total,
        "Fiber Pull Footage": pull_total,
        "Strand Footage": strand_total
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

    plot_footage(lash_df, "Fiber Lash Footage")
    plot_footage(pull_df, "Fiber Pull Footage")
    plot_footage(strand_df, "Strand Footage")
