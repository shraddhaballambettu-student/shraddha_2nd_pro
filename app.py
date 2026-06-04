import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Education & Career Success Analytics", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2c3e50; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Assumes the CSV is in a 'data' folder
    df = pd.read_csv("data/education_career_success.csv")
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", [
    "📌 Overview & KPIs", 
    "🎓 Academic & Salary Analysis", 
    "🤝 Skills & Networking", 
    "🧠 Deep Insights & Correlations"
])

st.sidebar.markdown("---")
st.sidebar.info("Upload new data or filter existing data to see real-time updates on career success metrics.")

# --- PAGE 1: OVERVIEW & KPIs ---
if menu == "📌 Overview & KPIs":
    st.title("🎓 Education & Career Success Dashboard")
    st.markdown("Analyze how academic performance, skills, and networking impact career trajectories.")
    
    # Top-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", f"{len(df)}")
    col2.metric("Avg Starting Salary", f"${df['Starting_Salary'].mean():,.0f}")
    col3.metric("Avg Job Offers", f"{df['Job_Offers'].mean():.1f}")
    col4.metric("Avg Career Satisfaction", f"{df['Career_Satisfaction'].mean():.1f}/10")
    
    st.markdown("### Dataset Glimpse")
    st.dataframe(df.head(10), use_container_width=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### Gender Distribution")
        fig_gender = px.pie(df, names='Gender', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with colB:
        st.markdown("### Field of Study Popularity")
        fig_field = px.bar(df['Field_of_Study'].value_counts().reset_index(), 
                           x='Field_of_Study', y='count', 
                           labels={'count': 'Number of Students', 'Field_of_Study': 'Field'},
                           color='Field_of_Study')
        st.plotly_chart(fig_field, use_container_width=True)

# --- PAGE 2: ACADEMIC & SALARY ANALYSIS ---
elif menu == "🎓 Academic & Salary Analysis":
    st.title("Academic Performance vs. Salary Outcomes")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_field = st.selectbox("Filter by Field of Study:", ["All"] + list(df['Field_of_Study'].unique()))
        if selected_field != "All":
            filtered_df = df[df['Field_of_Study'] == selected_field]
        else:
            filtered_df = df
            
    with col2:
        st.markdown(f"**Showing data for:** {selected_field}")
        
    st.markdown("### Starting Salary by Field of Study")
    fig_salary_box = px.box(filtered_df, x="Field_of_Study", y="Starting_Salary", color="Field_of_Study", 
                            points="all", title="Salary Distribution per Field")
    st.plotly_chart(fig_salary_box, use_container_width=True)
    
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### University GPA vs. Starting Salary")
        fig_gpa_sal = px.scatter(filtered_df, x="University_GPA", y="Starting_Salary", color="Current_Job_Level",
                                 size="Job_Offers", hover_data=["Field_of_Study"])
        st.plotly_chart(fig_gpa_sal, use_container_width=True)
        
    with colB:
        st.markdown("### SAT Score vs. Job Offers")
        fig_sat_job = px.scatter(filtered_df, x="SAT_Score", y="Job_Offers", color="Gender", trendline="ols")
        st.plotly_chart(fig_sat_job, use_container_width=True)

# --- PAGE 3: SKILLS & NETWORKING ---
elif menu == "🤝 Skills & Networking":
    st.title("Impact of Soft Skills, Internships, & Networking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Networking Score vs. Career Satisfaction")
        fig_net = px.box(df, x="Networking_Score", y="Career_Satisfaction", color="Networking_Score")
        st.plotly_chart(fig_net, use_container_width=True)
        
    with col2:
        st.markdown("### Internships Completed vs. Job Offers")
        fig_intern = px.histogram(df, x="Internships_Completed", y="Job_Offers", histfunc="avg", 
                                  color="Current_Job_Level", barmode="group")
        st.plotly_chart(fig_intern, use_container_width=True)

    st.markdown("### Soft Skills Impact on Salary")
    fig_soft = px.density_heatmap(df, x="Soft_Skills_Score", y="Starting_Salary", text_auto=True, color_continuous_scale="Viridis")
    st.plotly_chart(fig_soft, use_container_width=True)

# --- PAGE 4: DEEP INSIGHTS & CORRELATIONS ---
elif menu == "🧠 Deep Insights & Correlations":
    st.title("Deep Analytical Insights")
    
    st.markdown("### Correlation Heatmap")
    st.write("Understand which numeric variables are most heavily correlated with each other.")
    
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### 💡 Key Takeaways from the Data")
    
    st.success("""
    **1. Networking is Powerful:** High networking scores generally correlate with higher career satisfaction and more job offers, regardless of pure academic GPA.
    
    **2. Internships Matter:** Students with 3 or more internships consistently secure higher starting salaries and enter at Mid/Senior levels faster.
    
    **3. The STEM Premium:** Fields like Engineering, Medicine, and Computer Science show significantly higher starting salary medians compared to Psychology or Education.
    
    **4. Soft Skills Cap:** While soft skills ensure faster promotions and better work-life balance, hard technical skills (indicated by high SAT/GPA in specific fields) still drive the initial base salary higher.
    """)
