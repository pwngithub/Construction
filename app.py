
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Construction Daily Workflow Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Normalize column names
    df.columns = df.columns.str.strip()
    
    # Filters
    techs = df["Who filled this out?"].dropna().unique()
    projects = df["Project or labor?"].dropna().unique()

    selected_tech = st.selectbox("Filter by Technician", ["All"] + list(techs))
    selected_project = st.selectbox("Filter by Project/Labor", ["All"] + list(projects))

    filtered_df = df.copy()
    if selected_tech != "All":
        filtered_df = filtered_df[filtered_df["Who filled this out?"] == selected_tech]
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project or labor?"] == selected_project]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Analyze Fiber, Lash, and Strand based on activity descriptions
    fiber_lash = filtered_df[filtered_df["What did you do."].str.contains("Lashed Fiber", na=False)]
    fiber_pull = filtered_df[filtered_df["What did you do."].str.contains("Pulled Fiber", na=False)]
    strand_work = filtered_df[filtered_df["What did you do."].str.contains("Strand", na=False)]

    summary = {
        "Fiber Lash Count": len(fiber_lash),
        "Fiber Pull Count": len(fiber_pull),
        "Strand Work Count": len(strand_work)
    }

    st.subheader("Summary")
    st.write(summary)

    # Bar chart by technician for activity type
    st.subheader("Bar Charts per Technician")

    for label, data in [("Fiber Lash", fiber_lash), ("Fiber Pull", fiber_pull), ("Strand Work", strand_work)]:
        count_by_tech = data["Who filled this out?"].value_counts()
        if not count_by_tech.empty:
            st.write(f"### {label}")
            fig, ax = plt.subplots()
            count_by_tech.plot(kind="bar", ax=ax)
            ax.set_ylabel("Count")
            ax.set_xlabel("Technician")
            st.pyplot(fig)
