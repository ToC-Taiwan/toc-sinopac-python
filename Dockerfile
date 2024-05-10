FROM python:3.11.9-slim

USER root

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /toc-sinopac-python

COPY data /toc-sinopac-python/data
COPY logs /toc-sinopac-python/logs
COPY scripts /toc-sinopac-python/scripts
COPY src /toc-sinopac-python/src

ENV SJ_LOG_PATH=/toc-sinopac-python/logs/shioaji.log
ENV SJ_CONTRACTS_PATH=/toc-sinopac-python/data

ENTRYPOINT ["/toc-sinopac-python/scripts/docker-entrypoint.sh"]
