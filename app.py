import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

st.title("PSP Line Chart from Excel")

uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
if uploaded:
    @st.cache_data
    def load_excel(u):
        return pd.read_excel(BytesIO(u.getvalue()), engine="openpyxl")

    df = load_excel(uploaded)
    st.write(f"✅ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    st.dataframe(df.head())

    required = ["Stationing (m)", "ON PSP (VE V)", "OFF PSP (VE V)"]
    if all(col in df.columns for col in required):
        df_clean = df[required].copy()
        df_clean = df_clean.dropna(subset=["Stationing (m)"])
        df_clean = df_clean.fillna(0).astype({
            "Stationing (m)": float,
            "ON PSP (VE V)": float,
            "OFF PSP (VE V)": float
        })

        df_long = df_clean.melt(
            id_vars="Stationing (m)",
            value_vars=["ON PSP (VE V)", "OFF PSP (VE V)"],
            var_name="Type",
            value_name="Value"
        )

        chart = alt.Chart(df_long).mark_line(point=True).encode(
            x=alt.X("Stationing (m):Q", title="Stationing (m)"),
            y=alt.Y("Value:Q", title="PSP (VE V)"),
            color="Type:N"
        ).interactive()

        st.subheader("PSP vs Stationing")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.error(f"Excel must contain: {required}")
else:
    st.info("Please upload your Excel file (.xlsx)")
