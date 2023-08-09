import logging
import streamlit as st
import json
import asyncio

from src.logger import LogHandler
from src.utils import read_audio, plot_waveform
from src.async_client import server_client


logger = logging.getLogger(__file__)
# logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"


async def transcription():
    endpoint = SERVER_URL + "transcript"

    st.title('Transcription')

    uploaded_file = st.file_uploader("Choose a file")

    logger.info(f"Uploaded file type {type(uploaded_file)}")

    if not uploaded_file:
        return

    audio = read_audio(uploaded_file)
    plot_waveform(audio)

    payload = {"file": uploaded_file}

    logger.info(f"Sending request with {uploaded_file} to {endpoint}")

    response = await server_client.post(
        url=endpoint,
        files=payload,
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error attempting transcription API")
        return

    transc = json.loads(response.text)["transcription"]
    logger.info(f"Transcription: {transc}")
    st.write(transc)


if __name__ == "__main__":
    asyncio.run(transcription())
