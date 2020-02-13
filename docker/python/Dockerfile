FROM ubuntu:18.04

WORKDIR /usr/src/wrp-server

RUN apt-get update && \
    apt-get -y install python3 python3-dev python3-pip libmysqlclient-dev apt-utils nano mc  && \
    ln -s /usr/bin/python3 /usr/bin/python


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/wrp-server/requirements.txt
RUN pip3 install -r /usr/src/wrp-server/requirements.txt


COPY ./ /usr/src/wrp-server