#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''SINOPAC PYTHON API FORWARDER'''
import os
import random
import string
import time

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
    exit(1)


server_token = ''.join(random.choice(string.ascii_letters) for _ in range(25))
logger.info('Server Token: %s', server_token)


for i in range(int(connection_count)):
    logger.info('Connection %d', i+1)
    Sinopac().login(person_id, password, ca_password)
    time.sleep(3)


serve(port=grpc_port)
