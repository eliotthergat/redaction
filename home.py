import os
import openai
import streamlit as st

from components.sidebar import sidebar

st.set_page_config(
    page_title="Khlinic writer",
    page_icon="🖊️",
)


st.header("🖊️ Khlinic writer")
st.markdown("---")

if "shared" not in st.session_state:
   st.session_state["shared"] = True

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")

with st.expander("Concurrence", expanded=True):
    link_1 = st.text_input("Lien 1", placeholder="Lien concurrent #1")
    link_2 = st.text_input("Lien 2", placeholder="Lien concurrent #2")
    link_3 = st.text_input("Lien 3", placeholder="Lien concurrent #3")
    col1, col2, col3 = st.columns([2, 2,1])
    submit = col3.button("Scrapper 🏴‍☠️")


