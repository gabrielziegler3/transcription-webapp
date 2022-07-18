import io
import logging

from typing import List
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.logger import LogHandler
from src.asr import ASR
from src.audio_reader import AudioReader


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


asr_model = ASR()
audio_reader = AudioReader()


@app.get("/")
def home():
    return {
        "Hello": "World",
        "date": datetime.now().strftime("%Y%m%d %H:%M:%S")
    }


@app.post("/read_audio")
async def read_audio(file: UploadFile = File(...)) -> List[List[int]]:
    logger.info(f"Received {file.filename} at /read_audio")

    content = io.BytesIO(file.file.read())

    signal = audio_reader.read_audio(content).numpy()

    response = {
        "signal": signal.tolist(),
    }
    logger.info(f"Audio shape: {signal.shape}")

    return response


@app.post("/transcript")
async def transcript(file: UploadFile = File(...)):
    logger.info(f"Received {file.filename} at /transcript")

    content = io.BytesIO(file.file.read())

    signal = audio_reader.read_audio(content)
    duration = audio_reader.duration
    transcription = asr_model.predict(signal)

    response = {
        "filename": file.filename,
        "duration": duration,
        "transcription": transcription
    }

    logger.info(response)

    return response
