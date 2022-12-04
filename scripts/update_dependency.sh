#!/bin/bash

pip freeze > requirements.txt && \
pip uninstall -y -r requirements.txt
rm -rf requirements.txt

pip install --upgrade pip

pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  shioaji \
  grpcio \
  grpcio-tools \
  python-dotenv \
  numpy \
  schedule \
  pika \
  requests \
  yfinance

pip freeze > requirements.txt

git add requirements.txt
