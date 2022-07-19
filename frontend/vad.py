import io
import streamlit as st
import logging
import json
import numpy as np
import httpx


from src.logger import LogHandler
from src.custom_plots import plot_line


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"


def _read_audio(file: io.BytesIO) -> np.ndarray:
    endpoint = SERVER_URL + "read_audio"

    payload = {
        "file": file
    }

    logger.info(f"Sending request with {file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
        # headers=headers
    )
    if response.status_code != 200:
        logger.info(f"Couldn't read audio. Received {response.status_code} status code")

    signal = json.loads(response.content)["signal"]
    audio = np.array(signal)

    logger.info(audio)
    logger.info(f"Audio with shape {audio.shape} read")

    return audio


def get_speech_timestamps():
    endpoint = SERVER_URL + "get_speech_timestamps"

    st.title('Voice activity detection')

    st.sidebar.title("Services")
    st.sidebar.button("Transcription API")
    st.sidebar.button("Real Time Transcription")

    uploaded_file = st.file_uploader("Choose a file")

    if not uploaded_file:
        return

    audio = _read_audio(uploaded_file)
    plot_line(x=range(len(audio.flatten())), y=audio.flatten())

    payload = {
        "file": uploaded_file
    }

    logger.info(f"Sending request with {uploaded_file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error on VAD API")
        return

    logger.debug(f"Speech timestamps {response.content}")

    speech_timestamps = json.loads(response.content)["speech_timestamps"]
    st.write(speech_timestamps)
