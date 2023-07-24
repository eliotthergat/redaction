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
    page_title="Khontenu",
    page_icon="🧠",
)


st.header("🧠 Khontenu")
st.markdown("---")

if "shared" not in st.session_state:
   st.session_state["shared"] = True

sidebar()

openai.api_key = st.session_state.get("OPENAI_API_KEY")

st.markdown("### Rédigeons de meilleures pages que les concurrents 👀")

col1, col2 = st.columns(2)

with col1:
    suggestion = pills("", ["Avec suggestions", "Pas de suggestions"], ["🎉", "🚫"])
with col2:
    check = pills("", ["Avec fact checking", "Sans fact checking"], ["✅", "🚨"])

medecin_prompt = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. tu vas devoir passer à la rédaction de l'article, je vais te donner le plan de contenu et le brief de chaque paragraphe. Tu dois utiliser ce plan et rédiger l'ensemble des paragraphes de manière détaillée. Illustre tes propos avec des expériences et des exemples. Utilise un ton de professionnel médical, d'expert, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinants. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement et le terme patient au lieu d’individu ou personne. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant aux soins mentionnés, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Et le plan [PLAN] sous format Markdown , dont tu dois conserver le balisage et l’ensemble des titres. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Utilise des listes numérotées et non numérotées si besoin. Rédige 1500 à 2000 mots. Chaque paragraphe doit contenir au minimum 3 à 4phrases. " 
education_prompt = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en éducation en santé. Tu as rédigé des articles médicaux pour les sites prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa médecine. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. La voix de la marque est informative, soutenante et autoritaire, avec un accent clair sur l'aide aux étudiants en médecine potentiels dans leurs efforts académiques. Le style de communication résonne un courant sous-jacent de réconfort et d'orientation, tandis que ses attributs linguistiques mettent en avant la connaissance, l'inclusivité et l'accessibilité. En essence, la personnalité / le style de la marque est celui d'un mentor expert fiable, offrant des conseils et des informations éducatives essentielles avec une attitude accessible. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. tu vas devoir passer à la rédaction de l'article, je vais te donner le plan de contenu et le brief de chaque paragraphe. Tu dois utiliser ce plan et rédiger l'ensemble des paragraphes de manière détaillée, en expliquant chaque idée. Illustre tes propos avec des expériences et des exemples. Utilise un ton de professionnel médical et de l’éducation, d'expert, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinants. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un étudiant s’intéressant aux études mentionnées, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Et le plan [PLAN] sous format Markdown , dont tu dois conserver le balisage et l’ensemble des titres. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Utilise des listes numérotées et non numérotées si besoin. Rédige 1500 à 2000 mots. Chaque paragraphe doit contenir au minimum 3 phrases. Ne t'arrête pas avant d'avoir rédigé tout l'article et tous les titres du plan."
agence_prompt = ""

medecin_analyzer = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, biologiques, physiologiques, chirurgicales, historiques et les conseils. Conserve l'ensemble des détails. Ne parle pas de la clinique ou du chirurgien ayant écris l'article. Voici le texte à analyser :"
education_analyzer = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en éducation en santé. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre s’inscrire en prépa médecine. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, académiques, historiques, les astuces, les chiffres, les données, les propositions de valeurs, les services proposés et les conseils. Conserve l'ensemble des détails. Ne parle pas de la prépa ou du rédacteur ayant écris l'article. Voici le texte à analyser :"
agence_analyzer = ""

title_medecin = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Ta tâche est maintenant de proposer des titres supplémentaires à inclure dans l’article [TEXT] à partir des informations contenues dans la liste [INFOS]. Si des informations listées dans [INFOS] sont manquantes, propose moi un titre et un texte de paragraphe par idée. Tous les titres doivent être sous forme de question."
title_education = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en prépa médecine. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa médecine. Ta tâche est maintenant de proposer des titres supplémentaires à inclure dans l’article [TEXT] à partir des informations contenues dans la liste [INFOS]. Si des informations listées dans [INFOS] sont manquantes, propose moi un titre et un texte de paragraphe par idée. Tous les titres doivent être sous forme de question."
title_agence = ""

