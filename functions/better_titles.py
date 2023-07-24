import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def better_titles(text, infos):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": st.session_state.get("title_prompt")},
                        {"role": "user", "content": "[TEXT : ]\n" + text + "\n [INFOS : ]\n" + infos]}]
    )
    return response["choices"][0]["message"]["content"]