# TOC SINOPAC PYTHON

[![pipeline status](https://gitlab.tocraw.com/root/toc-sinopac-python/badges/main/pipeline.svg)](https://gitlab.tocraw.com/root/toc-sinopac-python/-/commits/main)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green)](https://gitlab.tocraw.com/root/toc-sinopac-python)
[![Python](https://img.shields.io/badge/Python-3.10.6-yellow?logo=python&logoColor=yellow)](https://python.org)
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

## Initialize

```sh
pip install --no-warn-script-location --no-cache-dir -U -r requirements.txt
```

## RabbitMQ

- @macOS

```sh
docker stop toc-rabbitmq
docker system prune --volumes -f

docker run -d \
  --restart always \
  --name toc-rabbitmq \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=password \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3.10.5-management

while ! nc -z 127.0.0.1 15672; do
  sleep 0.1 # wait for 1/10 of the second before check again
done

curl -i -u admin:password -H "content-type:application/json" \
  -XPUT -d'{"type":"direct","durable":true}' \
  http://127.0.0.1:15672/api/exchanges/%2F/toc

docker inspect bridge
```

### Run Local

```sh
echo 'DEPLOYMENT=prod
LOG_FORMAT=console
GRPC_PORT=56666
PERSON_ID=F127522501
PASSWORD=E2rgilaal
CA_PASSWORD=E2iairlol
REQUEST_LIMIT_PER_SECOND=50
RABBITMQ_HOST=172.20.10.226
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=password
RABBITMQ_EXCHANGE=toc
RABBITMQ_URL=amqp://admin:password@172.20.10.226:5672/%2f
CONNECTION_COUNT=5
'> ./.env
```

```sh
python -BOO ./src/main.py
```

## Authors

- [__Tim Hsu__](https://gitlab.tocraw.com/root)
