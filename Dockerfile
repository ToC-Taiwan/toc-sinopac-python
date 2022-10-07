FROM python:3.10.6-alpine

USER root

WORKDIR /toc-sinopac-python
ENV PYTHONPATH=/toc-sinopac-python/pb

COPY requirements.txt ./
RUN pip install --no-warn-script-location --no-cache-dir -r requirements.txt

COPY src /toc-sinopac-python
COPY pb /toc-sinopac-python
COPY scripts /toc-sinopac-python

# RUN apt update -y && \
#     apt install -y tzdata && \
#     apt autoremove -y && \
#     apt clean && \
#     rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/toc-sinopac-python/scripts/docker-entrypoint.sh"]
