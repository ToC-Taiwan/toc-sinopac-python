# TOC SINOPAC PYTHON

[![Workflow](https://github.com/ToC-Taiwan/toc-sinopac-python/actions/workflows/main.yml/badge.svg)](https://github.com/ToC-Taiwan/toc-sinopac-python/actions/workflows/main.yml)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green)](https://github.com/ToC-Taiwan/toc-sinopac-python)
[![Python](https://img.shields.io/badge/Python-3.10.9-yellow?logo=python&logoColor=yellow)](https://python.org)
[![OS](https://img.shields.io/badge/OS-Linux-orange?logo=linux&logoColor=orange)](https://www.linux.org/)
[![Container](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=blue)](https://www.docker.com/)

## .env

```sh
# fill in .env
cp .env.example .env
```

### Make

- show help

```sh
make help
```

- initial

```sh
make install
```

- run

```sh
make
```

- update dependencies

```sh
make update
```

## Development on Apple Silicon

- Install Rosetta
- Create a Rosetta terminal
- Install x86 homebrew in the Rosetta terminal
- Install x86 Python in the Rosetta terminal
  - python should be installed in `/usr/local/bin/python3`

### vscode setting

- add x86 terminal to options
- path: `.vscode/settings.json`

```json
{
    "terminal.integrated.profiles.osx": {
        "x86 zsh": {
            "path": "/usr/bin/arch",
            "args": [
                "-arch",
                "x86_64",
                "/bin/zsh"
            ]
        }
    },
    "terminal.integrated.defaultProfile.osx": "x86 zsh"
}
```

### setup venv

```sh
eval "$(/usr/local/bin/brew shellenv)"
. ./scripts/start_venv.sh
```

## Local RabbitMQ

```sh
docker stop toc-rabbitmq
docker system prune --volumes -f
docker rmi -f $(docker images -a -q)

docker run -d \
  --restart always \
  --name toc-rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=password \
  rabbitmq:3.11.5-management
```

## Authors

- [**Tim Hsu**](https://github.com/Chindada)
