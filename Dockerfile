FROM python:3.10.8-slim

USER root

RUN apt update && apt install -y make

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /toc-sinopac-python

COPY data /toc-sinopac-python/data
COPY logs /toc-sinopac-python/logs
COPY scripts /toc-sinopac-python/scripts
COPY src /toc-sinopac-python/src
COPY makefile /toc-sinopac-python/makefile

ENTRYPOINT ["/usr/bin/make"]
