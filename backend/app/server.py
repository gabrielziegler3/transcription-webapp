import io
import logging
import torch
import os
import boto3

from botocore.client import Config
from typing import Union
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.logger import LogHandler
# from src.asr import ASR
from src.vad.model import VAD
from src.audio_reader import AudioReader


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
app = FastAPI(debug=True)
origins = ["*"]


# Connect to MinIO
s3 = boto3.resource('s3',
                    endpoint_url='http://minio:9000',
                    aws_access_key_id='minio',
                    aws_secret_access_key='minio123',
                    region_name='us-east-1')


# Create bucket if is doesn't exist
if s3.Bucket('audios') not in s3.buckets.all():
    s3.create_bucket(Bucket='audios')
    logger.debug("Bucket 'audios' created successfully.")
else:
    logger.warning("Bucket 'audios' already exists. Skipping bucket creation.")


bucket = s3.Bucket('audios')


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


@app.post("/upload_file")
def upload_file(file: UploadFile = File(...)):
    try:
        logger.debug(f"Received file {file.filename} at /upload_file")
        bucket.upload_fileobj(file.file, file.filename)
        logger.debug("File inserted to bucket 'audios'")

        return {"message": "File uploaded successfully"}
    except Exception as e:
        logger.warning(f"Failed to upload file {file.filename} to bucket 'audios' {e}")
        return {"message": "File upload failed"}


def parse_audio_file(file: UploadFile) -> Union[torch.Tensor, None]:
    try:
        content = io.BytesIO(file.file.read())
        logger.info(f"Preparing to read content: {content}")
        signal = audio_reader.read_audio(content)
        return signal
    except Exception as e:
        logger.warning(f"Failed to parse audio file: {file.filename}")
        # logger.warning(e, exc_info=True)
        raise HTTPException(
            status_code=400, 
            detail="Failed to parse audio file. Please make sure the file is a valid audio file."
        )


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
