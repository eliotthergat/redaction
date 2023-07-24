import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def completer(text, infos, title, plan, keywords):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": st.session_state.get("completer_prompt") + "\n[TEXT : ]\n" + text +"\n[INFOS : ]\n" + infos + "\n [TITLE : ]\n" + title + "\n[KEYWORDS : ]\n" + keywords},
                        {"role": "user", "content": "[PLAN :]\n" + plan}]
    )
    return response["choices"][0]["message"]["content"]