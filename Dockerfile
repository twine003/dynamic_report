# pull official base image
FROM python:3.9.9-slim-buster

# set work directory
WORKDIR /usr/src/workindir

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    python3-gdal \
    gcc \
    musl-dev \
    libpq-dev \
    bash \
    git \
    libpango1.0-dev \
    libcairo2-dev \
    nodejs npm \
 && pip install psycopg2

# install fonts
RUN apt-get install -y \
    fontconfig \
    fonts-dejavu

RUN apt-get install -y netcat

# copy project
COPY . /usr/src/workindir/

# install dependencies
RUN pip install --upgrade pip

