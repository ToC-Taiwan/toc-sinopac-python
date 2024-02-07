import json
import time
from base64 import b64encode

import requests

from logger import logger


class RabbitAPI:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        exchange: str,
    ):
        self._username = username
        self._password = password
        self._host = host
        self._exchange = exchange

    def reset_rabbitmq_exchange(self):
        auth = b64encode(
            bytes(
                f"{self._username}:{self._password}",
                encoding="utf8",
            )
        ).decode("ascii")
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        }

        while True:
            try:
                resp = requests.get(
                    url=f"http://{self._host}:15672/api/health/checks/alarms",
                    headers=headers,
                    timeout=(5, 10),
                )
            except requests.exceptions.ConnectionError:
                logger.warning("RabbitMQ connection fail, retry after 1 second")
                time.sleep(1)
                continue
            if resp.status_code == 200:
                break

        resp = requests.get(
            url=f"http://{self._host}:15672/api/exchanges",
            headers=headers,
            timeout=(5, 10),
        )
        if resp.status_code != 200:
            raise RuntimeError("RabbitMQ get exchange fail")

        exchange_arr = resp.json()
        exist = False
        for exchange in exchange_arr:
            if exchange["name"] == self._exchange:
                exist = True
                logger.info("exchange %s already exists", self._exchange)
                # logger.warning("delete exchange %s", ex["name"])
                # r = requests.delete(
                #     url=f"http://{env.rabbitmq_host}:15672/api/exchanges/%2F/{env.rabbitmq_exchange}",
                #     headers=headers,
                #     timeout=(5, 10),
                # )
                # if r.status_code != 204:
                #     raise Exception("RabbitMQ exchange delete fail")
                break

        if not exist:
            resp = requests.put(
                url=f"http://{self._host}:15672/api/exchanges/%2F/{self._exchange}",
                data=json.dumps(
                    {
                        "type": "direct",
                        "durable": True,
                    }
                ),
                headers=headers,
                timeout=(5, 10),
            )
            logger.info("add exchange %s", self._exchange)
            if resp.status_code != 201:
                raise RuntimeError("RabbitMQ exchange add fail")
