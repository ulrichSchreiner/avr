FROM registry.gitlab.com/ulrichschreiner/base/debian:buster-slim

RUN apt -y update \
    && apt -y install python-pip \
    && pip install rxv bottle

ENV RX600=http://RXS600/YamahaRemoteControl/ctrl

RUN mkdir /app
ADD app.py /app/app.py

ENTRYPOINT ["/app/app.py"]
