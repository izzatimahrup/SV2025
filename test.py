import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Arts Faculty Comprehensive Visualization",
    layout="wide"
)

st.title("Arts Faculty Data Analysis and Visualization 📊")

# ######################################################################
# --- 1. DATA LOADING AND INITIAL PREPARATION (REPLACED WITH YOUR URL CODE) ---

url = 'https://raw.githubusercontent.com/izzatimahrup/SV2025/refs/heads/main/arts_student_survey_output.csv'

try:
    # Load the CSV directly from the URL and assign it to arts_df
    arts_df = pd.read_csv(url)
    st.success("Data loaded successfully from GitHub URL!")
except Exception as e:
    st.error(f"An error occurred while reading the CSV from the URL: {e}")
    st.stop() # Stop the app if data loading fails

# ######################################################################


# --- Data Cleaning and Calculation (Keep this section) ---
# This section prepares the data structure required by the charts
gpa_cols = [col for col in arts_df.columns if "semester" in col.lower()]
arts_df[gpa_cols] = arts_df[gpa_cols].apply(pd.to_numeric, errors='coerce')
arts_df['Overall_Average_GPA'] = arts_df[gpa_cols].mean(axis=1, skipna=True)
arts_df['S.S.C (GPA)_norm'] = (pd.to_numeric(arts_df['S.S.C (GPA)'], errors='coerce') / 5.0) * 4.0
arts_df['H.S.C (GPA)_norm'] = (pd.to_numeric(arts_df['H.S.C (GPA)'], errors='coerce') / 5.0) * 4.0
arts_df['Did you ever attend a Coaching center?'] = arts_df['Did you ever attend a Coaching center?'].astype(str).str.strip().str.title()
# ----------------------------------------------------------------------


st.header("1. Gender Distribution", divider="blue")

# Calculate gender counts for the initial charts
gender_counts_df = arts_df['Gender'].value_counts().reset_index()
gender_counts_df.columns = ['Gender', 'Count']
st.dataframe(gender_counts_df, hide_index=True)

col1, col2 = st.columns(2)

with col1:
    # --- 1A. Bar Chart: Gender Distribution (Custom Colors) ---
    st.subheader("Gender Distribution: Bar Chart")
    custom_colors = {
        'Male': '#3498db',    # Blue
        'Female': '#ff69b4',   # Pink
        'Non-Binary': '#95a5a6', # Fallback/Other gender color
    }
    
    fig1a = px.bar(
        gender_counts_df,
        x='Gender',
        y='Count',
        title='<b>Distribution of Gender in Arts Faculty</b>',
        color='Gender',
        color_discrete_map=custom_colors,
        template='plotly_white'
    )
    
    fig1a.update_traces(
        texttemplate='%{y}',
        textposition='outside',
        marker_line_color='black',
        marker_line_width=1.5
    )
    
    fig1a.update_layout(
        xaxis={'categoryorder': 'total descending'},
        xaxis_title='Gender',
        yaxis_title='Count',
        yaxis_range=[0, gender_counts_df['Count'].max() * 1.2], 
    )
    st.plotly_chart(fig1a, use_container_width=True)

with col2:
    # --- 1B. Pie Chart: Gender Distribution ---
    st.subheader("Gender Distribution: Pie Chart")
    
    fig1b = px.pie(
        gender_counts_df,
        names='Gender',
        values='Count',
        title='Distribution of Gender in Arts Faculty (Pie Chart)',
        hole=0.4,
        color='Gender'
    )
    
    fig1b.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1)),
    )
    
    fig1b.update_layout(margin=dict(t=50, l=0, r=0, b=0))
    st.plotly_chart(fig1b, use_container_width=True)


st.header("2. Program and Academic Year Distribution", divider="blue")

col3, col4 = st.columns(2)

with col3:
    # --- 2A. Pie Chart: Arts Program Distribution ---
    st.subheader("Percentage Distribution by Arts Program")
    arts_program_counts_df = arts_df['Arts Program'].value_counts().reset_index()
    arts_program_counts_df.columns = ['Arts Program', 'Count']

    fig2a = px.pie(
        arts_program_counts_df,
        names='Arts Program',
        values='Count',
        title='Percentage Distribution of Students by Arts Program',
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig2a.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2a, use_container_width=True)
    
