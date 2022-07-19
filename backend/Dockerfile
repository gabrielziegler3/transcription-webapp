FROM python:latest

ENV TERM xterm-256color

RUN python --version

RUN pip install -U pip

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

COPY . /backend

RUN pip install -r /backend/requirements.txt

RUN pip install torch==1.11.0 torchaudio==0.11.0

RUN pip install pydantic==1.9.1 \
                transformers==4.19.2 \
                huggingface-hub==0.7.0 \
                pyctcdecode==0.3.0

# CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
