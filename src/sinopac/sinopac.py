import threading

import shioaji as sj

from utils.logger import logger


class Sinopac:
    def __init__(self):
        self.api = sj.Shioaji()
        self.login_lock = threading.Lock()
        self.login_status = 0

    def login(self):
        self.api.login(
            person_id="F127522501",
            passwd="@A2rgilaal",
            contracts_cb=self.login_cb,
        )
        while True:
            if self.login_status == 100:
                break
        self.api.activate_ca(
            ca_path='./ca-sinopac.pfx',
            ca_passwd="~A2iairlol",
            person_id="F127522501",
        )

    def login_cb(self, security_type: sj.constant.SecurityType):
        with self.login_lock:
            if security_type.value in ('STK', 'IND', 'FUT', 'OPT'):
                self.login_status += 25
                logger.warning('login progress: %d%%, %s', self.login_status, security_type)

    def list_accounts(self):
        accounts = self.api.list_accounts()
        # print(accounts)
        # print(self.api.stock_account)
        # print(self.api.futopt_account)
        # return accounts
        logger.info(accounts)
