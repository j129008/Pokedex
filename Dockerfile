FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3 python3-pip mysql-client python3-dev build-essential libssl-dev libffi-dev \
    && apt-get purge -y --auto-remove

# install python modules
COPY requirements.txt /root/
RUN pip3 install -r /root/requirements.txt
