import os
import openai
import streamlit as st

from components.sidebar import sidebar

st.set_page_config(
    page_title="Khlinic writer",
    page_icon="🖊️",
)
st.header("🖊️ Khlinic writer")


sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")

col1, col2, col3 = st.columns([1, 1,1])
col1.subheader("Écriture 🖋")
col1.markdown("Pour écrire un article d'après un plan, des mots-clés et des liens.")
faq = col1.button("Écrire")

