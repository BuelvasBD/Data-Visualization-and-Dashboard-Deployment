import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="University Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------
# Custom Style (CSS)
# ----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2a2f3a;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #c7c7c7;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "university_student_data.csv")
    return pd.read_csv(file_path)

df = load_data()

# ----------------------------
# Title
# ----------------------------
st.markdown("<h1 style='text-align: center;'>🎓 University Student Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Admissions, Enrollment, Retention and Satisfaction Insights</p>", unsafe_allow_html=True)

st.divider()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("📌 Filters")

year_options = ["All"] + sorted(df["Year"].unique().tolist())
term_options = ["All"] + sorted(df["Term"].unique().tolist())

selected_year = st.sidebar.selectbox("📅 Select Year", year_options)
selected_term = st.sidebar.selectbox("📖 Select Term", term_options)

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

if selected_term != "All":
    filtered_df = filtered_df[filtered_df["Term"] == selected_term]

# ----------------------------
# KPIs
# ----------------------------
total_applications = int(filtered_df["Applications"].sum())
total_admitted = int(filtered_df["Admitted"].sum())
total_enrolled = int(filtered_df["Enrolled"].sum())

avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📩 Applications", f"{total_applications:,}")
col2.metric("✅ Admitted", f"{total_admitted:,}")
col3.metric("🎓 Enrolled", f"{total_enrolled:,}")
col4.metric("📈 Avg Retention", f"{avg_retention:.2f}%")
col5.metric("⭐ Avg Satisfaction", f"{avg_satisfaction:.2f}%")

st.divider()

# ----------------------------
# Layout Charts
# ----------------------------
left, right = st.columns(2)

# ----------------------------
# Chart 1: Retention over time
# ----------------------------
with left:
    st.subheader("📈 Retention Rate Trend")

    retention_data = filtered_df.groupby("Year")["Retention Rate (%)"].mean().reset_index()

    fig1, ax1 = plt.subplots(figsize=(7,4))
    ax1.plot(retention_data["Year"], retention_data["Retention Rate (%)"], marker="o", linewidth=2)
    ax1.set_title("Retention Rate Over Years")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Retention Rate (%)")
    ax1.grid(True, alpha=0.3)

    st.pyplot(fig1)

# ----------------------------
# Chart 2: Satisfaction by year
# ----------------------------
with right:
    st.subheader("📊 Satisfaction Score by Year")

    satisfaction_data = filtered_df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(7,4))
    ax2.bar(satisfaction_data["Year"], satisfaction_data["Student Satisfaction (%)"])
    ax2.set_title("Student Satisfaction Over Years")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Satisfaction (%)")
    ax2.grid(True, axis="y", alpha=0.3)

    st.pyplot(fig2)

st.divider()

# ----------------------------
# Enrollment Distribution
# ----------------------------
st.subheader("🏫 Enrollment Distribution by Department")

dept_cols = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
dept_sum = filtered_df[dept_cols].sum()

colA, colB = st.columns([1, 2])

with colA:
    fig3, ax3 = plt.subplots(figsize=(5,5))
    ax3.pie(dept_sum, labels=dept_sum.index, autopct="%1.1f%%", startangle=90)
    ax3.set_title("Enrollment Share")

    st.pyplot(fig3)

with colB:
    st.markdown("### 📌 Department Enrollment Totals")

    dept_table = pd.DataFrame({
        "Department": dept_sum.index,
        "Total Enrolled": dept_sum.values.astype(int)
    })

    st.dataframe(dept_table, use_container_width=True)

st.divider()

# ----------------------------
# Extra Chart: Spring vs Fall Comparison
# ----------------------------
st.subheader("📖 Spring vs Fall Comparison (Total Enrolled)")

term_data = filtered_df.groupby("Term")["Enrolled"].sum().reset_index()

fig4, ax4 = plt.subplots(figsize=(8,4))
ax4.bar(term_data["Term"], term_data["Enrolled"])
ax4.set_title("Enrolled Students by Term")
ax4.set_xlabel("Term")
ax4.set_ylabel("Total Enrolled")
ax4.grid(True, axis="y", alpha=0.3)

st.pyplot(fig4)

st.divider()

# ----------------------------
# Dataset Preview
# ----------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown(
    "<p style='text-align: center; color: gray;'>Developed for Data Mining - Universidad de la Costa</p>",
    unsafe_allow_html=True
)
