FROM python:3.7-slim-buster

COPY ./devops/requirements.txt .

RUN apt-get update && \
    apt-get install gcc -y && \
    apt-get install python-dev -y && \
    apt-get install libpq-dev -y && \
    apt-get install postgresql-client -y &&\
    pip install -r requirements.txt && \
    apt-get purge gcc -y

WORKDIR /amp
ENV PYTHONPATH=$PYTHONPATH:/amp
