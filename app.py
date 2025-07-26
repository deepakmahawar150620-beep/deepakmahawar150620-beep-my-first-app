import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🛠️ SCC Data Analysis Tool")

# File uploader
uploaded_file = st.file_uploader("📤 Upload your SCC data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Try to read the file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.success("✅ File uploaded and loaded successfully!")

    # Show preview
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    # Columns to choose
    st.subheader("🧪 Select columns for analysis")
    numeric_columns = df.select_dtypes(include=["float", "int"]).columns.tolist()
    column_x = st.selectbox("X-axis (e.g., Location)", numeric_columns)
    column_y = st.selectbox("Y-axis (e.g., Depth)", numeric_columns)

    # Optional grouping (e.g., by Pipeline ID)
    group_col = st.selectbox("Group by (optional, e.g., pipeline ID)", ["None"] + df.columns.tolist())

    st.subheader("📊 Chart")

    if group_col != "None":
        for group, data in df.groupby(group_col):
            st.line_chart(data[[column_x, column_y]].set_index(column_x), height=300, use_container_width=True)
            st.markdown(f"**Group: {group}**")
    else:
        st.line_chart(df[[column_x, column_y]].set_index(column_x), height=400)

    st.caption("Note: This is a basic visual preview. For Paris Law or crack growth prediction, we can add more logic later.")
