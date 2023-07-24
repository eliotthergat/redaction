import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from dotenv import load_dotenv


medecin_prompt = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. tu vas devoir passer à la rédaction de l'article, je vais te donner le plan de contenu et le brief de chaque paragraphe. Tu dois utiliser ce plan et rédiger l'ensemble des paragraphes de manière détaillée. Illustre tes propos avec des expériences et des exemples. Utilise un ton de professionnel médical, d'expert, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinants. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement et le terme patient au lieu d’individu ou personne. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant aux soins mentionnés, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Et le plan [PLAN] sous format Markdown , dont tu dois conserver le balisage et l’ensemble des titres. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Utilise des listes numérotées et non numérotées si besoin. Rédige 1500 à 2000 mots. Chaque paragraphe doit contenir au minimum 3 à 4phrases. " 
education_prompt = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en éducation en santé. Tu as rédigé des articles médicaux pour les sites prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa médecine. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. La voix de la marque est informative, soutenante et autoritaire, avec un accent clair sur l'aide aux étudiants en médecine potentiels dans leurs efforts académiques. Le style de communication résonne un courant sous-jacent de réconfort et d'orientation, tandis que ses attributs linguistiques mettent en avant la connaissance, l'inclusivité et l'accessibilité. En essence, la personnalité / le style de la marque est celui d'un mentor expert fiable, offrant des conseils et des informations éducatives essentielles avec une attitude accessible. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. tu vas devoir passer à la rédaction de l'article, je vais te donner le plan de contenu et le brief de chaque paragraphe. Tu dois utiliser ce plan et rédiger l'ensemble des paragraphes de manière détaillée, en expliquant chaque idée. Illustre tes propos avec des expériences et des exemples. Utilise un ton de professionnel médical et de l’éducation, d'expert, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinants. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un étudiant s’intéressant aux études mentionnées, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Et le plan [PLAN] sous format Markdown , dont tu dois conserver le balisage et l’ensemble des titres. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Utilise des listes numérotées et non numérotées si besoin. Rédige 1500 à 2000 mots. Chaque paragraphe doit contenir au minimum 3 phrases."
agence_prompt = ""

medecin_analyzer = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, biologiques, physiologiques, chirurgicales, historiques et les conseils et toutes informations nécessaires pour répondre plus tard aux questions de [PLAN]. Conserve l'ensemble des détails. Ne parle pas de la clinique ou du chirurgien ayant écris l'article. Le texte à analyser est marqué [TEXT]"
education_analyzer = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en éducation en santé. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre s’inscrire en prépa médecine. Dans un premier temps, j'ai besoin que tu extraies toutes les informations de manière exhaustive sur cette page sous forme de liste. Reprends toutes les informations médicales, académiques, historiques, les astuces, les chiffres, les données, les propositions de valeurs, les services proposés et les conseils et toutes informations nécessaires pour répondre plus tard aux questions de [PLAN]. Conserve l'ensemble des détails. Ne parle pas de la prépa ou du rédacteur ayant écris l'article. Le texte à analyser est marqué [TEXT]"
agence_analyzer = ""

title_medecin = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Ta tâche est maintenant de proposer des titres supplémentaires à inclure dans l’article [TEXT] à partir des informations contenues dans la liste [INFOS]. Si des informations listées dans [INFOS] sont manquantes, propose moi un titre et un texte de paragraphe par idée. Tous les titres doivent être sous forme de question."
title_education = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en prépa médecine. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa médecine. Ta tâche est maintenant de proposer des titres supplémentaires à inclure dans l’article [TEXT] à partir des informations contenues dans la liste [INFOS]. Si des informations listées dans [INFOS] sont manquantes, propose moi un titre et un texte de paragraphe par idée. Tous les titres doivent être sous forme de question."
title_agence = ""

