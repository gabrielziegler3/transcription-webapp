import io

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from src.asr import ASR
from src.audio_reader import AudioReader


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


@app.post("/upload_file")
async def create_upload_file(file: UploadFile):
    # TODO
    return {
        "name": file.filename,
    }


@app.get("/list_files")
async def list_files():
    # TODO
    return {
        "date": datetime.now().strftime("%Y%m%d %H:%M:%S")
    }


@app.post("/transcript")
async def transcript(file: UploadFile = File(...)):
    content = io.BytesIO(file.file.read())

    signal = audio_reader.read_audio(content)
    duration = audio_reader.duration
    transcription = asr_model.predict(signal)

    response = {
        "duration": duration,
        "transcription": transcription
    }

    print(response)

    return response
