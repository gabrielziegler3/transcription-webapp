# Transcription Web App

The project consists of a FastAPI server (`server.app`) and a frontend component with Python scripts (front-end) for various audio-related operations. It also utilizes AWS S3 for storing audio files and includes some external services such as VAD (Voice Activity Detection) and ASR (Automatic Speech Recognition).

# Getting Started

## Speech Models

### Voice Activity Detection

1. Download release from `https://github.com/snakers4/silero-vad/releases`
2. Unzip it to `backend/app/ml_models/vad`
3. Copy files from `files/` to `vad/`
4. Update `utils.py` from the VAD repo, if required.

### ASR speech-to-text

Any ASR model can be instantiated by implementing the class `ASR` from `backend/app/src/asr.py`

## Running locally

1. The project can be run locally using `Localstack` to simulate the creation of the AWS resources.

```
docker-compose up
```

2. Access `http://localhost:8501/` to see the website.

# License

This project is open-source and available under the MIT License. You are free to use, modify, and distribute it as per the terms of the license.
