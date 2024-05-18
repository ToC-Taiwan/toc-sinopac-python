#!/bin/sh

if [ $# -eq 0 ]; then
  echo "No pip supplied"
  exit 1
fi

pip=$1

$pip freeze >requirements.txt &&
  $pip uninstall -y -r requirements.txt
rm -rf requirements.txt

$pip install --upgrade pip

$pip install -U \
  --no-warn-script-location \
  --no-cache-dir \
  toc-trade-pb-v2 \
  shioaji[speed] \
  grpcio \
  grpcio-tools \
  python-dotenv \
  numpy \
  schedule \
  paho-mqtt \
  requests \
  yfinance \
  prometheus-client

$pip freeze >requirements.txt

git add requirements.txt
