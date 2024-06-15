FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/bot
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
