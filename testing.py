import streamlit as st
import pandas as pd
import numpy as np

# Title of the dashboard
st.title("Dashboard")

# Sidebar for interactivity
st.sidebar.header("Dashboard Controls")
time_period = st.sidebar.selectbox("Select Time Period", ["Daily", "Weekly", "Monthly"])
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=False)

# Sample data (replace with your own data source)
@st.cache_data
def load_sample_data():
    dates = pd.date_range(start="2025-01-01", end="2025-03-23", freq="D")
    data = pd.DataFrame({
        "Date": dates,
        "Sales": np.random.randint(100, 1000, len(dates)),
        "Users": np.random.randint(50, 500, len(dates))
    })
    return data

data = load_sample_data()

# Filter data based on time period (simplified example)
if time_period == "Weekly":
    data = data.resample("W", on="Date").sum().reset_index()
elif time_period == "Monthly":
    data = data.resample("M", on="Date").sum().reset_index()

# Key Metrics
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${data['Sales'].sum():,.2f}")
col2.metric("Total Users", f"{data['Users'].sum():,}")

# Chart
# st.subheader("Sales and Users Over Time")
# fig = sns.line(data, x="Date", y=["Sales", "Users"], title="Performance Trends")
# st.plotly_chart(fig)

# Optional raw data table
if show_raw_data:
    st.subheader("Raw Data")
    st.dataframe(data)

# Footer
st.write("Dashboard updated as of March 23, 2025.")
