FROM python:3.10.5

RUN apt update

WORKDIR /usr/src
RUN apt install -y cmake
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV ACCESS_TOKEN=""
ENV PYTHONPATH="${PYTHONPATH}:/usr/src"

