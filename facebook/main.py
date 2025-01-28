import streamlit as st
import subprocess

st.title("Social Media Analytics")
# Dropdown menu for selecting metric
metric = st.selectbox(
    "Select Metric",
    options=['Post', 'Followers', 'No of Likes', 'No of Comments'],
    index=0
)

# Dropdown menu for selecting chart type
chart = st.selectbox(
    "Select Chart Type",
    options=['pie', 'bar', 'column'],
    index=0
)

# Button to trigger fetch (run graphapi.py)
if st.button("Retrieve"):
    # Run the graphapi.py script
    subprocess.run(['python', 'graphapi.py'])
    st.success("Data retrieved successfully!")

# Initialize session state for analysis button
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

# Button to trigger analysis (clicked only once)
def analyze():
    st.session_state.analyze_clicked = True

# Render Analyze button
st.button("Analyze", on_click=analyze)

# Check if button has been clicked
if st.session_state.analyze_clicked:
    # Ensure both chart and metric are selected before rendering
    if chart and metric:
        from analysis import charts  # Import here to avoid running fetch on the first load
        highcharts_html = charts(chart, metric)
        st.title("Social Media Metrics Visualization")
        st.components.v1.html(highcharts_html, height=450)
