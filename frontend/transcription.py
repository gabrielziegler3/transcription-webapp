import io
import logging
import streamlit as st
import requests
import json
import numpy as np

from src.logger import LogHandler
from src.custom_plots import plot_line


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"
TRANSCRIPTION_URL = "http://host.docker.internal:80/transcript/"


def test():
    response = requests.get(url="http://host.docker.internal:80/")
    logger.info(f"Response: {response.content}")
    st.write(response.content)

def _read_audio(file: io.Bytes) -> np.ndarray:
    endpoint = SERVER_URL + "read_audio"

    payload = {
        "file": file
    }

    logger.info(f"Sending request to {}")
    response = requests.post(
        url=endpoint,
        files=payload,
        # headers=headers
    )
    requests.post()


def transcription():
    st.title('Transcription')

    st.sidebar.title("Services")
    st.sidebar.button("Transcription API")
    st.sidebar.button("Real Time Transcription")

    uploaded_file = st.file_uploader("Choose a file")

    if not uploaded_file:
        return

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    logger.info("File read succesfully")

    """Move this code"""
    audio = _read_audio(uploaded_file)
    plot_line(x=range(audio.shape[1]), y=audio.flatten())
    """"""

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
