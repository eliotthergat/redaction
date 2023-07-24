import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def writer(infos, title, plan, keywords):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": st.session_state.get['writer_prompt'] + "\n[INFOS : ]\n" + st.session_state.get['infos'] + "\n [TITLE : ]\n" + st.session_state.get['title'] + "\n[KEYWORDS : ]\n" + st.session_state.get['keywords']},
                        {"role": "user", "content": "[PLAN :]\n" + st.session_state.get['plan']}]
    )
    return response["choices"][0]["message"]["content"]