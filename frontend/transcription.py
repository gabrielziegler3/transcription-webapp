import logging
import streamlit as st
import requests
import json

from src.logger import LogHandler


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
TRANSCRIPTION_URL = "http://host.docker.internal:80/transcript"


def test():
    response = requests.get(url="http://host.docker.internal:80/")
    logger.info(f"Response: {response.content}")
    st.write(response.content)

def transcription():
    st.title('Transcription')

    uploaded_file = st.file_uploader("Choose a file")

    if not uploaded_file:
        return

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    logger.info("File read succesfully")

    # headers = {
    #     "Content-Type": "audio/form-data",
    # }
    payload = {
        "file": uploaded_file
    }

    logger.info(f"Sending request to {TRANSCRIPTION_URL}")
    response = requests.post(
        url=TRANSCRIPTION_URL,
        files=payload,
        # headers=headers
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error attempting transcription API")

    response = json.loads(response.content)
    transc = response.get('transcription')
    logger.info(f"Transcription: {transc}")
    st.write(transc)
