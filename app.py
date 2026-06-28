# Import the libraries
import streamlit as st
import pandas as pd
import plotly.express as px
# Page configuration
st.set_page_config(
    page_title="Mental Health Analytics",
    page_icon="🧠",
    layout="wide"
)
# Colors
colors = [
    "#00C896",
    "#3B82F6",
    "#8B5CF6",
    "#F59E0B",
    "#EF4444"
]
# Load the data
@st.cache_data
def load_data():
    # Read the data file
    df = pd.read_csv(
        "cleaned_mental_health_tech.csv"
    )
    # Convert age to numeric values
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )
    # Convert treatment values to "Yes" and "No"
    df["treated"] = (
        df["treatment"]
        .astype(str)
        .map({
            "1":"Yes",
            "0":"No"
        })
    )
    # Standardize company size labels
    df["company_size"] = df["company_size"].replace(
        {
            "5-Jan":"1-5",
            "25-Jun":"6-25"
        }
    )
    return df
df = load_data() # Load the dataset

# # Sidebar filters
st.sidebar.title("🔎 Data Filters")
# Select countries
country = st.sidebar.multiselect(
    "Country",
    df.country.dropna().unique(),
    default=df.country.dropna().unique()[:5]
)
# Select gender
gender = st.sidebar.multiselect(
    "Gender",
    df.gender.dropna().unique(),
    default=df.gender.dropna().unique()
)
# Select age range
age = st.sidebar.slider(
    "Age",
    18,
    70,
    (20,55)
)
# Select company size
company = st.sidebar.multiselect(
    "Company Size",
    df.company_size.dropna().unique(),
    default=df.company_size.dropna().unique()
)
# Select remote work status
remote = st.sidebar.multiselect(
    "Remote Work",
    df.work_remotely.dropna().unique(),
    default=df.work_remotely.dropna().unique()
)
# # Apply filters to the dataset
data = df[
    (df.country.isin(country)) &
    (df.gender.isin(gender)) &
    (df.company_size.isin(company)) &
    (df.work_remotely.isin(remote))
]
# Filter data by age
data = data[
    (data.age>=age[0]) &
    (data.age<=age[1])
]
# Dashboard title
st.title(
    "🧠 Mental Health in Tech Analytics"
)
st.write(
    "Interactive analysis dashboard for workplace mental health insights"
)
# Display the original dataset
if st.button("📄 Show Original Data"):

    st.dataframe(
        df,
        use_container_width=True
    )
# Key Performance Indicators (KPIs)
a,b,c,d = st.columns(4)
# Total respondents
a.metric(
    "Respondents",
    len(data)
)
# Total respondents
b.metric(
    "Treatment Rate",
    f"{data.treated.eq('Yes').mean()*100:.1f}%"
)
# Benefits availability rate
c.metric(
    "Benefits",
    f"{data.benefits.eq('Yes').mean()*100:.1f}%"
)
# Remote workers rate
d.metric(
    "Remote Workers",
    f"{(data.work_remotely!='Never').mean()*100:.1f}%"
)
st.divider() # Section divider

