import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Arts Faculty Gender Visualization",
    layout="wide"
)

st.header("Arts Faculty Gender Distribution Analysis 📊", divider="blue")

# --- 1. Data Preparation (Replace with your actual data loading) ---

# Example data for demonstration purposes
data = {
    'Gender': ['Female', 'Male', 'Female', 'Non-Binary', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male']
}
arts_df = pd.DataFrame(data)

# Calculate the counts and reset the index to create a Plotly-friendly DataFrame
gender_counts_df = arts_df['Gender'].value_counts().reset_index()
gender_counts_df.columns = ['Gender', 'Count']

st.write("Data summary (Counts):")
st.dataframe(gender_counts_df, hide_index=True)

# ----------------------------------------------------------------------
## Bar Chart (Matplotlib/Seaborn converted to Plotly Express)

st.subheader("Gender Distribution: Bar Chart")

# Create the Plotly Bar Chart
fig_bar = px.bar(
    gender_counts_df,
    x='Gender',
    y='Count',
    title='Distribution of Gender in Arts Faculty (Bar Chart)',
    color='Gender', # Color bars by gender
    labels={'Count': 'Number of Students', 'Gender': 'Student Gender'},
    template='plotly_white'
)

# Customize the layout
fig_bar.update_layout(
    xaxis={'categoryorder':'total descending'}, # Order bars by count
    margin=dict(t=50, l=0, r=0, b=0) # Adjust margins
)

# Display the chart in Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------------------------
## Pie Chart (Matplotlib converted to Plotly Express)

st.subheader("Gender Distribution: Pie Chart")

# Create the Plotly Pie Chart
fig_pie = px.pie(
    gender_counts_df,
    names='Gender',
    values='Count',
    title='Distribution of Gender in Arts Faculty (Pie Chart)',
    hole=0.4, # Creates a donut chart (optional)
    color='Gender'
)

# Customize the traces for better text display
fig_pie.update_traces(
    textposition='inside',
    textinfo='percent+label', # Shows percentage and label (gender)
    marker=dict(line=dict(color='#000000', width=1)),
)

# Update layout for a better circular appearance
fig_pie.update_layout(
    margin=dict(t=50, l=0, r=0, b=0)
)

# Display the chart in Streamlit
# Note: use_container_width=False is often better for preserving the circular shape
st.plotly_chart(fig_pie, use_container_width=False)
