# How to release a new version

## Upload to test PyPI

```
export VERSION=1.0.0
git checkout -b release-${VERSION}

git commit -am "Release ${VERSION}.rc2" --allow-empty
git tag ${VERSION}.rc2

make cleanall
make build
make upload-test

# Create venv and install rc version
pip install --extra-index-url=https://test.pypi.org/simple word2vec==${VERSION}rc2

# Delete rc tag
git tag -d ${VERSION}.rc2
```

Merge branch when CI passes

## Upload to PyPI

- Update `CHANGELOG.md`
- Update `README.md` and docs as needed

```
export VERSION=1.0.0

git commit -am "Release ${VERSION}" --allow-empty
git tag ${VERSION}

make build
make upload-pypi
git push origin ${VERSION}
git push
```
