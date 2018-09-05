When you do `python setup.py install` or `pip install -e .` it will place the
binary files (`word2vec`, `word2phrase`, ...) in: `$(pwd)/bin`
so you have to export that to the `$PATH`.

When you do `pip install word2vec` it will place them in the correct
`{{ environtment }}/bin` directory so users dont need to do that.
