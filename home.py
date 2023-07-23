import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify

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

st.markdown("### Allons explorer les meilleures pages des concurrents 👀")
with st.expander("Concurrence", expanded=True):
    link_1 = st.text_input("Lien 1", placeholder="Lien concurrent #1")
    link_2 = st.text_input("Lien 2", placeholder="Lien concurrent #2")
    link_3 = st.text_input("Lien 3", placeholder="Lien concurrent #3")
    col1, col2, col3 = st.columns([2, 2,1])
    submit = col3.button("Scrapper 🏴‍☠️", use_container_width=1)

def parser(link):
    res = requests.get(link_1)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = ['[document]','noscript','header','html','meta','head', 'input','script','style'
        # there may be more elements you don't want, such as "style", etc.
    ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output
if submit:
    st.success("Test")
    st.write(parser(link_1))
