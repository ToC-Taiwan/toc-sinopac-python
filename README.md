# TOC SINOPAC PYTHON

[![pipeline status](https://gitlab.tocraw.com/root/toc-sinopac-python/badges/main/pipeline.svg)](https://gitlab.tocraw.com/root/toc-sinopac-python/-/commits/main)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green)](https://gitlab.tocraw.com/root/toc-sinopac-python)
[![Python](https://img.shields.io/badge/Python-3.10.5-yellow?logo=python&logoColor=yellow)](https://python.org)
[![OS](https://img.shields.io/badge/OS-Linux-orange?logo=linux&logoColor=orange)](https://www.linux.org/)
[![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=blue)](https://www.docker.com/)

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

- install/modify from config

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

### Needed dependency

- Reset all dependency

```sh
pip freeze > requirements.txt && \
pip uninstall -y -r requirements.txt
rm -rf requirements.txt
```

- Install prod

```sh
pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  shioaji \
  grpcio \
  grpcio-tools \
  python-dotenv \
  numpy \
  schedule \
  pika
pip freeze > requirements.txt
```

- dev

```sh
pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  pre-commit \
  mypy-protobuf \
  pylint-protobuf \
  black \
  mypy \
  pylint
mypy --install-types --non-interactive ./src
pre-commit install
```

## Initialize

```sh
pip install --no-warn-script-location --no-cache-dir -U -r requirements.txt
```

### Run

```sh
echo 'DEPLOYMENT=prod
GRPC_PORT=56666
CONNECTION_COUNT=5
PERSON_ID=XXXXXXXXXX
PASSWORD=YYYYYYYYYY
CA_PASSWORD=ZZZZZZZZZZ
RABBITMQ_EXCHANGE=exchange
RABBITMQ_URL=amqp://guest:guest@localhost:5672/'> ./.env
```

```sh
python -BOO ./src/main.py
```

## Authors

- [__Tim Hsu__](https://gitlab.tocraw.com/root)
