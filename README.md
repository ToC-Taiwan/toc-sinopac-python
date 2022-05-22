# TOC SINOPAC PYTHON

## Initialize

```sh
pip install --no-warn-script-location --no-cache-dir -U -r requirements.txt
```

### Reset all dependency

```sh
pip freeze > requirements.txt && \
pip uninstall -y -r requirements.txt
rm -rf requirements.txt
```

```sh
pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  autopep8 \
  shioaji \
  grpcio \
  grpcio-tools \
  mypy \
  mypy-protobuf \
  pylint-protobuf \
  pylint \
  python-dotenv
pip freeze > requirements.txt
```

- lint

```sh
mypy --install-types --non-interactive ./src
pylint ./src
```

- env file template

```env
GRPC_PORT=56666
CONNECTION_COUNT=2

PERSON_ID=F127522501
PASSWORD=@A2rgilaal
CA_PASSWORD=~A2iairlol
```

```sh
python ./src/main.py
```

### Delete __pycache__

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
