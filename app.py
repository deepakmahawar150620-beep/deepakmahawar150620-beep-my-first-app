# app.py
import streamlit as st
import pandas as pd
import altair as alt

st.title("PSP Data Viewer")

uploaded = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)

    # Ensure expected columns exist
    expected = ["Stationing", "ON PSP", "OFF PSP", "LATITUDE", "LONGITUDE"]
    if all(col in df.columns for col in expected):
        st.subheader("Line plot: ON PSP and OFF PSP vs Stationing")
        df_line = df[["Stationing", "ON PSP", "OFF PSP"]].rename(columns={
            "ON PSP": "ON_PSP", "OFF PSP": "OFF_PSP"
        })
        df_melt = df_line.melt(id_vars="Stationing", var_name="type", value_name="value")
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x="Stationing:Q",
            y="value:Q",
            color="type:N"
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Map: Locations (latitude & longitude)")
        df_map = df.rename(columns={"LATITUDE":"lat", "LONGITUDE":"lon"})
        st.map(df_map[["lat", "lon"]].dropna(), zoom=10)
    else:
        st.error(f"CSV must include these columns: {expected}")
else:
    st.info("Please upload your CSV file")
