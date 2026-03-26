import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

st.set_page_config(page_title="AI Study Planner", layout="centered")

st.markdown("## 📚 AI Study Planner")
st.caption("Plan smarter. Study better. 🚀")

# Sidebar
st.sidebar.title("📌 Menu")
option = st.sidebar.selectbox("Choose Option", ["Planner", "Analytics"])

file_name = "study_data.csv"

# Create file if not exists
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Name", "Subject", "Hours"])
    df.to_csv(file_name, index=False)

# ===================== PLANNER =====================
if option == "Planner":

    name = st.text_input("Enter your name")
    subjects = st.text_area("Enter subjects (comma separated)")
    hours = st.number_input("Study hours per day", min_value=1, max_value=12)

    study_log = {}

    if st.button("Generate Plan"):
        if subjects.strip() == "":
            st.warning("Please enter subjects")
        else:
            subject_list = subjects.split(",")
            time_per_subject = hours / len(subject_list)

            st.subheader("📅 Your Study Plan")
            for sub in subject_list:
                st.write(f"{sub.strip()} → {round(time_per_subject,2)} hrs")

    st.subheader("📊 Track Your Study")

    if subjects:
        for sub in subjects.split(","):
            study_log[sub.strip()] = st.number_input(f"Hours studied for {sub}", 0, 10)

        if st.button("Save Data"):
            df = pd.read_csv(file_name)

            for sub, hr in study_log.items():
                new_row = {"Name": name, "Subject": sub, "Hours": hr}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df.to_csv(file_name, index=False)
            st.success("Data Saved Successfully!")

# ===================== ANALYTICS =====================
elif option == "Analytics":

    st.subheader("📈 Analytics Dashboard")

    df = pd.read_csv(file_name)

    if not df.empty:
        fig, ax = plt.subplots()
        df.groupby("Subject")["Hours"].sum().plot(kind="bar", ax=ax)
        st.pyplot(fig)

        st.subheader("📅 Recent Data")
        st.dataframe(df.tail(10))
    else:
        st.warning("No data available. Please add data first.")