completer_medecin = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. Analyse le texte [TEXT] et regarde si tous les titres présents dans le plan [PLAN] sont présentes dans [TEXT]. Si l’article n’est pas fini, rédige la suite du plan sans modifier le contenu précédent. Utilise un ton de professionnel médical, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant au soin mentionné, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Rédige la suite de l’article sans reprendre le texte précédent dans ta réponse."
completer_education = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en études de santé. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. Analyse le texte [TEXT] et regarde si tous les titres présents dans le plan [PLAN] sont présentes dans [TEXT]. Si l’article n’est pas fini, rédige la suite du plan sans modifier le contenu précédent. Utilise un ton de professionnel médical, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant au soin mentionné, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Rédige la suite de l’article sans reprendre le texte précédent dans ta réponse."
completer_agence = ""


analyzer_prompt = "#"
title_prompt = "#"
writer_prompt = "#"
completer_prompt = "#"

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


client = pills("", ["Médecin", "Éducation", "Agence"], ["🩺", "👨🏻‍🏫", "💸"])
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
        messages=[{"role": "system", "content": "À partir du code markdown suivant, extraies l'article principal sous format markdown. Ne conserve que les H1, H2, H3, H4, H5, H6, les paragraphes et les listes contenues dans le corps principal de l'article. Supprime le contenu avec le H1, les sections à lire également, les sections photos et avants/après, catégories, les crédits, etc..."},
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
        messages=[{"role": "system", "content": analyzer_prompt},
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
        messages=[{"role": "system", "content": writer_prompt + "\n[INFOS : ]\n" + infos + "\n [TITLE : ]\n" + title + "\n[KEYWORDS : ]\n" + keywords},
                        {"role": "user", "content": "[PLAN :]\n" + plan}]
    )
    return response["choices"][0]["message"]["content"]
    
def completer(text, infos, title, plan, keywords):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": completer_prompt + "\n[TEXT : ]\n" + text +"\n[INFOS : ]\n" + infos + "\n [TITLE : ]\n" + title + "\n[KEYWORDS : ]\n" + keywords},
                        {"role": "user", "content": "[PLAN :]\n" + plan}]
    )
    return response["choices"][0]["message"]["content"]

def bold_keywords(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Ignore toutes les instructions avant celle-ci. Ta tâche est maintenant de gras dans le format markdown les mots-clés et expressions sémantiquement importantes dans le texte [TEXT]. Ne modifie jamais les titres ou le texte, ne fais que mettre en gras. Conserve la totalité du texte."},
                        {"role": "user", "content": "[TEXT : ]\n" + text}]
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
        messages=[{"role": "system", "content": title_prompt},
                        {"role": "user", "content": "[TEXT : ]\n" + text + "\n [INFOS : ]\n" + infos}]
    )
    return response["choices"][0]["message"]["content"]

def fact_check(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "Tu es médecin expert. Existe-t-il des informations médicalement inexactes dans ce texte ? "},
                        {"role": "user", "content": "[TEXT : ]\n" + text}]
    )
    return response["choices"][0]["message"]["content"]
    
