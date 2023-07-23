import os
import openai
import streamlit as st

from components.sidebar import sidebar

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")

st.set_page_config(page_title="Khlinic Brain", page_icon="🧠", layout="wide")
st.header("🧠 Khlinic Brain")
