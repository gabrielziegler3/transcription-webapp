import logging
import streamlit as st
import httpx
import json

from src.logger import LogHandler
from src.utils import read_audio, plot_waveform


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"


def test():
    response = httpx.get(url=SERVER_URL)
    logger.info(f"Response: {response.content}")
    st.write(response.content)


def transcription():
    endpoint = SERVER_URL + "transcript"

    st.title('Transcription')

    st.sidebar.title("Services")
    st.sidebar.button("Transcription API")
    st.sidebar.button("Real Time Transcription")

    uploaded_file = st.file_uploader("Choose a file")

    logger.info(f"Uploaded file type {type(uploaded_file)}")

    if not uploaded_file:
        return

    audio = read_audio(uploaded_file)
    plot_waveform(audio)

    payload = {"file": uploaded_file}

    logger.info(f"Sending request with {uploaded_file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error attempting transcription API")
        return

    transc = json.loads(response.content)["transcription"]
    logger.info(f"Transcription: {transc}")
    st.write(transc)
