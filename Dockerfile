FROM ubuntu:latest

WORKDIR /usr/src/app

ADD pet_combiner Pipfile Pipfile.lock ./

RUN apt-get update -y

RUN apt-get install -y python3-pip curl
RUN python3 -m pip install pipenv

RUN python3 -m pipenv install

