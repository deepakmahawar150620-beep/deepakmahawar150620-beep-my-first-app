import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Complete Pipeline Data Viewer", layout="centered")
st.title("📁 Full Pipeline Excel Data (with GPS)")

@st.cache_data(show_spinner=False)
def load_full_data():
    url = "https://raw.githubusercontent.com/deepakmahawar150620-beep/SCC_Pawan/main/Pipeline_data.xlsx"
    df = pd.read_excel(url, engine="openpyxl", header=0)
    df.columns = df.columns.astype(str).str.strip()  # ensure clean headers
    return df

df = load_full_data()

st.write("✅ Detected Columns in Sheet:")
st.write(df.columns.tolist())

st.subheader("📋 First 10 Rows Preview")
st.dataframe(df.head(10), use_container_width=True)

if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
    st.success("✅ GPS columns found!")
    st.write("Some LATITUDE values:", df['LATITUDE'].dropna().head(5).tolist())
    st.write("Some LONGITUDE values:", df['LONGITUDE'].dropna().head(5).tolist())
else:
    st.error("⚠️ LATITUDE or LONGITUDE column missing!")
