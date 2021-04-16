# word2vec

[![pypi](https://badge.fury.io/py/word2vec.svg)](https://pypi.org/project/word2vec/)
[![build](https://github.com/danielfrg/word2vec/workflows/test/badge.svg)](http://github.com/danielfrg/word2vec/actions/workflows/test.yml)
[![coverage](https://codecov.io/gh/danielfrg/word2vec/branch/master/graph/badge.svg)](https://codecov.io/gh/danielfrg/word2vec?branch=master)
[![license](https://img.shields.io/:license-Apache%202-blue.svg)](http://github.com/danielfrg/word2vec/blob/master/LICENSE.txt)

Python interface to Google word2vec.

Training is done using the original C code, other functionality is pure Python with numpy.

## Installation

```
pip install word2vec
```

### Compilation

The installation requires to compile the original C code using `gcc`.

You can override the compilation flags if needed:

```
WORD2VEC_CFLAGS='-march=corei7' pip install word2vec
```

**Windows:** There is basic some support for this support based on this [win32 port](https://github.com/zhangyafeikimi/word2vec-win32).

## Usage

Example notebook: [word2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/word2vec.ipynb)

The default functionality from word2vec is available with the following commands:
- `word2vec`
- `word2phrase`
- `word2vec-distance`
- `word2vec-word-analogy`
- `word2vec-compute-accuracy`

Experimental functionality on doc2vec can be found in this example:
[doc2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/doc2vec.ipynb)
