import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind # For the t-test part

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Arts Faculty Comprehensive Visualization",
    layout="wide"
)

st.header("Arts Faculty Data Analysis and Visualization 📊", divider="blue")

# ######################################################################
# --- 1. DATA LOADING FROM URL ---
url = 'https://raw.githubusercontent.com/izzatimahrup/SV2025/refs/heads/main/arts_student_survey_output.csv'

try:
    # Load the CSV directly from the URL and assign it to arts_df
    arts_df = pd.read_csv(url)
    st.success("Data loaded successfully from GitHub URL!")
except Exception as e:
    st.error(f"An error occurred while reading the CSV from the URL: {e}")
    st.stop() # Stop the app if data loading fails
# ######################################################################


# --- Perform necessary data cleaning and calculation for all charts ---

# 1. GPA Calculations
gpa_cols = [col for col in arts_df.columns if "semester" in col.lower()]
arts_df[gpa_cols] = arts_df[gpa_cols].apply(pd.to_numeric, errors='coerce')
arts_df['Overall_Average_GPA'] = arts_df[gpa_cols].mean(axis=1, skipna=True)

# 2. Normalize SSC (5.0 scale) and HSC (5.0 scale) to 4.0 scale
arts_df['S.S.C (GPA)_norm'] = (pd.to_numeric(arts_df['S.S.C (GPA)'], errors='coerce') / 5.0) * 4.0
arts_df['H.S.C (GPA)_norm'] = (pd.to_numeric(arts_df['H.S.C (GPA)'], errors='coerce') / 5.0) * 4.0

# 3. Clean Coaching Center column
arts_df['Did you ever attend a Coaching center?'] = arts_df['Did you ever attend a Coaching center?'].astype(str).str.strip().str.title()

# 4. Corrected Academic Year column name
academic_year_col = 'Bachelor Academic Year in EU' # <-- CHANGED THIS LINE
# ----------------------------------------------------------------------

st.subheader("Gender Distribution")

# Calculate gender counts for the initial charts
gender_counts_df = arts_df['Gender'].value_counts().reset_index()
gender_counts_df.columns = ['Gender', 'Count']

st.write("Data summary (Gender Counts):")
st.dataframe(gender_counts_df, hide_index=True)

# ----------------------------------------------------------------------
## 1. Gender Bar Chart

st.subheader("Gender Distribution: Bar Chart")

fig_bar = px.bar(
    gender_counts_df,
    x='Gender',
    y='Count',
    title='Distribution of Gender in Arts Faculty (Bar Chart)',
    color='Gender',
    labels={'Count': 'Number of Students', 'Gender': 'Student Gender'},
    template='plotly_white'
)

fig_bar.update_layout(
    xaxis={'categoryorder':'total descending'},
    margin=dict(t=50, l=0, r=0, b=0)
)

st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------
## 2. Gender Pie Chart

st.subheader("Gender Distribution: Pie Chart")

fig_pie = px.pie(
    gender_counts_df,
    names='Gender',
    values='Count',
    title='Distribution of Gender in Arts Faculty (Pie Chart)',
    hole=0.4,
    color='Gender'
)

fig_pie.update_traces(
    textposition='inside',
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=1)),
)

fig_pie.update_layout(
    margin=dict(t=50, l=0, r=0, b=0)
)

st.plotly_chart(fig_pie, use_container_width=False)

st.markdown("---")
st.header("Advanced Program and Performance Analysis 🔬")

# ----------------------------------------------------------------------
# --- 3. Pie Chart: Arts Program Distribution ---
st.subheader("3. Percentage Distribution of Students by Arts Program")

arts_program_counts_df = arts_df['Arts Program'].value_counts().reset_index()
arts_program_counts_df.columns = ['Arts Program', 'Count']

fig3 = px.pie(
    arts_program_counts_df,
    names='Arts Program',
    values='Count',
    title='Percentage Distribution of Students by Arts Program',
    hole=0.3,
    color_discrete_sequence=px.colors.sequential.Agsunset
)
fig3.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------------------
# --- 4. Stacked Bar Chart: Arts Program Distribution by Gender ---
st.subheader("4. Arts Program Distribution by Gender (Stacked Bar)")

cross_tab_df = pd.crosstab(arts_df['Arts Program'], arts_df['Gender']).reset_index()
cross_tab_df = cross_tab_df.melt(
    id_vars='Arts Program',
    var_name='Gender',
    value_name='Count'
)

colors_map = {'Male': '#4A90E2', 'Female': '#FF69B4', 'Non-Binary': '#F7DC6F', 'Other': '#95a5a6'} 

fig4 = px.bar(
    cross_tab_df,
    x='Arts Program',
    y='Count',
    color='Gender',
    title='Arts Program Distribution by Gender',
    color_discrete_map=colors_map
)

