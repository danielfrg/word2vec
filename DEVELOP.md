# Development

Create dev environment

```
# Create conda env
make env
conda activate word2vec

pip install -e .
```

When you do `python setup.py install` or `pip install -e .` it will place the
binary files (`word2vec`, `word2phrase`, ...) in: `$(pwd)/bin`
so you have to export that to the `$PATH`.

With `pip install word2vec` it will place them in the correct
`{{ sys.prefix }}/bin` directory so users don't need to do that.

## Testing

```
make test
```
