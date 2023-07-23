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

openai.api_key = st.session_state.get("OPENAI_API_KEY")

st.markdown("### Allons explorer les meilleures pages des concurrents 👀")
with st.expander("Concurrence", expanded=True):
    link_1 = st.text_input("Lien 1", placeholder="Lien concurrent #1")
    link_2 = st.text_input("Lien 2", placeholder="Lien concurrent #2")
    link_3 = st.text_input("Lien 3", placeholder="Lien concurrent #3")
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
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecine. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Dans un premier temps, j'ai besoin que tu extraies toutes les informations utiles sur cette page sous forme de liste. Concentre-toi sur les informations médicales, biologiques, physiologiques, chirurgicales, historiques et les conseils. Voici le texte à analyser :"},
                        {"role": "user", "content": text}]
        
    )
    return response["choices"][0]["message"]["content"]
if submit:
    st.success("Test")
    text_1 = parser(link_1)
    response_1 = concurrent_analyzer(text_1)
    st.write(response_1)
