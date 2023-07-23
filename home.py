import os
import openai
import streamlit as st

from components.sidebar import sidebar

st.set_page_config(
    page_title="Khlinic writer",
    page_icon="🖊️",
)


st.header("🖊️ Khlinic writer")
st.markdown("Un peu d'IA pour gagner beaucoup de 💸")
st.markdown("---")

if "shared" not in st.session_state:
   st.session_state["shared"] = True

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")


