import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="History")

st.title("📜 Analysis History")

response = requests.get("http://127.0.0.1:8000/history")

history = response.json()

if len(history) == 0:

    st.info("No history found.")

else:

    df = pd.DataFrame(history)

    st.dataframe(df, use_container_width=True)