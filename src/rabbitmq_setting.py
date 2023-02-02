import json
import time
from base64 import b64encode

import requests

from env import RequiredEnv
from logger import logger

env = RequiredEnv()


class RabbitMQSetting:
    def reset_rabbitmq_exchange(self):
        auth = b64encode(
            bytes(
                f"{env.rabbitmq_user}:{env.rabbitmq_password}",
                encoding="utf8",
            )
        ).decode("ascii")
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        }

        while True:
            try:
                req = requests.get(
                    url=f"http://{env.rabbitmq_host}:15672/api/health/checks/alarms",
                    headers=headers,
                    timeout=(5, 10),
                )
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                continue
            if req.status_code == 200:
                break

        req = requests.get(
            url=f"http://{env.rabbitmq_host}:15672/api/exchanges",
            headers=headers,
            timeout=(5, 10),
        )
        if req.status_code != 200:
            raise RuntimeError("RabbitMQ get exchange fail")

        exchange_arr = req.json()
        exist = False
        for ex in exchange_arr:
            if ex["name"] == env.rabbitmq_exchange:
                exist = True
                logger.warning("exchange %s already exists", env.rabbitmq_exchange)
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
            req = requests.put(
                url=f"http://{env.rabbitmq_host}:15672/api/exchanges/%2F/{env.rabbitmq_exchange}",
                data=json.dumps(
                    {
                        "type": "direct",
                        "durable": True,
                    }
                ),
                headers=headers,
                timeout=(5, 10),
            )
            logger.warning("add exchange %s", env.rabbitmq_exchange)
            if req.status_code != 201:
                raise RuntimeError("RabbitMQ exchange add fail")
