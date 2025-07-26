import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Excel Upload Test")

uploaded = st.file_uploader("Upload XLSX", type="xlsx")

if uploaded:
    @st.cache_data
    def load_data(u):
        return pd.read_excel(BytesIO(u.getvalue()), engine="openpyxl")

    try:
        df = load_data(uploaded)
        st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Failed to load Excel: {e}")
else:
    st.info("Please upload your Excel file.")
