import streamlit as st
import pandas as pd

st.title("Stock Data Viewer (Ticker-wise)")
uploaded_file = st.file_uploader("Upload final_output.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Full DataFrame")
    st.write(df)
    tickers = sorted(df["Ticker"].unique())
    st.subheader("Select Ticker")
    selected = st.selectbox("Choose a ticker", tickers)
    ticker_df = df[df["Ticker"] == selected]

    st.subheader(f"Data for {selected}")
    st.write(ticker_df)
    csv_data = ticker_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=f"Download {selected} CSV",
        data=csv_data,
        file_name=f"{selected}.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload final_output.csv first.")

