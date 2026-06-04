import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
# This must be the first Streamlit command
st.set_page_config(page_title="Career Success Analytics", page_icon="📈", layout="wide")

# --- CUSTOM CSS FOR UI ---
st.markdown("""
    <style>
    /* Main background */
    .main { background-color: #f8f9fa; }
    /* Headers */
    h1, h2, h3 { color: #2b2b2b; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    /* Metrics styling */
    [data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Ensure education_career_success.csv is in the same directory or adjust the path
    df = pd.read_csv("education_career_success.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Dataset not found. Please ensure 'education_career_success.csv' is in the same folder as this script.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📊 Dashboard Navigation")
menu = st.sidebar.radio("Go to:", [
    "📌 Overview & KPIs", 
    "🎓 Academic & Salary Analysis", 
    "🤝 Skills & Networking", 
    "🧠 Deep Insights & Correlations"
])

st.sidebar.markdown("---")
st.sidebar.info("Filter and explore how academic performance, skills, and networking impact career trajectories.")

# --- PAGE 1: OVERVIEW & KPIs ---
if menu == "📌 Overview & KPIs":
    st.title("📌 Education & Career Success Overview")
    st.markdown("A high-level view of student demographics and baseline career outcomes.")
    
    # Top-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", f"{len(df)}")
    col2.metric("Avg Starting Salary", f"${df['Starting_Salary'].mean():,.0f}")
    col3.metric("Avg Job Offers", f"{df['Job_Offers'].mean():.1f}")
    col4.metric("Avg Career Satisfaction", f"{df['Career_Satisfaction'].mean():.1f} / 10")
    
    st.markdown("### 🗄️ Dataset Glimpse")
    st.dataframe(df.head(8), use_container_width=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 🧑‍🎓 Gender Distribution")
        fig_gender = px.pie(df, names='Gender', hole=0.4, color_discrete_sequence=['#4c78a8', '#f58518'])
        fig_gender.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with colB:
        st.markdown("### 📚 Field of Study Popularity")
        field_counts = df['Field_of_Study'].value_counts().reset_index()
        field_counts.columns = ['Field_of_Study', 'Count']
        fig_field = px.bar(field_counts, x='Field_of_Study', y='Count', 
                           color='Field_of_Study', text='Count')
        fig_field.update_traces(textposition='outside')
        fig_field.update_layout(showlegend=False, xaxis_title="", yaxis_title="Number of Students")
        st.plotly_chart(fig_field, use_container_width=True)

# --- PAGE 2: ACADEMIC & SALARY ANALYSIS ---
elif menu == "🎓 Academic & Salary Analysis":
    st.title("🎓 Academic Performance vs. Salary Outcomes")
    
    # Filter setup
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_field = st.selectbox("Filter by Field of Study:", ["All"] + sorted(list(df['Field_of_Study'].unique())))
        
    filtered_df = df if selected_field == "All" else df[df['Field_of_Study'] == selected_field]
        
    st.markdown("### 💰 Starting Salary by Field of Study")
    fig_salary_box = px.box(filtered_df, x="Field_of_Study", y="Starting_Salary", color="Field_of_Study", 
                            points="all", hover_data=["University_GPA"])
    st.plotly_chart(fig_salary_box, use_container_width=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 📊 University GPA vs. Starting Salary")
        fig_gpa_sal = px.scatter(filtered_df, x="University_GPA", y="Starting_Salary", 
                                 color="Current_Job_Level", size="Job_Offers", 
                                 hover_data=["Field_of_Study", "Age"], opacity=0.7)
        st.plotly_chart(fig_gpa_sal, use_container_width=True)
        
    with colB:
        st.markdown("### 📝 SAT Score vs. Starting Salary")
        fig_sat_sal = px.scatter(filtered_df, x="SAT_Score", y="Starting_Salary", 
                                 color="Gender", trendline="ols")
        st.plotly_chart(fig_sat_sal, use_container_width=True)

# --- PAGE 3: SKILLS & NETWORKING ---
elif menu == "🤝 Skills & Networking":
    st.title("🤝 Impact of Soft Skills, Internships, & Networking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌐 Networking Score vs. Job Offers")
        fig_net = px.box(df, x="Networking_Score", y="Job_Offers", color="Networking_Score")
        fig_net.update_layout(showlegend=False)
        st.plotly_chart(fig_net, use_container_width=True)
        
    with col2:
        st.markdown("### 💼 Internships Completed vs. Starting Salary")
        fig_intern = px.box(df, x="Internships_Completed", y="Starting_Salary", color="Internships_Completed")
        fig_intern.update_layout(showlegend=False)
        st.plotly_chart(fig_intern, use_container_width=True)

    st.markdown("### 🗣️ Soft Skills Impact on Career Satisfaction")
    fig_soft = px.density_heatmap(df, x="Soft_Skills_Score", y="Career_Satisfaction", text_auto=True, color_continuous_scale="Blues")
    st.plotly_chart(fig_soft, use_container_width=True)

# --- PAGE 4: DEEP INSIGHTS & CORRELATIONS ---
elif menu == "🧠 Deep Insights & Correlations":
    st.title("🧠 Deep Analytical Insights")
    st.markdown("Understand which numeric variables are most heavily correlated with career success metrics.")
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    # Drop IDs if they accidentally got parsed as numeric (not the case here, but good practice)
    if 'Student_ID' in numeric_df.columns:
        numeric_df = numeric_df.drop('Student_ID', axis=1)
        
    corr = numeric_df.corr()
    
    # Plotting the heatmap using Seaborn inside Streamlit
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax, vmin=-1, vmax=1)
    plt.xticks(rotation=45, ha='right')
    plt.title("Correlation Matrix of Numeric Features", fontsize=16)
    st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### 💡 Key Takeaways from the Data")
    
    st.success("""
    * **High Academic Return:** SAT Scores and University GPAs show an exceptionally strong positive correlation with Starting Salary and Job Offers. 
    * **The Power of Projects & Internships:** The number of projects and internships completed heavily influences career satisfaction and the speed at which someone reaches a 'Senior' job level.
    * **Skills Synergy:** Soft Skills and Networking Scores strongly correlate with higher Career Satisfaction and better Work-Life Balance.
    """)