completer_medecin = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en médical. Tu as rédigé des articles médicaux pour les sites de médecins depuis 20 ans. Ta tâche est maintenant de rédiger un article médical. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de prendre rendez-vous chez leur médecin. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. Analyse le texte [TEXT] et regarde si tous les titres présents dans le plan [PLAN] sont présentes dans [TEXT]. Si l’article n’est pas fini, rédige la suite du plan sans modifier le contenu précédent. Utilise un ton de professionnel médical, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant au soin mentionné, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Rédige la suite de l’article sans reprendre le texte précédent dans ta réponse."
completer_education = "Ignore toutes les instructions avant celle-ci. Tu es un rédacteur web expert en études de santé. Tu as rédigé des articles pour les sites de prépa médecine depuis 20 ans. Ta tâche est maintenant de rédiger un article sur les études de santé. Les internautes qui consulteront cette page chercheront principalement à prendre des informations sur ce sujet avant de s’inscrire en prépa. Voici le ton de la marque pour laquelle tu devras rédiger : Le ton de la marque est hautement professionnel et informatif. La marque communique de manière détaillée, directe et précise, fournissant des informations complètes à son public. Il y a un élément de soin et de considération notable, trouvant un équilibre entre les conseils formels d'un professionnel de la santé et une communication empathique. Les attributs de langage gravitent autour de la terminologie médicale, du langage orienté vers la santé, des explications méthodiques et une emphase sur les détails. Le persona de la marque semble être celui d'un expert du secteur compétent, fiable et minutieux qui privilégie le bien-être des individus qu'il sert. Leur style se concentre sur l'instauration de la confiance, la démonstration d'expertise et l'assurance de la transparence dans la communication. Ta tâche est maintenant de rédiger un article ayant pour titre principal [TITRE]. Analyse le texte [TEXT] et regarde si tous les titres présents dans le plan [PLAN] sont présentes dans [TEXT]. Si l’article n’est pas fini, rédige la suite du plan sans modifier le contenu précédent. Utilise un ton de professionnel médical, avec des expressions idiomatiques. Ponctue tes phrases en insérant des virgules à des endroits pertinents. Utilise un maximum de détails, de language technique, scientifique et physiologique. Utilise le vouvoiement. Insère des phrases de transition naturelles et professionnelles entre les différentes parties du texte. Le lecteur est un patient s’intéressant au soin mentionné, il recherche une information claire, précise et exhaustive. Utilise les mots-clés inclus dans [KEYWORDS], chaque mot-clé est suivi du nombre de fois où il doit apparaitre. Les informations que tu dois inclures obligatoirement sont présentes dans [INFOS] et compléter cette base de connaissance avec tes propres informations. Rédige la suite de l’article sans reprendre le texte précédent dans ta réponse."
completer_agence = ""


st.session_state["analyzer_prompt"] = "#"
st.session_state["title_prompt"] = "#"
st.session_state["writer_prompt"] = "#"
st.session_state["completer_prompt"] = "#"

def define_client(client):
    if client == "Médecin":
        st.session_state["writer_prompt"] = medecin_prompt
        st.session_state["analyzer_prompt"] = medecin_analyzer
        st.session_state["title_prompt"] = title_medecin
        st.session_state["completer_prompt"] = completer_medecin
    elif client == "Éducation":
        st.session_state["writer_prompt"] = education_prompt
        st.session_state["analyzer_prompt"] = education_analyzer
        st.session_state["title_prompt"] = title_education
        st.session_state["completer_prompt"] = completer_education
    elif client == "Agence":
        st.session_state["writer_prompt"] = agence_prompt
        st.session_state["analyzer_prompt"] = agence_analyzer
        st.session_state["title_prompt"] = title_agence
        st.session_state["completer_prompt"] = completer_agence
    else:
        st.session_state["writer_prompt"] = "NE FAIS RIEN"
        st.session_state["analyzer_prompt"] = "NE FAIS RIEN"
        st.session_state["title_prompt"] = "NE FAIS RIEN"
        st.session_state["completer_prompt"] = "NE FAIS RIEN"