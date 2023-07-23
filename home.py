import streamlit as st

st.set_page_config(
    page_title="Accueil - Khlinic",
    page_icon="✍🏻",
)
with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key')
