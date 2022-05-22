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
  pylint
pip freeze > requirements.txt
```

```sh
mypy --install-types --non-interactive ./src/main.py
```

```sh
python ./src/main.py
```

```sh
find . -type d -name __pycache__ -exec rm -rf "{}" \;
```

- install protoc

```sh
version=3.20.0
version=3.20.1
rm -rf /utils
mkdir /utils
cd /utils
curl -fSL https://github.com/protocolbuffers/protobuf/releases/download/v$version/protoc-$version-linux-x86_64.zip --output protobuf.zip
unzip protobuf.zip -d protobuf
cd /sinopac_mq_srv
```

### Git

```sh
git fetch --prune --prune-tags origin
git check-ignore *
```

## Authors

- [**Tim Hsu**](https://gitlab.tocraw.com/root)
