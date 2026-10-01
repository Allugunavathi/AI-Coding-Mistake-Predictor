import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Coding Dashboard")

response = requests.get("http://127.0.0.1:8000/history")
history = response.json()

if len(history) == 0:
    st.warning("No history available.")

else:

    df = pd.DataFrame(history)

    total = len(df)

    average = round(df["score"].mean(), 2)

    highest = df["score"].max()

    lowest = df["score"].min()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Analyses", total)

    with col2:
        st.metric("Average Score", average)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Highest Score", highest)

    with col4:
        st.metric("Lowest Score", lowest)

    st.divider()

    st.subheader("📈 Score History")

    st.line_chart(df["score"])

    st.subheader("📋 Recent Analyses")

    st.dataframe(df, use_container_width=True)