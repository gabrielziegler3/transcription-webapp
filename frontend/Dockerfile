FROM node:latest

WORKDIR /frontend/transcription_webapp

USER root

ENV NODE_OPTIONS=--openssl-legacy-provider

COPY . /frontend

RUN npm --version

RUN npm install axios

CMD [ "npm", "start" ]
