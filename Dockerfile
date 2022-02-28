# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /riffable

COPY requirements.txt requirements.txt

RUN apt-get update
RUN apt-get --yes install libsndfile1
RUN apt-get install --yes git
RUN apt-get install --yes ffmpeg
RUN apt-get install --yes lilypond

RUN pip3 install youtube-dl
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "views.py"]