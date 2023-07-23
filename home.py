import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from streamlit_pills import pills 


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

suggestion = pills("", ["Avec suggestions", "Pas de suggestions"], ["🎉", "🚫"])
with st.expander("Concurrence", expanded=False):
    link_1 = st.text_input("Concurrent n°1", placeholder="Lien")
    link_2 = st.text_input("Concurrent n°2", placeholder="Lien")
    link_3 = st.text_input("Concurrent n°3", placeholder="Lien")
    
    #text_1 = st.text_area("Concurrent n°1", placeholder="Contenu")
    #text_2 = st.text_area("Concurrent n°2", placeholder="Contenu")
    #text_3 = st.text_area("Concurrent n°3", placeholder="Contenu")
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
    tags = soup.findAll('img')
    for match in tags:
        match.decompose()
    tags = soup.findAll('picture')
    for match in tags:
        match.decompose()
    tags = soup.findAll('head')
    for match in tags:
        match.decompose()
    tags = soup.findAll('header')
    for match in tags:
        match.decompose()
    tags = soup.findAll('script')
    for match in tags:
        match.decompose()
    tags = soup.findAll('noscript')
    for match in tags:
        match.decompose()
    tags = soup.findAll('a')
    for match in tags:
        del match["href"]
    tags = soup.findAll('div')
    for match in tags:
        del match["class"]
        del match["id"]
        del match["role"]
    
    if str(soup.find('article')) != 'None':
        main = soup.find('article')
    elif str(soup.find('main')) != 'None':
        main = soup.find('main')
    else:
        main = soup.find('body')
    cleaned_html = str(main)
    markdown_text = markdownify.markdownify(cleaned_html)
    return markdown_text
def markdown_generator(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "À partir du code markdown suivant, extraies l'article principal sous format markdown. Ne conserve que les H1, H2, H3, H4, H5, H6, les paragraphes et les listes contenues dans le corps principal de l'article. Supprime les sections à lire également, catégories, les crédits, etc..."},
                        {"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]
    
def concurrent_analyzer(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, biologiques, physiologiques, chirurgicales, historiques et les conseils. Conserve l'ensemble des détails. Ne parle pas de la clinique ou du chirurgien ayant écris l'article. Voici le texte à analyser :"},
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

    with st.spinner("Requête en cours..."):
            ts_start = perf_counter()
        
            st.markdown("### Traitement du 1er article...")
            col1, col2 = st.columns([1, 2])
            col1.info("1/9 - Scrapping de l'article...")
            text_1 = parser(link_1)
            with col2.expander("Texte n°1", expanded=False):
                st.write(markdown_generator(text_1))
        
            col1, col2 = st.columns([1, 2])
            col1.info("2/9 - Analyse de l'article...")
            response_1 = concurrent_analyzer(text_1)
            with col2.expander("Analyse n°1", expanded=False):
                st.write(response_1) 
            
            st.markdown("### Traitement du 2ème article...")
            col1, col2 = st.columns([1, 2])
            col1.info("3/9 - Scrapping de l'article...")
            text_2 = parser(link_2)
            with col2.expander("Texte n°2", expanded=False):
                st.write(markdown_generator(text_2))
        
            col1, col2 = st.columns([1, 2])
            col1.info("4/9 - Analyse de l'article...")
            response_2 = concurrent_analyzer(text_2)
            with col2.expander("Analyse n°2", expanded=False):
                st.write(response_2)
        
            st.markdown("### Traitement du 3ème article...")
            col1, col2 = st.columns([1, 2])
            col1.info("5/9 - Scrapping de l'article...")
            text_3 = parser(link_3)
            with col2.expander("Texte n°3", expanded=False):
                st.write(markdown_generator(text_3))
                
            col1, col2 = st.columns([1, 2])
            col1.info("6/9 - Analyse de l'article...")
            response_3 = concurrent_analyzer(text_3)
            with col2.expander("Analyse n°3", expanded=False):
                st.write(response_3)
                
            st.info("7/9 - Synthèse des connaissances acquises...")
            infos = concurrent_sumerizer(response_1, response_2, response_3)
            with st.expander("Synthèse", expanded=False):
                st.write(infos)

            st.warning("8/9 - Rédaction du premier jet...")
            first_text = writer(infos, title, plan, keywords)
            with st.expander("Texte brut", expanded=False):
                st.write(first_text)

            st.success("9/9 - Amélioration à partir des mots-clés...")
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
            if suggestion == "Avec suggestions":
                st.warning("Proposition de titres en cours...")
                titles_to_add = better_titles(final_text, infos)
                with st.expander("Titres à réviser", expanded=False):
                        st.write(titles_to_add)
        
            ts_end = perf_counter()
            st.info(f" {round(ts_end - ts_start, 3)} secondes d'exécution")
