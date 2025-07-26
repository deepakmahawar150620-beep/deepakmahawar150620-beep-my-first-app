import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

st.title("PSP Line Chart from Excel (Stationing vs ON PSP/OFF PSP)")

uploaded = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
if uploaded:
    @st.cache_data
    def load_excel(u):
        buffer = BytesIO(u.getvalue())
        return pd.read_excel(buffer, engine="openpyxl")

    df = load_excel(uploaded)
    st.write(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    required = ["Stationing", "ON PSP", "OFF PSP"]
    if all(col in df.columns for col in required):
        df_clean = df[required].copy()
        # Drop rows where Stationing or both PSPs are null
        df_clean = df_clean.dropna(subset=["Stationing"]).fillna(0)
        df_clean = df_clean.astype({"Stationing": float, "ON PSP": float, "OFF PSP": float})

        df_melt = df_clean.melt(
            id_vars="Stationing",
            value_vars=["ON PSP", "OFF PSP"],
            var_name="Type",
            value_name="Value"
        )

        st.subheader("Line chart: PSP vs Stationing")
        chart = alt.Chart(df_melt).mark_line(point=True).encode(
            x=alt.X("Stationing:Q", title="Stationing (m)"),
            y=alt.Y("Value:Q", title="PSP (VE V)"),
            color="Type:N"
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.error(f"Excel must include these columns: {required}")
else:
    st.info("Please upload your Excel file (.xlsx)")
