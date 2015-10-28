FROM continuumio/miniconda

RUN apt-get update && apt-get install -y git build-essential libatlas-base-dev

RUN /opt/conda/bin/conda install ipython numpy pytest -y

VOLUME /word2vec
WORKDIR /word2vec
