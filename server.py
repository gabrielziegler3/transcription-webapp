import json
import torchaudio
import torch
import io
import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from src.asr import ASR
from src.audio import AudioReader


app = FastAPI()
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
def transcript(file: UploadFile):
    content = io.BytesIO(file.file.read())
    print("CONTENT")
    print(content)

    signal = audio_reader.read_audio(content)
    transcription = asr_model.predict(signal)

    return {
        "name": file,
        "transcription": transcription
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
