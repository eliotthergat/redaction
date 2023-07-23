import streamlit as st
import openai
from time import perf_counter
from streamlit_extras.app_logo import add_logo

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
st.sidebar.subheader("Paramètres")
PARAMS = {}
openai.api_key = "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"
PARAMS["engine"] = "text-davinci-003"

PARAMS["max_tokens"] = st.sidebar.slider("Longueur maximale (`max_tokens`):", min_value=1, max_value=4097, value=3100, step=25)
PARAMS["temperature"] = st.sidebar.slider("Température (`randomness`)", min_value=0.0, max_value=1.0, value=0.7)
PARAMS["best_of"] = st.sidebar.slider("Nombre de générations (`best_of`):", min_value=1, max_value=10, step=1, value=1)
PARAMS["presence_penalty"] = st.sidebar.slider("Pénalité de présence (`presence_penalty`)", min_value=0.0, max_value=1.0, value=0.3)
PARAMS["frequency_penalty"] = st.sidebar.slider("Pénalité de fréquence (`frequence_penalty`)", min_value=0.0, max_value=1.0, value=0.1)


st.subheader("Requête")
col1, col2 = st.columns([1, 1])
mots = col1.text_input("Nombre de mots👇", value="1500")
plan = st.text_area("Plan de contenu 👇",value="")
keywords = st.text_area("Mots-clés 🔑")

PARAMS["prompt"] = "Supprime les sauts de ligne et mets des virgules à la place : \n" + keywords + "\n Réponse :"
col1, col2, col3 = st.columns([1, 1,4])
submit = col1.button("Générer")
relecture = col2.checkbox("Relecture", value="1")

st.subheader("Résultats")
if submit:
        with st.spinner("Requête en cours..."):
            ts_start = perf_counter()
            st.warning("Optimisation des mots-clés")
            request = openai.Completion.create(**PARAMS)
            keywords_modified = request["choices"][0].text
            st.subheader("Mots-clés reformatés")
            st.info(request["choices"][0].text)
            PARAMS["prompt"] = "Écris un article optimisé pour le SEO pour une page web, de " + mots + " mots environ. Rédige un article long, qui pourrait être classé dans Google sur les mots-clés donnés. L'article doit contenir des paragraphes riches et complets, avec beaucoup d'explications (biologie, histologie,...) et de variations de langage. Prends un ton de médecin, utilise les mots-clés suivants \"" + keywords_modified + "\", utilise les titres suivants en conservant tout le marquage markdown :\n" + plan + "\n Article :"
            st.warning("Écriture en cours")
            request = openai.Completion.create(**PARAMS)
            st.markdown(request["choices"][0].text)
            if relecture == 1:
                st.warning("Relecture en cours")
                del PARAMS["engine"], PARAMS["best_of"], PARAMS["presence_penalty"], PARAMS["frequency_penalty"], PARAMS["prompt"], PARAMS["max_tokens"]
                PARAMS["model"] = "text-davinci-edit-001"
                PARAMS["instruction"] = "Remplace toutes les expressions suivantes :\n- \"il est important de\"\n- \"il est donc important de\"\n- \"En outre\"\n- \"les personnes\"\n- \"la personne\"\n- \"il est important de suivre les instructions de\"\n- \"heureusement\"\n- \"la plupart des personnes\"\n- \"des personnes\"\n- \"choses\""
                PARAMS["input"] = request["choices"][0].text
                request = openai.Edit.create(**PARAMS)
            ts_end = perf_counter()
        st.subheader("Texte optimisé")
        st.markdown(request["choices"][0].text)
        st.info(f" {round(ts_end - ts_start, 3)} secondes d'exécution")
