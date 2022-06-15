import json
import time
from base64 import b64encode

import docker
import requests


class RabbitMQContainer:
    def __init__(self):
        self.client = docker.from_env()

    def terminate_exist_rabbitmq(self):
        for c in self.client.containers.list():
            if c.name == "toc-rabbitmq":
                c.stop()

    def run_rabbitmq(self):
        self.terminate_exist_rabbitmq()

        docker_host = "172.20.10.96"
        self.client.containers.run(
            auto_remove=True,
            image="rabbitmq:3.10.5-management",
            name="toc-rabbitmq",
            environment={
                "RABBITMQ_DEFAULT_USER": "admin",
                "RABBITMQ_DEFAULT_PASS": "password",
            },
            detach=True,
            network_mode="host",
        )

        userAndPass = b64encode(b"admin:password").decode("ascii")
        headers = {
            "Authorization": f"Basic {userAndPass}",
            "Content-Type": "application/json",
        }

        while True:
            try:
                r = requests.get(
                    url=f"http://{docker_host}:15672/api/health/checks/alarms",
                    headers=headers,
                )
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                continue
            if r.status_code == 200:
                break

        r = requests.put(
            url=f"http://{docker_host}:15672/api/exchanges/%2F/toc",
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
