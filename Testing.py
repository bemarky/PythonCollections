import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Data Explorer", layout="wide")

# Main title
st.title("📊 Interactive Data Explorer")

# Sidebar controls
with st.sidebar:
    st.header("Data Settings")

    # Data generation options
    data_size = st.slider("Data Size", 10, 1000, 100)
    noise_level = st.slider("Noise Level", 0.0, 2.0, 0.5)

    # Chart options
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line", "Bar", "Scatter", "Histogram"]
    )

    # Color options
    color_theme = st.selectbox(
        "Color Theme",
        ["Blues", "Reds", "Greens", "Viridis", "Plasma"]
    )

    # Generate data button
    generate_btn = st.button("Generate New Data")

# Initialize session state
if 'data' not in st.session_state or generate_btn:
    # Generate random data
    x = np.linspace(0, 10, data_size)
    y1 = np.sin(x) + np.random.normal(0, noise_level, data_size)
    y2 = np.cos(x) + np.random.normal(0, noise_level, data_size)
    y3 = np.sin(x) * np.cos(x) + np.random.normal(0, noise_level, data_size)

    st.session_state.data = pd.DataFrame({
        'x': x,
        'sin(x)': y1,
        'cos(x)': y2,
        'sin(x)cos(x)': y3
    })

# Display the data
st.subheader("Data Preview")
st.dataframe(st.session_state.data.head(10))

# Data statistics
st.subheader("Data Statistics")
col1, col2 = st.columns(2)
with col1:
    st.write("Summary Statistics")
    st.write(st.session_state.data.describe())
with col2:
    st.write("Data Information")
    buffer = st.session_state.data.info()
    st.text(f"Data Shape: {st.session_state.data.shape}")
    st.text(f"Missing Values: {st.session_state.data.isnull().sum().sum()}")

# Visualization
st.header("Data Visualization")

# Select columns to visualize
columns = st.session_state.data.columns.tolist()[1:]  # Exclude x column
selected_columns = st.multiselect(
    "Select columns to visualize",
    columns,
    default=columns[0]
)

if selected_columns:
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot based on selection
    if chart_type == "Line":
        for col in selected_columns:
            ax.plot(st.session_state.data['x'], st.session_state.data[col], label=col)
        ax.set_title("Line Chart")

    elif chart_type == "Bar":
        sample_size = min(30, len(st.session_state.data))  # Limit bar chart for better visibility
        bar_data = st.session_state.data.iloc[:sample_size]
        bar_width = 0.8 / len(selected_columns)

        for i, col in enumerate(selected_columns):
            x_pos = np.arange(sample_size) + i * bar_width
            ax.bar(x_pos, bar_data[col], width=bar_width, label=col)

        ax.set_title("Bar Chart (First 30 points)")
        ax.set_xticks(np.arange(sample_size))
        ax.set_xticklabels([f"{x:.1f}" for x in bar_data['x']], rotation=45)

    elif chart_type == "Scatter":
        for col in selected_columns:
            ax.scatter(st.session_state.data['x'], st.session_state.data[col], label=col, alpha=0.7)
        ax.set_title("Scatter Plot")

    elif chart_type == "Histogram":
        for col in selected_columns:
            ax.hist(st.session_state.data[col], bins=20, alpha=0.7, label=col)
        ax.set_title("Histogram")

    # Customize plot
    ax.set_xlabel("X")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    # Set color theme
    plt.style.use('default')
    if len(selected_columns) == 1:
        plt.set_cmap(color_theme)

    # Display the plot
    st.pyplot(fig)

    # Additional interactive plot with Streamlit
    st.subheader("Interactive Chart")

    # Different Streamlit chart based on selection
    if chart_type in ["Line", "Scatter"]:
        chart_data = st.session_state.data[selected_columns]
        st.line_chart(chart_data)
    elif chart_type == "Bar":
        chart_data = st.session_state.data.iloc[:30][selected_columns]  # Limit for visibility
        st.bar_chart(chart_data)
    else:
        st.write("Interactive histogram not available with Streamlit's built-in charts")

# Data download section
st.header("Download Data")
csv = st.session_state.data.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="streamlit_generated_data.csv",
    mime="text/csv"
)

# App information
with st.expander("About this app"):
    st.write("""
    This is a demo Streamlit application that shows how to:
    - Create interactive widgets
    - Generate and display data
    - Create visualizations
    - Use session state
    - Structure a Streamlit app with sidebar, columns, and expanders

    Feel free to explore the different options and see how the app responds to your inputs!
    """)