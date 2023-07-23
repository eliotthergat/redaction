import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from streamlit_pills import pills
import trafilatura

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

st.markdown("### Rédigeons de meilleures pages que les concurrents 👀")

suggestion = pills("", ["Pas de suggestions", "Avec suggestions"], ["🚫", "🎉"])
with st.expander("Concurrence", expanded=False):
    link_1 = st.text_input("Concurrent n°1", placeholder="Lien")
    text_1 = st.text_area("Concurrent n°1", placeholder="Contenu")
    text_2 = st.text_area("Concurrent n°2", placeholder="Contenu")
    text_3 = st.text_area("Concurrent n°3", placeholder="Contenu")
with st.expander("Plan de contenu", expanded=False):
    title = st.text_input("Titre", placeholder="Le titre de l'article")
    plan = st.text_area("Plan", placeholder="Le plan de l'article")
    keywords = st.text_area("Mots-clés", placeholder="Les mots-clés à utiliser")


col1, col2, col3 = st.columns([2, 2,1])
submit = col3.button("Rédiger ✍🏻", use_container_width=1)

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
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Remets toutes les informations contenues dans les textes 1, 2 et 3 sous forme d'une seule liste complète. N'oublie aucune information contenue dans les 3 textes."},
                        {"role": "user", "content": "[TEXTE 1 : ]\n" + response_1 + "\n [TEXTE 2 : ]\n" + response_2 + "\n [TEXTE 3 : ]\n" + response_3}]
    )
    return response["choices"][0]["message"]["content"]

def writer(infos, title, plan, keywords):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecine. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. tu vas devoir passer à la rédaction de l'article, je vais te donner le plan de contenu et le brief de chaque paragraphe. Tu dois utiliser ce plan et rédiger l'ensemble des paragraphes de manière détaillée, en expliquant chaque bullet point. Illustre tes propos avec des expériences et des exemples. Utilise un ton de professionnel médical, d'expert, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinants. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement et le terme « patient » au lieu d’individu ou personne. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant aux soins mentionnés, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS]. Et le plan [PLAN] sous format Markdown , dont tu dois conserver le balisage et l’ensemble des titres. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Utilise des listes numérotées et non numérotées si besoin. Rédige 1500 à 2000 mots."},
                        {"role": "user", "content": "[INFOS : ]\n" + infos + "\n [TITLE : ]\n" + title + "\n [PLAN : ]\n" + plan + "\n [KEYWORDS : ]\n" + keywords}]
    )
    return response["choices"][0]["message"]["content"]
    
def better_keywords(text, keywords):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecine. Ta tâche est maintenant d’améliorer l’article contenu dans [TEXT] avec les mots-clés contenus dans [KEYWORDS]. Ajoute les mots-clés manquants aux endroits pertinents, sans modifier les titres, les paragraphes ou le sens du contenu. Tu dois améliorer sémantiquement le texte dans le dénaturer."},
                        {"role": "user", "content": "[TEXT : ]\n" + text + "\n [KEYWORDS : ]\n" + keywords}]
    )
    return response["choices"][0]["message"]["content"]

def better_titles(text, infos):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecine. Ta tâche est maintenant de proposer des titres supplémentaires à inclure dans l’article [TEXT] à partir des informations contenues dans la liste [INFOS]. Si des informations listées dans [INFOS] sont manquantes, propose moi un titre et un texte de paragraphe par idée."},
                        {"role": "user", "content": "[TEXT : ]\n" + text + "\n [INFOS : ]\n" + infos}]
    )
    return response["choices"][0]["message"]["content"]
    
if submit:

    downloaded = trafilatura.fetch_url('https://www.crpce.com/chirurgie-esthetique/chirurgie-visage')
    text_bis = trafilatura.extract(downloaded)
    st.write(text_bis)

    with st.spinner("Requête en cours..."):
            ts_start = perf_counter()

            col1, col2 = st.columns([1, 2])
            col1.info("1/7 - Analyse du premier article...")
            response_1 = concurrent_analyzer(text_1)
            with col2.expander("Analyse n°1", expanded=False):
                st.write(response_1)
                
            col1, col2 = st.columns([1, 2])
            col1.info("2/7 - Analyse du second article...")
            response_2 = concurrent_analyzer(text_2)
            with col2.expander("Analyse n°2", expanded=False):
                st.write(response_2)

            col1, col2 = st.columns([1, 2])
            col1.info("3/7 - Analyse du troisième article...")
            response_3 = concurrent_analyzer(text_3)
            with col2.expander("Analyse n°3", expanded=False):
                st.write(response_3)
                
            st.info("4/7 - Synthèse des connaissances acquises...")
            infos = concurrent_sumerizer(response_1, response_2, response_3)
            with st.expander("Synthèse", expanded=False):
                st.write(infos)

            st.warning("5/7 - Rédaction du premier jet...")
            first_text = writer(infos, title, plan, keywords)
            with st.expander("Texte brut", expanded=False):
                st.write(first_text)

            st.success("6/7 - Amélioration à partir des mots-clés...")
            final_text = better_keywords(first_text, keywords)
            with st.expander("Texte final", expanded=False):
                    st.write(final_text)

            col1, col2, col3 = st.columns([2, 2,1])
            col3.download_button(
                label="Télécharger 💾",
                data=final_text,
                file_name='texte.md',
                mime='text/markdown',
            )
            if suggestion:
                st.warning("7/7 - Proposition de titres en cours...")
                titles_to_add = better_titles(final_text, infos)
                with st.expander("Titres à réviser", expanded=False):
                        st.write(titles_to_add)
        
            ts_end = perf_counter()
            st.info(f" {round(ts_end - ts_start, 3)} secondes d'exécution")
