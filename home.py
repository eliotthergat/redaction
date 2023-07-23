import streamlit as st

st.set_page_config(
    page_title="Accueil - Khlinic",
    page_icon="✍🏻",
)
with st.sidebar:
    st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Upload a pdf, docx, or txt file📄\n"
            "3. Ask a question about the document💬\n"
        )
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="Paste your OpenAI API key here (sk-...)",
        help="Needed to use the OpenAI API",  # noqa: E501
    )
