#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''SINOPAC PYTHON API FORWARDER'''
import random
import string

import srv.grpc as grpcsrv
from sinopac.sinopac import Sinopac

server_token = ''.join(random.choice(string.ascii_letters) for _ in range(25))
sino = Sinopac()

sino.login()
sino.list_accounts()

grpcsrv.serve()
