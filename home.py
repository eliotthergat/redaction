import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter

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

openai.api_key = st.session_state.get("OPENAI_API_KEY")

st.markdown("### Allons explorer les meilleures pages des concurrents 👀")
with st.expander("Concurrence", expanded=True):
    text_1 = st.text_area("Concurrent n°1", placeholder="Contenu")
    text_2 = st.text_area("Concurrent n°2", placeholder="Contenu")
    text_3 = st.text_area("Concurrent n°3", placeholder="Contenu")
with st.expander("Plan de contenu", expanded=True):
    title = st.text_input("Titre", placeholder="Le titre de l'article")
    plan = st.text_area("Plan", placeholder="Le plan de l'article")
    keywords = st.text_area("Mots-clés", placeholder="Les mots-clés à utiliser")

col1, col2, col3 = st.columns([2, 2,1])
submit = col3.button("Scrapper 🏴‍☠️", use_container_width=1)

def parser(link):
    res = requests.get(link)
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
def concurrent_analyzer(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, biologiques, physiologiques, chirurgicales, historiques et les conseils. Conserve l'ensemble des détails. Voici le texte à analyser :"},
                        {"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

def concurrent_sumerizer(response_1, response_2, response_3):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecine. Reprends toutes les informations médicales, physiologiques, biologiques, anatomiques, les conseils et fais une liste de ces informations. Cette liste servira à la rédaction d'un article complet sur le sujet, n'oublie pas d'information et sois exhaustif. Voici les textes à analyser :"},
                        {"role": "user", "content": "[TEXTE 1 : ]\n" + response_1 + "\n [TEXTE 2 : ]\n" + response_2 + "\n [TEXTE 3 : ]\n" + response_3}]
    )
    return response["choices"][0]["message"]["content"]
    
if submit:
    with st.spinner("Requête en cours..."):
            ts_start = perf_counter()
        
            st.info("Analyse du premier article...")
            response_1 = concurrent_analyzer(text_1)
            with st.expander("Analyse n°1", expanded=False):
                st.write(response_1)
                
            st.info("Analyse du second article...")
            response_2 = concurrent_analyzer(text_2)
            with st.expander("Analyse n°2", expanded=False):
                st.write(response_2)

            st.info("Analyse du troisième article...")
            response_3 = concurrent_analyzer(text_3)
            with st.expander("Analyse n°3", expanded=False):
                st.write(response_3)
                
            st.info("Synthèse des connaissances acquises...")
            complete = concurrent_sumerizer(response_1, response_2, response_3)
            st.write(complete)
        
            ts_end = perf_counter()
            st.info(f" {round(ts_end - ts_start, 3)} secondes d'exécution")
