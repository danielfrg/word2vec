```
export VERSION=0.10.4

git commit --allow-empty -am "Release version: ${VERSION}"
git tag -a ${VERSION} -m "${VERSION}"

make build
make upload

git push origin ${VERSION}
git push
```
