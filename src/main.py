#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''SINOPAC PYTHON API FORWARDER'''
import os
import sys
import typing

from dotenv import load_dotenv

from grpcsrv import serve
from logger import logger
from sinopac import Sinopac

load_dotenv()
person_id = os.environ.get("PERSON_ID")
password = os.environ.get("PASSWORD")
ca_password = os.environ.get("CA_PASSWORD")
grpc_port = os.environ.get("GRPC_PORT")
connection_count = os.environ.get("CONNECTION_COUNT")
if person_id is None or password is None or ca_password is None or grpc_port is None or connection_count is None:
    logger.error("Missing environment variables")
    sys.exit()


MAIN_WORKER: Sinopac
SINOPAC_WORKER_LIST: typing.List[Sinopac] = []

for i in range(int(connection_count)):
    logger.info('Establish Connection %d', i+1)
    is_first = bool(i == 0)
    tmp = Sinopac().login(person_id, password, ca_password, is_first)
    if is_first:
        MAIN_WORKER = tmp
    SINOPAC_WORKER_LIST.append(tmp)

serve(port=grpc_port, main_worker=MAIN_WORKER, workers=SINOPAC_WORKER_LIST)
