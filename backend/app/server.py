import io
import logging
import torch

from typing import List, Union
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.logger import LogHandler
from src.asr import ASR
from src.vad.model import VAD
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


# asr_model = ASR()
vad = VAD()
audio_reader = AudioReader()


@app.get("/")
def home():
    return {
        "date": datetime.now().strftime("%Y%m%d %H:%M:%S")
    }


def parse_audio_file(file: UploadFile) -> Union[torch.Tensor, None]:
    content = io.BytesIO(file.file.read())
    logger.info(f"Preparing to read content: {content}")
    signal = audio_reader.read_audio(content)
    return signal


@app.post("/read_audio")
async def read_audio(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /read_audio")

    signal = parse_audio_file(file)

    response = {
        "signal": signal.numpy().tolist(),
    }

    return response


@app.post("/get_speech_timestamps")
async def get_speech_timestamps(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /get_speech_timestamps")
    signal = parse_audio_file(file)

    speech_timestamps = vad.predict(signal)

    response = {
        "speech_timestamps": speech_timestamps,
    }

    return response


@app.post("/transcript")
async def transcript(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /transcript")

    signal = parse_audio_file(file)

    # transcription = asr_model.predict(signal.squeeze(0))
    transcription = "hello world"

    response = {
        "transcription": transcription
    }

    logger.info(response)

    return response
