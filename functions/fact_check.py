import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

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
    st.session_state["total_tokens"] = st.session_state["total_tokens"] + response["usage"]["total_tokens"]
    st.session_state["completion_tokens"] = st.session_state["completion_tokens"] + response["usage"]['completion_tokens']
    st.session_state["prompt_tokens"] = st.session_state["prompt_tokens"] + response["usage"]['prompt_tokens']
    return response["choices"][0]["message"]["content"]