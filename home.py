import streamlit as st
# from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras.app_logo import add_logo

st.set_page_config(
    page_title="Accueil - Khlinic",
    page_icon="✍🏻",
)
# add_logo("assets/logo_black.png", height=50)

if "shared" not in st.session_state:
   st.session_state["shared"] = True
st.write("# Les outils de rédaction Khlinic ✍🏻")
st.markdown(
    """
    Ces outils permettent de générer des textes pour Khlinic.
"""
)
st.sidebar.subheader("Paramètres")
PARAMS = {}
PARAMS["api_key"] = st.text_area("OpenAI API key")
