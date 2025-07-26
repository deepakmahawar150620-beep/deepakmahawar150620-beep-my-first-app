# app.py
import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

st.title("PSP Excel Uploader & Visualiser")

uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
if uploaded is not None:
    @st.cache_data(hash_funcs={st.runtime.uploaded_file_manager.UploadedFile: lambda x: x.file_id})
    def load_excel(uploaded_file):
        data = uploaded_file.getvalue()
        buffer = BytesIO(data)
        return pd.read_excel(buffer, engine="openpyxl")

    df = load_excel(uploaded)
    st.write(f"Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")

    # required columns
    required = ["Stationing", "ON PSP", "OFF PSP", "LATITUDE", "LONGITUDE"]
    if all(col in df.columns for col in required):
        # Line chart
        df_line = df[required[:-2]].rename(columns={"ON PSP":"ON_PSP","OFF PSP":"OFF_PSP"})
        df_melt = df_line.melt(id_vars="Stationing", var_name="type", value_name="value")
        line = alt.Chart(df_melt).mark_line(point=True).encode(
            x="Stationing:Q", y="value:Q", color="type:N"
        ).interactive()
        st.altair_chart(line, use_container_width=True)

        # Map plot
        df_map = df.rename(columns={"LATITUDE":"lat", "LONGITUDE":"lon"})
        st.map(df_map[["lat","lon"]].dropna())
    else:
        st.error(f"Missing one of these columns: {required}")
else:
    st.info("Please upload your Excel file (.xlsx)")
