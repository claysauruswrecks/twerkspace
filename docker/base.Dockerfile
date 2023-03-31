FROM python:3-bullseye

ADD ./ /opt/twerkspace

WORKDIR /opt/twerkspace

RUN pip install -r ./requirements.txt
