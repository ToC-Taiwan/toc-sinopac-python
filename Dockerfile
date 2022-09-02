FROM python:3.10.6-bullseye
USER root

ENV TZ=Asia/Taipei

WORKDIR /
RUN mkdir toc-sinopac-python
WORKDIR /toc-sinopac-python
COPY . .

ENV PYTHONPATH=/toc-sinopac-python/pb

RUN apt update -y && \
    apt install -y tzdata && \
    apt autoremove -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-warn-script-location --no-cache-dir -r requirements.txt

ENTRYPOINT ["/toc-sinopac-python/scripts/docker-entrypoint.sh"]
