FROM python:latest

RUN python --version
RUN pip install -U pip

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

COPY ./app /app

RUN pip install --no-cache-dir -r /tmp/requirements.txt