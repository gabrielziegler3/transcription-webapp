FROM python:latest

RUN python --version

RUN pip install -U pip

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

RUN pip install -r /tmp/requirements.txt

RUN pip install torch==1.11.0 torchaudio==0.11.0

RUN pip install pydantic==1.9.1 \
                transformers==4.19.2 \
                huggingface-hub==0.7.0 \
                pyctcdecode==0.3.0

RUN pip freeze

# CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
