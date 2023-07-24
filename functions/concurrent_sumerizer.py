import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


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
    st.session_state["total_tokens"] = st.session_state["total_tokens"] + response["usage"]["total_tokens"]
    st.session_state["completion_tokens"] = st.session_state["completion_tokens"] + response["usage"]['completion_tokens']
    st.session_state["prompt_tokens"] = st.session_state["prompt_tokens"] + response["usage"]['prompt_tokens']
    return response["choices"][0]["message"]["content"]