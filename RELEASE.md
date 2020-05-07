# How to release a new version

- Update `CHANGELOG.md`
- Update `README.md` and docs

```
export VERSION=1.0.0
git commit -am "Release ${VERSION}" --allow-empty
git tag -a ${VERSION} -m "${VERSION}"
git push origin ${VERSION}
git push
```

```
make clean
make build
make upload-pypi

# Upload to test PyPI
make upload-test
```
