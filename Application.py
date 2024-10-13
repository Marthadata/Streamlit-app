# Import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Health Insights Dashboard", page_icon=":mechanical_arm:", layout="wide") 

# Read in data
@st.cache_data
def get_data():
    df = pd.read_csv('health.csv', index_col=0)
    return df
df = get_data()  


# Sidebar for filtering data
st.sidebar.header("Health Parameters")

# Filters
age_group = st.sidebar.multiselect(
    "Select Age Group:",
    options=df['Age_group'].unique(),
    default=df['Age_group'].unique()
)

gender = st.sidebar.radio(
    "Select Gender:",
    options=df['Gender'].unique()
)

sleep_quality = st.sidebar.slider(
    "Sleep Quality (Rating):",
    min_value=1,
    max_value=10,
    value=(1, 10)
)

physical_activity = st.sidebar.slider(
    "Physical Activity Level:",
    min_value=0,
    max_value=2,
    value=(0, 2)
) 

dietary_habits = st.sidebar.multiselect(
    "Dietary Habits:",
    options=df['Dietary Habits'].unique(),
    default=df['Dietary Habits'].unique()
)

medication_usage = st.sidebar.multiselect(
    "Medication Usage:",
    options=df['Medication Usage'].unique(),
    default=df['Medication Usage'].unique()
)

# Apply filters to the dataset
df_select = df.query(
    "Age_group == @age_group & Gender == @gender & `Sleep Quality` >= @sleep_quality[0] & `Sleep Quality` <= @sleep_quality[1] & `Physical Activity Level` >= @physical_activity[0] & `Physical Activity Level` <= @physical_activity[1] & `Dietary Habits` in @dietary_habits & `Medication Usage` in @medication_usage"
)

# Check if dataframe is empty
if df_select.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()


# ---- Main Page ----
st.title("HealthTech Insights Dashboard")
st.markdown('##') 

# Calculate KPIs
average_sleep_quality = round(df_select['Sleep Quality'].mean(), 2)
sleep_duration = round(df_select['Sleep Duration'].mean(), 2)
average_steps = round(df_select['Daily Steps'].mean(), 2)
average_sleep_dis = round(df_select['Sleep Disorders'].mean(), 2)

first_column, second_column, third_column, fourth_column = st.columns(4)

with first_column:
    st.subheader("Sleep quality")
    st.subheader(f"{average_sleep_quality} / 10")

with second_column:
    st.subheader("Sleep duration")
    st.subheader(f"{sleep_duration} hours")

with third_column:
    st.subheader("Daily steps")
    st.subheader(f"{average_steps:,} steps")

with fourth_column:
    st.subheader("Sleep disorders")
    st.subheader(f"{average_sleep_dis:,}")

st.divider()


# Bar chart: Sleep Quality by Age Group
sleep_by_age = df_select.groupby(by="Age_group")[["Sleep Quality"]].mean().sort_values(by="Sleep Quality")

fig_sleep_age = px.bar(
    sleep_by_age,
    x = sleep_by_age.index,
    y="Sleep Quality",
    title="<b>Average Sleep Quality by Age Group</b>",
    color_discrete_sequence=["#0083B8"] * len(sleep_by_age),
    template="plotly_white",
)
fig_sleep_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# Scatter chart: Sleep Quality and Sleep Disorder
fig_sleep_quality_disorders = px.scatter(
    df_select,
    x="Sleep Quality",
    y="Sleep Disorders",  
    title="<b>Sleep Quality vs. Sleep Disorders</b>",  
    template="plotly_white",
)
fig_sleep_quality_disorders.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# Histogram: Sleep Quality Level Distribution
fig_sleep_quality_dist = px.histogram(
    df_select, 
    x="Sleep Quality", 
    title="Sleep Quality Distribution",
    nbins=5
) 
fig_sleep_quality_dist.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

left_column, middle_column, right_column  = st.columns(3)
left_column.plotly_chart(fig_sleep_age, use_container_width=True)
middle_column.plotly_chart(fig_sleep_quality_disorders, use_container_width=True)
right_column.plotly_chart(fig_sleep_quality_dist, use_container_width=True)

st.divider()


# Scatter chart: Calories Burned and Daily Steps
fig_calories_steps = px.scatter(
    df_select,
    x="Calories Burned",
    y="Daily Steps",  
    title="<b>Calories Burned vs. Daily Steps</b>",  
    template="plotly_white",
)

fig_sleep_quality_disorders.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# Bar chart: Physical Activity Level by Calories Burned
fig_activity_age = px.bar(
    df_select,
    x="Physical Activity Level",
    y= "Calories Burned",
    title="<b>Physical Activity Level by Calories Burned</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white", 
)

fig_activity_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# Bar chart: Physical Activity Level by Daily Steps
fig_activity_age1 = px.bar(
    df_select,
    x="Physical Activity Level",
    y= "Daily Steps",
    title="<b>Physical Activity Level by Daily Steps</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white", 
)

fig_activity_age1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

left_column, right_column, middle_column = st.columns(3)
left_column.plotly_chart(fig_calories_steps, use_container_width=True)
middle_column.plotly_chart(fig_activity_age, use_container_width=True)
right_column.plotly_chart(fig_activity_age1, use_container_width=True)

# Bar chart: Sleep Quality across Dietary Habits
fig_activity_age3 = px.bar(
    df_select,
    x="Dietary Habits",
    y= "Sleep Quality",
    title="<b>Sleep Quality across Dietary Habits</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white", 
)
fig_activity_age3.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# Bar chart: Sleep Quality across Medication Usage
fig_activity_age2 = px.bar(
    df_select,
    x= "Medication Usage",
    y= "Sleep Quality",
    title="<b>Sleep Quality across Medication Usage</b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white", 
)
fig_activity_age2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_activity_age3, use_container_width=True)
right_column.plotly_chart(fig_activity_age2, use_container_width=True)


