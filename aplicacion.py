import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="University Dashboard", layout="wide")

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("university_student_data.csv")

df = load_data()

st.title("📊 University Admissions & Retention Dashboard")
st.write("Interactive dashboard for student admissions, enrollment, retention and satisfaction.")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

year_options = ["All"] + sorted(df["Year"].unique().tolist())
term_options = ["All"] + sorted(df["Term"].unique().tolist())

selected_year = st.sidebar.selectbox("Select Year", year_options)
selected_term = st.sidebar.selectbox("Select Term", term_options)

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

if selected_term != "All":
    filtered_df = filtered_df[filtered_df["Term"] == selected_term]

# ----------------------------
# KPI Metrics
# ----------------------------
total_applications = filtered_df["Applications"].sum()
total_admitted = filtered_df["Admitted"].sum()
total_enrolled = filtered_df["Enrolled"].sum()

avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Applications", f"{total_applications}")
col2.metric("Admitted", f"{total_admitted}")
col3.metric("Enrolled", f"{total_enrolled}")
col4.metric("Avg Retention (%)", f"{avg_retention:.2f}")
col5.metric("Avg Satisfaction (%)", f"{avg_satisfaction:.2f}")

st.divider()

# ----------------------------
# Plot 1: Retention trend over time
# ----------------------------
st.subheader("📈 Retention Rate Trends Over Time")

retention_data = filtered_df.groupby("Year")["Retention Rate (%)"].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(8,4))
ax1.plot(retention_data["Year"], retention_data["Retention Rate (%)"], marker="o")
ax1.set_title("Retention Rate Over Time")
ax1.set_xlabel("Year")
ax1.set_ylabel("Retention Rate (%)")
ax1.grid(True)

st.pyplot(fig1)

# ----------------------------
# Plot 2: Satisfaction by year (bar chart)
# ----------------------------
st.subheader("📊 Student Satisfaction Scores by Year")

satisfaction_data = filtered_df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.bar(satisfaction_data["Year"], satisfaction_data["Student Satisfaction (%)"])
ax2.set_title("Student Satisfaction by Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Satisfaction (%)")
ax2.grid(True)

st.pyplot(fig2)

# ----------------------------
# Plot 3: Pie chart enrollment by department
# ----------------------------
st.subheader("🥧 Enrollment Distribution by Department")

dept_cols = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
dept_sum = filtered_df[dept_cols].sum()

fig3, ax3 = plt.subplots(figsize=(6,6))
ax3.pie(dept_sum, labels=dept_sum.index, autopct="%1.1f%%", startangle=90)
ax3.set_title("Enrollment by Department")

st.pyplot(fig3)

st.divider()

# ----------------------------
# Table preview
# ----------------------------
st.subheader("📄 Filtered Dataset Preview")
st.dataframe(filtered_df)