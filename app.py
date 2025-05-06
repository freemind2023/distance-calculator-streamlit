import streamlit as st
import pandas as pd
import time
from distance_utils import get_distance_km

BATCH_SIZE = 1000

st.set_page_config(page_title="Distance Calculator", layout="centered")

st.title("📍 Batch-wise Distance Calculator")

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx"])

if uploaded_file:
    if "df" not in st.session_state:
        df = pd.read_excel(uploaded_file)
        if "Distance A to B (km)" not in df.columns:
            df["Distance A to B (km)"] = ""
        st.session_state.df = df
        st.session_state.batch_index = 0
        st.success("✅ File loaded successfully.")

    df = st.session_state.df
    batch_index = st.session_state.batch_index
    start = batch_index * BATCH_SIZE
    end = min(start + BATCH_SIZE, len(df))

    if start >= len(df):
        st.success("🎉 All rows processed!")
    else:
        st.info(f"Processing batch {batch_index + 1}: Rows {start + 1} to {end}")

        if st.button("🚀 Process This Batch"):
            with st.spinner("Calculating distances..."):
                for i in range(start, end):
                    if df.at[i, "Distance A to B (km)"] in ["", None, "Error"]:
                        loc_a = f"{df.at[i, 'Location A']} School, Pune"
                        loc_b = f"{df.at[i, 'Location B']} College, Pune"
                        dist = get_distance_km(loc_a, loc_b)
                        df.at[i, "Distance A to B (km)"] = dist
                        time.sleep(1.2)

                st.session_state.df = df
                st.session_state.batch_index += 1
                st.success("✅ Batch completed.")

                partial_df = df.iloc[:end]
                st.download_button(
                    label="📥 Download Partial Results",
                    data=partial_df.to_excel(index=False),
                    file_name=f"distance_batch_{batch_index + 1}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        if batch_index > 0:
            st.download_button(
                label="📘 Download Full Processed File So Far",
                data=df.to_excel(index=False),
                file_name="distance_full_progress.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
