import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def concurrent_sumerizer(response_1, response_2, response_3):
    for attempt in range(st.session_state["max_retries"]):
        try:
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
            break
        except openai.error.Timeout as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API request timed out: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1

        except openai.error.APIError as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API returned an API Error: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1
        
        except openai.error.APIConnectionError as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API request failed to connect: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1
        
        except openai.error.InvalidRequestError as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API request was invalid: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1

        except openai.error.AuthenticationError as e:
                st.write(f"OpenAI API request was not authorized: {e}, retrying...")
                st.write("Please change your OpenAI key.")
                st.session_state["error"] = 1
                pass
        
        except openai.error.PermissionError as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API request was not permitted: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1
        
        except openai.error.RateLimitError as e:
            if attempt < st.session_state["max_retries"] - 1:  # ne pas attendre après la dernière tentative 
                st.write(f"OpenAI API request exceeded rate limit: {e}, retrying...")
                time.sleep(st.session_state["wait_time"])
            else:
                st.write("Max retries reached. Aborting.")
                st.session_state["error"] = 1