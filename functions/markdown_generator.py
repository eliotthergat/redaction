import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def markdown_generator(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=st.session_state.get("TEMPERATURE"),
        max_tokens=st.session_state.get("MAX_TOKENS"),
        top_p=1,
        frequency_penalty=st.session_state.get("FREQUENCY_PENALTY"),
        presence_penalty=st.session_state.get("PRESENCE_PENALTY"),
        messages=[{"role": "system", "content": "À partir du code markdown suivant, extraies l'article principal sous format markdown. Ne conserve que les H1, H2, H3, H4, H5, H6, les paragraphes et les listes contenues dans le corps principal de l'article. Supprime le contenu avec le H1, les sections à lire également, les sections photos et avants/après, catégories, les crédits, etc..."},
                        {"role": "user", "content": text}]
    )
    st.write(response["usage"])
    return response["choices"][0]["message"]["content"]