import time  # For demo delays

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages


# Cache data loading
@st.cache_data
def load_data(file):
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    required_cols = ["date", "outcome", "pl_by_percentage", "risk_by_percentage", "entry_time", "pl_by_rr"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError("Missing required columns, Please make sure the required templet is used.")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["DoW"] = df["date"].dt.day_name().str.lower()
    return df


# Cache stats calculation
@st.cache_data
def calculate_stats(df):
    wins = df["outcome"].value_counts().get("WIN", 0)
    losses = df["outcome"].value_counts().get("LOSS", 0)
    winrate = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0.0
    pl_raw = (
        df["pl_by_percentage"].str.replace("%", "").astype(float)
        if df["pl_by_percentage"].dtype == "object"
        else df["pl_by_percentage"] * 100
    )
    pl = pl_raw.cumsum()
    total_pl = pl_raw.sum()
    return pl, pl_raw, {"Win Rate": f"{winrate:.2f}%", "Total P/L": f"{total_pl:.2f}%"}


# Main app
st.title("Trading Journal Analyser")

uploaded_file = st.file_uploader("Upload your trades data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Spinner for loading
    with st.spinner("Loading your trades..."):
        try:
            df = load_data(uploaded_file)
        except ValueError as e:
            st.error(str(e))  # Display only the error message
            st.stop()  # Stop further execution

    # Progress bar for analysis
    st.write("Analyzing trades...")
    progress_bar = st.progress(0)
    with st.spinner("Calculating stats..."):
        pl, pl_raw, stats = calculate_stats(df)
        progress_bar.progress(43)  # 1/3 done

    # Plotting with progress updates
    with st.spinner("Generating plots..."):
        fig, ax = plt.subplots()
        sns.lineplot(x=range(len(df)), y=pl, ax=ax)
        st.pyplot(fig)
        progress_bar.progress(100)
        st.write("Stats:", stats)


    # Button to trigger PDF saving
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF..."):
            # Create and save PDF
            with PdfPages("trading_report.pdf") as pdf:
                pdf.savefig(fig)
                st.progress(100)  # Show completion
                
            # Success message and download button
            st.success("PDF Report created!")
            with open("trading_report.pdf", "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="trading_report.pdf",
                    mime="application/pdf"
                )

    # Clear progress bar after completion
    progress_bar.empty()
