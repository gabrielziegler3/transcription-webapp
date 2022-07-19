import streamlit as st
import logging
import json
import httpx

from src.logger import LogHandler
from src.utils import read_audio, plot_waveform


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"


def voice_activity_detection():
    st.title('Voice activity detection')

    st.sidebar.title("Services")
    st.sidebar.button("Transcription API")
    st.sidebar.button("Real Time Transcription")

    uploaded_file = st.file_uploader("Choose a file")

    if not uploaded_file:
        return

    audio = read_audio(uploaded_file)
    plot_waveform(audio)
    speech_timestamps = get_speech_timestamps()
    st.write(speech_timestamps)


def get_speech_timestamps(file):
    """
    Client to send request with audio file to receive speech timestamps
    """
    endpoint = SERVER_URL + "get_speech_timestamps"

    payload = {
        "file": file
    }

    logger.info(f"Sending request with {file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error on VAD API")
        return

    logger.debug(f"Speech timestamps {response.content}")

    speech_timestamps = json.loads(response.content)["speech_timestamps"]
    return speech_timestamps
