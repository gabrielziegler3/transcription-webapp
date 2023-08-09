import streamlit as st
import logging
import httpx

from src.logger import LogHandler


logger = logging.getLogger(__file__)
# logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
SERVER_URL = "http://host.docker.internal:80/"


def upload_file():
    st.title('File Upload')
    endpoint = SERVER_URL + "upload_file"

    uploaded_file = st.file_uploader("Choose a file")

    if not uploaded_file:
        return

    payload = {
        "file": uploaded_file
    }

    logger.info(f"Sending request with {uploaded_file} to {endpoint}")
    response = httpx.post(
        url=endpoint,
        files=payload,
    )

    if response.status_code != 200:
        logger.warn(f"Status {response.status_code} received. Error on upload")
        return


    st.write(response.content)


if __name__ == "__main__":
    upload_file()
