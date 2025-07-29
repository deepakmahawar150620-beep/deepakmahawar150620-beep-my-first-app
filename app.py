import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📡 GitHub Excel Fresh Loader", layout="centered")
st.title("🔄 Always Fresh Load from GitHub Excel")

# Reload function with caching cleared every run
@st.cache_data(show_spinner=False)
def load_github_excel():
    url = "https://raw.githubusercontent.com/deepakmahawar150620-beep/SCC_Pawan/main/Pipeline_data.xlsx"
    df = pd.read_excel(url, engine="openpyxl", header=0)
    df.columns = df.columns.astype(str).str.strip()
    return df

# Force clear cache for this function to avoid stale content
load_github_excel.clear()

# Load fresh dataframe
df = load_github_excel()

st.write("✅ Column headers currently loaded:")
st.write(df.columns.tolist())

st.subheader("📋 Sample Data (First 5 rows):")
st.dataframe(df.head(5), use_container_width=True)

# Show LAT/LON if present
if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
    st.success("✅ GPS columns found.")
    st.write("Sample LATITUDE values:", df['LATITUDE'].head(5).tolist())
    st.write("Sample LONGITUDE values:", df['LONGITUDE'].head(5).tolist())
else:
    st.error("⚠️ GPS columns missing. Please confirm file structure.")