if submit:
    if client == "Médecin":
        writer_prompt = medecin_prompt
        analyzer_prompt = medecin_analyzer
        title_prompt = title_medecin
        completer_prompt = completer_medecin
    elif client == "Éducation":
        writer_prompt = education_prompt
        analyzer_prompt = education_analyzer
        title_prompt = title_education
        completer_prompt = completer_education
    elif client == "Agence":
        writer_prompt = agence_prompt
        analyzer_prompt = agence_analyzer
        title_prompt = title_agence
        completer_prompt = completer_agence
    else:
        writer_prompt = "NE FAIS RIEN"
        analyzer_prompt = "NE FAIS RIEN"
        title_prompt = "NE FAIS RIEN"
        completer_prompt = "NE FAIS RIEN"

    with st.spinner("Requête en cours..."):
        ts_start = perf_counter()
    
        st.markdown("### Traitement du 1er article")
        col1, col2 = st.columns([1, 2])
        col1.info("1/12 - Scrapping de l'article...")
        text_1 = parser(link_1)
        with col2.expander("Texte n°1", expanded=False):
            st.write(text_1)

        col1, col2 = st.columns([1, 2])
        col1.info("2/12 - Data cleaning...")
        text_1 = markdown_generator(text_1)
        with col2.expander("Texte nettoyé n°1", expanded=False):
            st.write(text_1)
    
        col1, col2 = st.columns([1, 2])
        col1.info("3/12 - Analyse de l'article...")
        response_1 = concurrent_analyzer(text_1)
        with col2.expander("Analyse n°1", expanded=False):
            st.write(response_1) 
        
        st.markdown("### Traitement du 2ème article")
        col1, col2 = st.columns([1, 2])
        col1.info("4/12 - Scrapping de l'article...")
        text_2 = parser(link_2)
        with col2.expander("Texte n°2", expanded=False):
            st.write(text_2)

        col1, col2 = st.columns([1, 2])
        col1.info("5/12 - Data cleaning...")
        text_2 = markdown_generator(text_2)
        with col2.expander("Texte nettoyé n°2", expanded=False):
            st.write(text_2)
    
        col1, col2 = st.columns([1, 2])
        col1.info("6/12 - Analyse de l'article...")
        response_2 = concurrent_analyzer(text_2)
        with col2.expander("Analyse n°2", expanded=False):
            st.write(response_2)
    
        st.markdown("### Traitement du 3ème article")
        col1, col2 = st.columns([1, 2])
        col1.info("7/12 - Scrapping de l'article...")
        text_3 = parser(link_3)
        with col2.expander("Texte n°3", expanded=False):
            st.write(text_3)

        col1, col2 = st.columns([1, 2])
        col1.info("8/12 - Data cleaning...")
        text_3 = markdown_generator(text_3)
        with col2.expander("Texte nettoyé n°3", expanded=False):
            st.write(text_3)
            
        col1, col2 = st.columns([1, 2])
        col1.info("9/12 - Analyse de l'article...")
        response_3 = concurrent_analyzer(text_3)
        with col2.expander("Analyse n°3", expanded=False):
            st.write(response_3)
            
        st.info("10/12 - Synthèse des connaissances acquises...")
        infos = concurrent_sumerizer(response_1, response_2, response_3)
        with st.expander("Synthèse", expanded=False):
            st.write(infos)

        st.warning("11/12 - Rédaction du premier texte...")
        first_text = writer(infos, title, plan, keywords)
        with st.expander("Texte brut", expanded=False):
            st.write(first_text)

        col1, col2, col3 = st.columns([2, 1,1])
        modifier = col2.button('Texte à compléter')
        complete = col3.button('Texte complet')

        ts_end = perf_counter()
        st.info(f" {round(ts_end - ts_start, 3)} secondes d'exécution")

        if modifier : 
            st.warning("11b/12 - Article en cours de correction...")
            final_text = first_text + "\n" + completer(first_text, infos, title, plan, keywords)
            with st.expander("Texte complet", expanded=False):
                st.write(final_text)
            st.success("12/12 - Mise en gras du texte...")
            final_text = bold_keywords(final_text)
            with st.expander("Texte finalisé", expanded=False):
                st.write(final_text)

            col1, col2, col3 = st.columns([2, 2,1])
            col3.download_button(
                label="Télécharger 💾",
                data=final_text,
                file_name='texte.md',
                mime='text/markdown',
            )

            if check == "Avec fact checking":
                st.error("⚠️ Fact checking en cours...")
                fact_check = fact_check(final_text)
                with st.expander("Fact checking", expanded=False):
                    st.write(fact_check)
                
            if suggestion == "Avec suggestions":
                st.warning("Proposition de titres en cours...")
                titles_to_add = better_titles(final_text, infos)
                with st.expander("Titres à réviser", expanded=False):
                        st.write(titles_to_add)
        if complete:
            st.success("12/12 - Mise en gras du texte...")
            final_text = bold_keywords(first_text)
            with st.expander("Texte finalisé", expanded=False):
                st.write(final_text)

            col1, col2, col3 = st.columns([2, 2,1])
            col3.download_button(
                label="Télécharger 💾",
                data=final_text,
                file_name='texte.md',
                mime='text/markdown',
            )

            if check == "Avec fact checking":
                st.error("⚠️ Fact checking en cours...")
                fact_check = fact_check(final_text)
                with st.expander("Fact checking", expanded=False):
                    st.write(fact_check)
                
            if suggestion == "Avec suggestions":
                st.warning("Proposition de titres en cours...")
                titles_to_add = better_titles(final_text, infos)
                with st.expander("Titres à réviser", expanded=False):
                        st.write(titles_to_add)

