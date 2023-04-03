FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip3 install