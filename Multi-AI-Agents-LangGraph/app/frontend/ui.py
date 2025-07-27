
import streamlit as st 
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
#from app.prompts.system_prompt import *



logger = get_logger(__name__)

st.set_page_config(
    page_title="Multi AI Agent", 
    layout="centered"
)

st.title("Multi AI Agent")

system_prompt = st.text_area("System Prompt", placeholder="Define your AI Agent")
selected_model = st.selectbox(
    "Select your Model: ", settings.ALLOWED_MODEL_NAMES)

allow_web_search = st.checkbox("Allow web search")


user_query = st.text_area("User query",
    placeholder="Enter your query here",)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search,
    }

    try:
        logger.info(f"Sending request to API: {API_URL} with payload: {payload}")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info(f"Received response: {agent_response}")
        
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            logger.error(f"Error from API: {response.status_code} - {response.text}")
            st.error(f"Error from API: {response.status_code} - {response.text}")
            raise CustomException(f"Error from API: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error occurred while sending request to backend")
        st.error(str(CustomException(f"Failed to communicate with backend")))