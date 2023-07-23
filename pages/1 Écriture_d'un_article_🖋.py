import streamlit as st
import openai
from time import perf_counter

st.set_page_config(
    page_title="Article complet - Khlinic",
    page_icon="🖋",
)


st.write("# L'écriture d'article 🖋")
st.markdown(
    """
    Cet outil permet d'écrire un article complet.
"""
)
