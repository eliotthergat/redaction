import os
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify
from time import perf_counter
from dotenv import load_dotenv

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
    st.session_state["total_tokens"] = st.session_state["total_tokens"] + response["usage"]["total_tokens"]
    st.session_state["completion_tokens"] = st.session_state["completion_tokens"] + response["usage"]['completion_tokens']
    st.session_state["prompt_tokens"] = st.session_state["prompt_tokens"] + response["usage"]['prompt_tokens']
    return response["choices"][0]["message"]["content"]