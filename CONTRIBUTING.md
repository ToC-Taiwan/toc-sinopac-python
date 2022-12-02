# Contributing

## Tools

### Conventional Commit

- install git cz tool global

```sh
npm install -g commitizen
npm install -g cz-conventional-changelog
npm install -g conventional-changelog-cli
echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc
```

### Pre-commit

- install git pre-commit tool global

```sh
pip install --no-warn-script-location --no-cache-dir pre-commit
```

- install/modify from config .pre-commit-config.yaml

```sh
pre-commit autoupdate
pre-commit install
```

- dry run pre-commit

```sh
pre-commit run --all-files
```

### Modify CHANGELOG

- First Time

```sh
conventional-changelog -p angular -i CHANGELOG.md -s -r 0
```

- From Last semver tag

```sh
conventional-changelog -p angular -i CHANGELOG.md -s
```

### Find ignored files

```sh
find . -type f  | git check-ignore --stdin
```
