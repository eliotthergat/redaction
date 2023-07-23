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
        st.markdown("# À propos")
        st.markdown(
            "📖 Tous les crédits vont à Khlinic. "
        )
