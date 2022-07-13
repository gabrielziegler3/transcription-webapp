import io
import logging

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from src.logger import LogHandler
from src.asr import ASR
from src.audio_reader import AudioReader


log = logging.getLogger(__file__)
log.setLevel('DEBUG')
log.addHandler(LogHandler())
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


@app.post("/transcript")
async def transcript(file: UploadFile = File(...)):
    content = io.BytesIO(file.file.read())

    signal = audio_reader.read_audio(content)
    duration = audio_reader.duration
    transcription = asr_model.predict(signal)

    response = {
        "filename": file.filename,
        "duration": duration,
        "transcription": transcription
    }

    log.info(response)

    return response
