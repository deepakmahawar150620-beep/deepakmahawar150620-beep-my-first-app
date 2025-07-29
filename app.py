import streamlit as st
import pandas as pd

st.set_page_config(page_title="✅ GitHub Excel GPS Loader", layout="centered")
st.title("🧪 Load & Preview Excel from GitHub (with GPS columns)")

@st.cache_data(show_spinner=False)
def load_github_sheet():
    url = "https://raw.githubusercontent.com/deepakmahawar150620-beep/SCC_Pawan/main/Pipeline_data.xlsx"
    # Read all columns without restriction (no usecols)
    df = pd.read_excel(url, engine="openpyxl", header=0)
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_github_sheet()

st.write("✅ Columns detected in Excel:")
st.write(df.columns.tolist())

st.write("📋 Preview first 5 rows (including GPS columns):")
st.dataframe(df.head(5), use_container_width=True)

if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
    st.success("✅ Found LATITUDE and LONGITUDE columns.")
else:
    st.error("⚠️ LATITUDE or LONGITUDE column missing!")

if 'LATITUDE' in df.columns:
    st.write("First few LATITUDE values:")
    st.write(df['LATITUDE'].head(5).tolist())
if 'LONGITUDE' in df.columns:
    st.write("First few LONGITUDE values:")
    st.write(df['LONGITUDE'].head(5).tolist())
