# word2vec

[![PyPI](https://badge.fury.io/py/word2vec.svg)](https://pypi.org/project/word2vec/)
[![Testing](http://github.com/danielfrg/word2vec/workflows/test/badge.svg)](http://github.com/danielfrg/word2vec/actions)
[![Coverage Status](https://codecov.io/gh/danielfrg/word2vec/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/word2vec?branch=master)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://github.com/danielfrg/word2vec/blob/master/LICENSE.txt)

Python interface to Google word2vec.

Training is done using the original C code, other functionality is pure Python with numpy.

## Installation

```
pip install word2vec
```

The installation requires to compile the original C code:

### Compilation

In order to compile the original C code a `gcc` compiler is needed.

You can override the compilation flags if needed:

```
WORD2VEC_CFLAGS='-march=corei7' pip install word2vec
```

**Windows:** There is basic some support for this support based on this [win32 port](https://github.com/zhangyafeikimi/word2vec-win32).

## Usage

Example notebook: [word2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/word2vec.ipynb)

The default functionality from word2vec is available from the command line:
- `word2vec`
- `word2phrase`
- `word2vec-distance`
- `word2vec-word-analogy`
- `word2vec-compute-accuracy`

Experimental functionality on doc2vec can be found in this other example:
[doc2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/doc2vec.ipynb)