fig4.update_layout(
    xaxis_title='Arts Program',
    yaxis_title='Number of Students',
    barmode='stack',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------------------------------------
# --- 5. Line Chart: Normalized GPA Comparison ---
st.subheader("5. Normalized GPA Comparison: S.S.C → H.S.C → University")

# Melt the data into long format
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

# Create figure using go.Figure for layering
fig5 = go.Figure()

# Individual Student Trends (Light gray lines)
for i, row in arts_df.iterrows():
    gpas = [row['S.S.C (GPA)_norm'], row['H.S.C (GPA)_norm'], row['Overall_Average_GPA']]
    fig5.add_trace(go.Scatter(
        x=list(level_map.values()),
        y=gpas,
        mode='lines',
        line=dict(color='gray', width=1),
        opacity=0.15,
        showlegend=False
    ))

# Average GPA Line + Points (Blue line)
fig5.add_trace(go.Scatter(
    x=avg_gpa_df['Level'],
    y=avg_gpa_df['GPA'],
    mode='lines+markers+text',
    line=dict(color='royalblue', width=2.5),
    marker=dict(size=10),
    text=[f"{gpa:.2f}" for gpa in avg_gpa_df['GPA']],
    textposition="bottom center",
    name='Average GPA'
))

fig5.update_layout(
    title='Normalized GPA Comparison: S.S.C → H.S.C → University (4.0 Scale)',
    xaxis_title='Education Level',
    yaxis_title='Normalized GPA (4.0 Scale)',
    yaxis_range=[0, 4.1]
)
fig5.update_yaxes(tickvals=[0, 1, 2, 3, 4])

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------------------------------------------------
# --- 6. Bar Chart: Average Overall GPA by Coaching Attendance ---
st.subheader("6. Average Overall GPA: Coaching Center vs Non-Coaching Students")

avg_gpa_overall = arts_df.groupby('Did you ever attend a Coaching center?')['Overall_Average_GPA'].mean().reset_index()
order = ['Yes', 'No']

palette_colors = {'Yes': '#2ecc71', 'No': '#e74c3c'}

fig6 = px.bar(
    avg_gpa_overall,
    x='Did you ever attend a Coaching center?',
    y='Overall_Average_GPA',
    title='Average Overall GPA: Coaching Center vs Non-Coaching Students',
    category_orders={'Did you ever attend a Coaching center?': order},
    color='Did you ever attend a Coaching center?',
    color_discrete_map=palette_colors
)

fig6.update_traces(texttemplate='%{y:.2f}', textposition='outside')
fig6.update_layout(
    xaxis_title='Attended Coaching Center',
    yaxis_title='Average Overall GPA',
    yaxis_range=[0, 4]
)

st.plotly_chart(fig6, use_container_width=True)

# --- Statistical Test Output ---
st.caption("Statistical Analysis (T-test)")
yes_group = arts_df[arts_df['Did you ever attend a Coaching center?'] == 'Yes']['Overall_Average_GPA'].dropna()
no_group = arts_df[arts_df['Did you ever attend a Coaching center?'] == 'No']['Overall_Average_GPA'].dropna()

# Check if both groups have enough samples
if len(yes_group) > 1 and len(no_group) > 1:
    t_stat, p_value = ttest_ind(yes_group, no_group, equal_var=False)
    
    st.write(f"Average GPA (Coaching Yes): {yes_group.mean():.3f}")
    st.write(f"Average GPA (Coaching No): {no_group.mean():.3f}")
    st.write(f"T-statistic = {t_stat:.3f}")
    st.write(f"P-value = {p_value:.4f}")

    if p_value < 0.05:
        st.success("✅ The difference between groups is statistically significant (p < 0.05).")
    else:
        st.info("⚖️ No statistically significant difference between coaching and non-coaching students.")
else:
    st.warning("Insufficient data points in one or both coaching groups to perform a reliable T-test.")


# --- 5. Bar Chart: Distribution of Academic Years ---
st.subheader("5. Distribution of Academic Years (Student Count)")

# Identify column (using placeholder name)
academic_year_col = 'Bachelor Academic Year in EU'

# Prepare data
academic_year_counts_df = arts_df[academic_year_col].value_counts().reset_index()
academic_year_counts_df.columns = ['Academic Year', 'Count']
year_order = ['1st Year', '2nd Year', '3rd Year', '4th Year']

fig5 = px.bar(
    academic_year_counts_df,
    x='Academic Year',
    y='Count',
    title='Distribution of Academic Years for Bachelor Students in Arts Faculty',
    category_orders={'Academic Year': year_order},
    color='Academic Year', # Assign colors by year
    color_discrete_sequence=px.colors.qualitative.Pastel # Pastel palette
)

fig5.update_traces(texttemplate='%{y}', textposition='outside') # Add value labels
fig5.update_layout(
    xaxis_title='Academic Year',
    yaxis_title='Number of Students'
)

st.plotly_chart(fig5, use_container_width=True)
