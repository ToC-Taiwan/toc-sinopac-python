# TOC SINOPAC PYTHON

[![pipeline status](https://gitlab.tocraw.com/root/toc-sinopac-python/badges/main/pipeline.svg)](https://gitlab.tocraw.com/root/toc-sinopac-python/-/commits/main)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green)](https://gitlab.tocraw.com/root/toc-sinopac-python)
[![Python](https://img.shields.io/badge/Python-3.7.13-yellow?logo=python&logoColor=yellow)](https://python.org)
[![OS](https://img.shields.io/badge/OS-Linux-orange?logo=linux&logoColor=orange)](https://www.linux.org/)
[![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=blue)](https://www.docker.com/)

## Initialize

```sh
pip install --no-warn-script-location --no-cache-dir -U -r requirements.txt
```

### Needed dependency

- Reset all dependency

```sh
pip freeze > requirements.txt && \
pip uninstall -y -r requirements.txt
rm -rf requirements.txt
```

- Install

```sh
pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  shioaji \
  grpcio \
  grpcio-tools \
  mypy \
  mypy-protobuf \
  pylint-protobuf \
  pylint \
  python-dotenv \
  numpy \
  schedule
mypy --install-types --non-interactive ./src
pip freeze > requirements.txt
```

### Lint

```sh
mypy --install-types --non-interactive ./src && pylint ./src
```

### Run

```sh
echo 'DEPLOYMENT=dev
GRPC_PORT=56666
CONNECTION_COUNT=4

PERSON_ID=XXXXXXXXXX
PASSWORD=YYYYYYYYYY
CA_PASSWORD=ZZZZZZZZZZ' > ./.env
```

```sh
python -B -OO ./src/main.py
```

### Dev

```sh
find . -type d -name __pycache__ -exec rm -rf "{}" \;
```

### Git

```sh
git fetch --prune --prune-tags origin
git check-ignore *
```

## Authors

- [__Tim Hsu__](https://gitlab.tocraw.com/root)
