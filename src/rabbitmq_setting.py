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
                r = requests.get(
                    url=f"http://{env.rabbitmq_host}:15672/api/health/checks/alarms",
                    headers=headers,
                )
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                continue
            if r.status_code == 200:
                break

        r = requests.get(
            url=f"http://{env.rabbitmq_host}:15672/api/exchanges",
            headers=headers,
        )
        if r.status_code != 200:
            raise Exception("RabbitMQ get exchange fail")

        exchange_arr = r.json()
        for ex in exchange_arr:
            if ex["name"] == env.rabbitmq_exchange:
                logger.warning("Delete exchange %s", ex["name"])
                r = requests.delete(
                    url=f"http://{env.rabbitmq_host}:15672/api/exchanges/%2F/{env.rabbitmq_exchange}",
                    headers=headers,
                )
                if r.status_code != 201:
                    raise Exception("RabbitMQ container start fail")
                break

        r = requests.put(
            url=f"http://{env.rabbitmq_host}:15672/api/exchanges/%2F/{env.rabbitmq_exchange}",
            data=json.dumps(
                {
                    "type": "direct",
                    "durable": True,
                }
            ),
            headers=headers,
        )
        if r.status_code != 201:
            raise Exception("RabbitMQ container start fail")
