import io
import logging
import torch

from typing import List, Union
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.logger import LogHandler
from src.asr import ASR
from src.audio_reader import AudioReader


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
app = FastAPI(debug=True)
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


asr_model = ASR()
# audio_reader = AudioReader()


@app.get("/")
def home():
    return {
        "Hello": "World",
        "date": datetime.now().strftime("%Y%m%d %H:%M:%S")
    }


def parse_audio_file(file: UploadFile) -> Union[torch.Tensor, None]:
    audio_reader = AudioReader()
    content = io.BytesIO(file.file.read())
    logger.info(f"Preparing to read content: {content}")
    signal = audio_reader.read_audio(content)
    return signal


@app.post("/read_audio")
def read_audio(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /read_audio")

    signal = parse_audio_file(file)

    response = {
        "signal": signal.numpy().tolist(),
    }

    return response


@app.post("/transcript")
def transcript(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /transcript")

    signal = parse_audio_file(file)

    transcription = asr_model.predict(signal.squeeze(0))

    response = {
        "transcription": transcription
    }

    logger.info(response)

    return response

