FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add --no-cache poppler-utils

COPY . .
