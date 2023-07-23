import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def sidebar():
    with st.sidebar:
        st.image('assets/logo.svg')
        st.markdown(
                "## Comment fonctionne l'outil ?\n"
                "1. Entrez une clé OpenAI\n"
                "2. Choisissez les liens à explorer\n"
                "3. Entrez le plan\n"
                "4. Entrez les mots-clés\n"
            )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here",
            help="Needed to use the OpenAI API",
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )
        st.session_state["OPENAI_API_KEY"] = api_key_input
        st.markdown("---")
        st.markdown("# Paramètres")
        max_tokens = st.slider("Longueur maximale (`max_tokens`):", min_value=1, max_value=8000, value=st.session_state.get("MAX_TOKENS", 2048), step=25, help="Maximum number of tokens to consume")
        st.session_state["MAX_TOKENS"] = max_tokens
        
        #PARAMS["temperature"] = st.slider("Température (`randomness`)", min_value=0.0, max_value=2.0, value=1, step=0.1)
        #PARAMS["presence_penalty"] = st.slider("Pénalité de présence (`presence_penalty`)", min_value=0.0, max_value=2.0, value=0, step=0.1)
        #PARAMS["frequency_penalty"] = st.slider("Pénalité de fréquence (`frequence_penalty`)", min_value=0.0, max_value=2.0, value=0, step=0.1)
        st.markdown("---")
        st.markdown("# À propos")
        st.markdown(
            "📖 Tous les crédits vont à Khlinic. "
        )
        