with col4:
    # --- 2B. Bar Chart: Distribution of Academic Years ---
    st.subheader("Distribution of Academic Years")
    academic_year_col = 'Academic Year in EU'
    academic_year_counts_df = arts_df[academic_year_col].value_counts().reset_index()
    academic_year_counts_df.columns = ['Academic Year', 'Count']
    year_order = ['1st Year', '2nd Year', '3rd Year', '4th Year']

    fig2b = px.bar(
        academic_year_counts_df,
        x='Academic Year',
        y='Count',
        title='Distribution of Academic Years for Bachelor Students',
        category_orders={'Academic Year': year_order},
        color='Academic Year',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig2b.update_traces(texttemplate='%{y}', textposition='outside')
    fig2b.update_layout(xaxis_title='Academic Year', yaxis_title='Number of Students')
    st.plotly_chart(fig2b, use_container_width=True)


# --- 2C. Stacked Bar Chart: Arts Program Distribution by Gender ---
st.subheader("2C. Arts Program Distribution by Gender (Stacked Bar)")

cross_tab_df = pd.crosstab(arts_df['Arts Program'], arts_df['Gender']).reset_index()
cross_tab_df = cross_tab_df.melt(
    id_vars='Arts Program',
    var_name='Gender',
    value_name='Count'
)

colors_map_stacked = {'Male': '#4A90E2', 'Female': '#FF69B4', 'Non-Binary': '#F7DC6F'} 

fig2c = px.bar(
    cross_tab_df,
    x='Arts Program',
    y='Count',
    color='Gender',
    title='Arts Program Distribution by Gender',
    color_discrete_map=colors_map_stacked
)

fig2c.update_layout(
    xaxis_title='Arts Program',
    yaxis_title='Number of Students',
    barmode='stack',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig2c, use_container_width=True)


st.header("3. GPA Performance Analysis", divider="blue")

# --- 3A. Line Chart: Normalized GPA Comparison ---
st.subheader("3A. Normalized GPA Comparison: S.S.C → H.S.C → University")

gpa_long = arts_df.melt(
    value_vars=['S.S.C (GPA)_norm', 'H.S.C (GPA)_norm', 'Overall_Average_GPA'],
    var_name='Level',
    value_name='GPA'
)

level_map = {
    'S.S.C (GPA)_norm': 'S.S.C (GPA)',
    'H.S.C (GPA)_norm': 'H.S.C (GPA)',
    'Overall_Average_GPA': 'University (Avg GPA)'
}
gpa_long['Level'] = gpa_long['Level'].replace(level_map)
gpa_long['Level'] = pd.Categorical(
    gpa_long['Level'], categories=level_map.values(), ordered=True
)
avg_gpa_df = gpa_long.groupby('Level', observed=True)['GPA'].mean().reset_index()

fig3a = go.Figure()

# Individual Student Trends (Light gray lines)
for i, row in arts_df.iterrows():
    gpas = [row['S.S.C (GPA)_norm'], row['H.S.C (GPA)_norm'], row['Overall_Average_GPA']]
    fig3a.add_trace(go.Scatter(
        x=list(level_map.values()),
        y=gpas,
        mode='lines',
        line=dict(color='gray', width=1),
        opacity=0.15,
        showlegend=False
    ))

# Average GPA Line + Points (Blue line)
fig3a.add_trace(go.Scatter(
    x=avg_gpa_df['Level'],
    y=avg_gpa_df['GPA'],
    mode='lines+markers+text',
    line=dict(color='royalblue', width=2.5),
    marker=dict(size=10),
    text=[f"{gpa:.2f}" for gpa in avg_gpa_df['GPA']],
    textposition="bottom center",
    name='Average GPA'
))

fig3a.update_layout(
    title='Normalized GPA Comparison: S.S.C → H.S.C → University (4.0 Scale)',
    xaxis_title='Education Level',
    yaxis_title='Normalized GPA (4.0 Scale)',
    yaxis_range=[0, 4.1]
)
fig3a.update_yaxes(tickvals=[0, 1, 2, 3, 4])
st.plotly_chart(fig3a, use_container_width=True)

# --- 3B. Bar Chart: Average Overall GPA by Coaching Attendance ---
st.subheader("3B. Average Overall GPA: Coaching Center vs Non-Coaching Students")

avg_gpa_overall = arts_df.groupby('Did you ever attend a Coaching center?')['Overall_Average_GPA'].mean().reset_index()
order = ['Yes', 'No']
palette_colors = {'Yes': '#2ecc71', 'No': '#e74c3c'}

fig3b = px.bar(
    avg_gpa_overall,
    x='Did you ever attend a Coaching center?',
    y='Overall_Average_GPA',
    title='Average Overall GPA: Coaching Center vs Non-Coaching Students',
    category_orders={'Did you ever attend a Coaching center?': order},
    color='Did you ever attend a Coaching center?',
    color_discrete_map=palette_colors
)

fig3b.update_traces(texttemplate='%{y:.2f}', textposition='outside')
fig3b.update_layout(
    xaxis_title='Attended Coaching Center',
    yaxis_title='Average Overall GPA',
    yaxis_range=[0, 4]
)

st.plotly_chart(fig3b, use_container_width=True)

# --- Statistical Test Output ---
st.caption("Statistical Analysis (T-test)")
yes_group = arts_df[arts_df['Did you ever attend a Coaching center?'] == 'Yes']['Overall_Average_GPA'].dropna()
no_group = arts_df[arts_df['Did you ever attend a Coaching center?'] == 'No']['Overall_Average_GPA'].dropna()

if len(yes_group) > 1 and len(no_group) > 1:
    t_stat, p_value = ttest_ind(yes_group, no_group, equal_var=False)
    
    st.text(f"Average GPA (Coaching Yes): {yes_group.mean():.3f}")
    st.text(f"Average GPA (Coaching No): {no_group.mean():.3f}")
    st.text(f"T-statistic = {t_stat:.3f}")
    st.text(f"P-value = {p_value:.4f}")

    if p_value < 0.05:
        st.success("✅ The difference between groups is statistically significant (p < 0.05).")
    else:
        st.info("⚖️ No statistically significant difference between coaching and non-coaching students
