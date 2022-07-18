FROM python:latest

RUN python --version
RUN pip install -U pip

WORKDIR /backend

COPY . /backend

RUN pip install -r /backend/requirements.txt

# CMD ["uvicorn", "server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
