FROM python:3.10.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir
COPY . ./
