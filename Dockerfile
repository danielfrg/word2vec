FROM conda/miniconda2

RUN apt-get update && apt-get install -y git build-essential libatlas-base-dev

RUN conda install -y -q ipython numpy cython pytest

VOLUME /word2vec
WORKDIR /word2vec
