FROM registry.gitlab.com/ulrichschreiner/base/debian:buster-slim

ARG RXV=v0.7.0rc2

RUN apt -y update \
    && apt -y install python3-pip \
    && pip3 install rxv==$RXV bottle

ENV RX600=http://RXS600/YamahaRemoteControl/ctrl

RUN mkdir /app
ADD app.py /app/app.py

ENTRYPOINT ["/app/app.py"]
