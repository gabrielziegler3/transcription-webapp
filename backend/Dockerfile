FROM python:latest

RUN python --version

WORKDIR /backend

COPY . /backend

RUN pip install -r /backend/requirements.txt

CMD ["uvicorn", "server:app", "--reload"]