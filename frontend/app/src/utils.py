import io
import logging
import json
import numpy as np
import httpx
import plotly.express as px
import streamlit as st

from src.logger import LogHandler


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"
SAMPLING_RATE = 16_000


def read_audio(file: io.BytesIO) -> np.ndarray:
    endpoint = SERVER_URL + "read_audio"

    payload = {"file": file}

    logger.info(f"Sending request with {file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
    )
    if response.status_code != 200:
        logger.info(f"Couldn't read audio. Received {response.status_code} status code")

    signal = json.loads(response.content)["signal"]
    audio = np.array(signal)

    logger.info(audio)
    logger.info(f"Audio with shape {audio.shape} read")

    return audio


def plot_waveform(audio: np.ndarray):
    x = np.arange(0, audio.flatten().shape()[0]) / SAMPLING_RATE
    y = audio.flatten()

    fig = px.line(x=x, y=y, title="Waveform")
    fig.update_xaxes(
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
    )
    st.plotly_chart(fig)
