word2vec
========

Python interface to Google word2vec.

Training is done using the original C code plus some patches, the other funcionality is pure python + numpy.

## Installation

`pip install word2vec`

I highly recommend the use the [Anaconda python distribution](http://continuum.io/downloads)

## Usage

The easiest way is to look at this example:
[word2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/word2vec.ipynb)

The default functionality from word2vec is also available from the command line as:
- word2vec
- word2phrase
- w2v-distance
- w2v-word-analogy
- w2v-compute-accuracy

## Issues

Some people reported that they needed to do this if running OS X:
[http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue](http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue)
