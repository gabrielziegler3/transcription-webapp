FROM python:latest

RUN python --version
RUN pip install -U pip

WORKDIR /frontend

COPY . /frontend

RUN pip install -r /frontend/requirements.txt
