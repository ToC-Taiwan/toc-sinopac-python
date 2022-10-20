# TOC SINOPAC PYTHON

![workflow](https://github.com/ToC-Taiwan/toc-sinopac-python/actions/workflows/main.yml/badge.svg)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green)](https://github.com/ToC-Taiwan/toc-sinopac-python)
[![Python](https://img.shields.io/badge/Python-3.10.6-yellow?logo=python&logoColor=yellow)](https://python.org)
[![OS](https://img.shields.io/badge/OS-Linux-orange?logo=linux&logoColor=orange)](https://www.linux.org/)
[![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=blue)](https://www.docker.com/)

## Reference

- Schedule restart at 08:20, 14:40 every day

## Initialize

```sh
pip install --no-warn-script-location --no-cache-dir -U -r requirements.txt
```

## RabbitMQ for development

- For macOS

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

## .env example

```sh
echo 'LOG_FORMAT=console
GRPC_PORT=56666
PERSON_ID=F127522501
PASSWORD=EEE2rgilaal
CA_PASSWORD=EEE2iairlol
REQUEST_LIMIT_PER_SECOND=50
RABBITMQ_HOST=172.17.0.3
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=password
RABBITMQ_EXCHANGE=toc
RABBITMQ_URL=amqp://admin:password@172.17.0.3:5672/%2f
CONNECTION_COUNT=5
'> ./.env
```

### RUN

```sh
python -BOO ./src/main.py
```

## Authors

- [__Tim Hsu__](https://github.com/Chindada)
