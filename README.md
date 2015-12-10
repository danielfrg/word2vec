word2vec
========

[![travis-ci](https://api.travis-ci.org/danielfrg/word2vec.svg)](https://travis-ci.org/danielfrg/word2vec)
[![appveyor](https://ci.appveyor.com/api/projects/status/github/danielfrg/word2vec?branch=master&svg=true
)](https://ci.appveyor.com/project/danielfrg/word2vec)

Python interface to Google word2vec.

Training is done using the original C, other functionality is pure python + numpy.

## Installation

`pip install word2vec`

I recommend the [Anaconda python distribution](http://continuum.io/downloads)

**Note**: Only Linux and OS X are tested

**Windows:** Experimental support based on a [win32 port](https://github.com/zhangyafeikimi/word2vec-win32)

### Development

Clone the repo and `pip install -e .`

## Usage

The easiest way is to look at this example:
[word2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/word2vec.ipynb)

The default functionality from word2vec is also available from the command line as:
- word2vec
- word2phrase
- word2vec-distance
- word2vec-word-analogy
- word2vec-compute-accuracy

Experimental functionality on doc2vec can be found in this other example:
[doc2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/doc2vec.ipynb)

## Issues

Some people reported that they needed to do this if running OS X:
[http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue](http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue)
