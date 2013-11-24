word2vec
========

Python interface to Google word2vec

Installation
------------

`pip install word2vec`

Use [virtualenvs](http://www.virtualenv.org/en/latest/)!

Usage
-----

The default functionality from Google is available:
* word2vec
* word2phrase
* w2v-distance
* w2v-word-analogy
* w2v-compute-accuracy

### Examples

[word2vec](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/demo-word.ipynb)
[word clusters](http://nbviewer.ipython.org/urls/raw.github.com/danielfrg/word2vec/master/examples/demo-clusters.ipynb)

Issues
------

Some people reported that they needed to do this if running OS X:
[http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue](http://stackoverflow.com/questions/15590169/ld-library-not-found-for-lgfortran-mac-symlink-issue)

Development
-----------
If you want to use the scripts interface (for training models) in development and need to use using
`pip install -e` you need to change the make file, it has comments ;)


