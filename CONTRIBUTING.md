# Contributing

## Development environment

Create Python env

```
make env
conda activate word2vec
```

Install package for development

```
make develop
```

When you do `python setup.py develop` or `pip install -e .` the binary files
binary files (`word2vec`, `word2phrase`, ...) will be placed under: `$(pwd)/bin`
so you have to export that to the `$PATH` for development.

```
export PATH=$(PWD)/bin:$PATH
```

## Tests

Download test data

```
make test-data
```

Run tests

```
make test
```

Check linting and format

```
make check
make fmt
```

### Docker (for Linux)

```
make docker-img
make docker-run

# Inside the container
conda activate word2vec
make develop
make test
```
