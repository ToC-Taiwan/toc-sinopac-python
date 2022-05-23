#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''SINOPAC PYTHON API FORWARDER'''
import os
import random
import string
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


server_token = ''.join(random.choice(string.ascii_letters) for _ in range(50))
logger.info('Server Token: %s', server_token)

MAIN_WORKER: Sinopac
SINOPAC_WORKDER_LIST: typing.List[Sinopac] = []

for i in range(int(connection_count)):
    logger.info('New Connection %d', i+1)
    is_first = bool(i == 0)
    tmp = Sinopac().login(person_id, password, ca_password, is_first)
    if is_first:
        MAIN_WORKER = tmp
    SINOPAC_WORKDER_LIST.append(tmp)

serve(port=grpc_port, main_connection=MAIN_WORKER, workers=SINOPAC_WORKDER_LIST)