# ================================================================
# This section provides an overview of mental health treatment
# ================================================================
# Section title
st.subheader(
    "Mental Health Treatment Overview"
)
# Count respondents who received treatment and those who didn't
t = data.treated.value_counts().reset_index()
# Rename columns for better visualization
t.columns=[
    "Status",
    "Count"
]
# Create a donut chart to display the treatment distribution
fig1 = px.pie(
    t,
    names="Status",  # Category labels
    values="Count",  # Number of respondents in each category
    hole=.55,   # Set the chart as a donut
    color="Status",   # Assign colors by category
    color_discrete_sequence=colors[:2],  # Apply the custom color palette
    title="Treatment Status"  # Chart title
)
# Apply the dark theme
fig1.update_layout(
    template="plotly_dark"
)
# Display the chart in Streamlit
st.plotly_chart(
    fig1,
    use_container_width=True
)
# Key insight below the chart
st.info(
    "📌 Insight: The treatment rate helps organizations assess the need for mental health support and employee assistance programs."
)
# =====================================================
# Workplace support analysis section
# =====================================================
# Section title
st.subheader(
    "Workplace Support Analysis"
)
# Create a table of workplace support programs and their availability
support = pd.DataFrame({
"Support":
[
"Benefits",
"Wellness Program",
"Care Options"
],
"Percentage":
[
data.benefits.eq("Yes").mean()*100, # Calculate the percentage of employees with benefits
data.wellness_program.eq("Yes").mean()*100,  # Calculate the percentage of employees with wellness programs
data.care_options.eq("Yes").mean()*100   # Calculate the percentage of employees with wellness programs
]
})
# Create a bar chart to compare workplace support programs
fig2 = px.bar(
    support,
    x="Support",   # Support program names
    y="Percentage", # Percentage for each support program
    text_auto=".1f",   # Display values on top of each bar
    color="Support",     # Assign a different color to each bar
    color_discrete_sequence=colors,  # Apply the custom color palette
    title="Company Support Availability (%)" # Chart title
)
# Apply the dark theme
fig2.update_layout(
    template="plotly_dark"
)
# Display the chart in Streamlit
st.plotly_chart(
    fig2,
    use_container_width=True
)
# Key insight below the chart
st.success(
    "📌 Insight: Providing workplace support programs can encourage employees to seek help and reduce barriers to accessing mental health care"
)
# ===========================================================================
# Treatment rate analysis by company size
# ===========================================================================
# Section title
st.subheader(
"Treatment Rate by Company Size"
)
# Group data by company size and calculate the treatment rate
company_df = (
data.groupby("company_size")
.treated
.apply(
lambda x:x.eq("Yes").mean()*100
)
.reset_index()
)
# Rename columns for better visualization
company_df.columns=[
"Company Size",
"Rate"
]
# Create a bar chart showing treatment rates by company size
fig3 = px.bar(
company_df,
x="Company Size",  # Company size
y="Rate",    # Treatment rate
text_auto=".1f",  # Display values on top of each bar
color="Rate",  # Color bars based on the treatment rate
color_continuous_scale=[
"#1E293B",
"#00C896"
],
title="Treatment Rate (%)"   # Chart title
)
# Apply the dark theme
fig3.update_layout(
template="plotly_dark"
)
# Display the chart in Streamlit
st.plotly_chart(
fig3,
use_container_width=True
)
# Display the final insight below the chart
st.warning(
        "📌 Insight: Company size may influence access to mental health services, highlighting the importance of providing adequate support across organizations of all sizes."
)
# =====================================================
# Age distribution and treatment analysis
# =====================================================
# Section title
st.subheader(
"Age Distribution and Treatment"
)
# Create a histogram showing age distribution by treatment status
fig4 = px.histogram(
data,
x="age", # Age
color="treated",  # Group data by treatment status
nbins=25,  # Number of bins
barmode="overlay",  # Overlay bars for comparison
color_discrete_sequence=[
"#00C896", # Color for respondents who did not receive treatment
"#EF4444" # Color for respondents who received treatment
],
# Chart title
title="Age Groups"
)
# Apply the dark theme
fig4.update_layout(
template="plotly_dark"
)
# Display the chart in Streamlit
st.plotly_chart(
fig4,
use_container_width=True
)
# Key insight below the chart
st.info(
    "📌 Insight: Understanding which age groups seek treatment most often can help organizations design targeted mental health initiatives."
)
# =====================================================
# 5
# =====================================================
# Section title
st.subheader(
"Remote Work and Company Size Impact"
)
# Group data by remote work status and company size
heat = (
data.groupby(
[
"work_remotely", # Remote work status
"company_size"  # Company size
]
)
# Calculate the treatment rate
.treated
.apply(
lambda x:x.eq("Yes").mean()*100
)
.reset_index()  # Convert the results into a DataFrame
)
# Rename columns for better visualization
heat.columns=[
"Remote",
"Company Size",
"Rate"
]
# Reshape the data into a pivot table for the heatmap
pivot = heat.pivot(
index="Remote",
columns="Company Size",
values="Rate"
)
# Create the heatmap
fig5 = px.imshow(
pivot,
# Display the value inside each cell
text_auto=".1f",
# Apply the custom color scale
color_continuous_scale=[
"#111827",
"#3B82F6",
"#00C896"
],
# Chart title
title="Treatment Rate Heatmap (%)"
)
# Apply the dark theme
fig5.update_layout(
template="plotly_dark"
)
# Display the chart in Streamlit
st.plotly_chart(
fig5,
use_container_width=True
)
# Key insight below the chart
st.success(
    "📌 Insight: Work environment and company size may influence treatment-seeking behavior, emphasizing the need for flexible mental health support across different work settings."
)