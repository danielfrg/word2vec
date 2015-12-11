word2vec
========

[![travis-ci](https://api.travis-ci.org/danielfrg/word2vec.svg)](https://travis-ci.org/danielfrg/word2vec)
[![appveyor](https://ci.appveyor.com/api/projects/status/github/danielfrg/word2vec?branch=master&svg=true
)](https://ci.appveyor.com/project/danielfrg/word2vec)

Python interface to Google word2vec.

Training is done using the original C, other functionality is pure python + numpy.

## Installation

I recommend the [Anaconda python distribution](http://continuum.io/downloads)

`pip install word2vec`

**Wheel**: Wheels packages for OS X and Windows are provided on Pypi on a
best effort sense. The code is quite easy to compile so consider using:
`--no-use-wheel` on Linux and OS X.

**Linux**: There is no wheel support for linux so you have to compile the
C code. The only requirement is `gcc`. You can override the compilation flags
if needed: `CFLAGS='-march=corei7' pip install word2vec`

**Windows:** Very experimental support based this [win32 port](https://github.com/zhangyafeikimi/word2vec-win32)

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
