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
        
        temperature = st.slider("Température (`randomness`):", min_value=0.0, max_value=2.0, value=st.session_state.get("TEMPERATURE", 1.0), step=0.1, help="###")
        st.session_state["TEMPERATURE"] = temperature

        presence_penalty = st.slider("Pénalité de présence (`presence_penalty`):", min_value=0.0, max_value=2.0, value=st.session_state.get("PRESENCE_PENALTY", 0.0), step=0.01, help="###")
        st.session_state["PRESENCE_PENALTY"] = presence_penalty

        frequency_penalty = st.slider("Pénalité de fréquence (`frequency_penalty`):", min_value=0.0, max_value=2.0, value=st.session_state.get("FREQUENCY_PENALTY", 0.0), step=0.01, help="###")
        st.session_state["FREQUENCY_PENALTY"] = frequency_penalty

        st.markdown("---")
        st.markdown("# À propos")
        st.markdown(
            "📖 Tous les crédits vont à Khlinic. "
        )
        
