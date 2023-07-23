import streamlit as st
import openai
from time import perf_counter

st.set_page_config(
    page_title="Article complet - Khlinic",
    page_icon="🖋",
)

add_logo("assets/logo_black.png", height=50)

st.write("# L'écriture d'article 🖋")
st.markdown(
    """
    Cet outil permet d'écrire un article complet.
"""
)
