import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel Upload (Fixes Axios 502)")

uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])

if uploaded:
    @st.cache_data
    def load_excel(u):
        return pd.read_excel(BytesIO(u.getvalue()), engine="openpyxl")

    try:
        df = load_excel(uploaded)
        st.write(f"✅ File loaded: {df.shape[0]} rows × {df.shape[1]} cols")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload your Excel file.")
