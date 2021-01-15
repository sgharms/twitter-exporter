FROM python:3.8.3-buster

RUN  mkdir -p /opt /workarea

COPY ./requirements.txt /opt

RUN python3.8 -m pip install -r /opt/requirements.txt

WORKDIR /workarea
