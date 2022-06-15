import json
import socket
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

        container_host = "172.20.10.227"
        container = self.client.containers.create(
            auto_remove=True,
            image="rabbitmq:3.10.5-management",
            name="toc-rabbitmq",
            environment={
                "RABBITMQ_DEFAULT_USER": "admin",
                "RABBITMQ_DEFAULT_PASS": "password",
            },
            detach=True,
        )

        network = self.client.networks.get("tocvlan")
        if network is None:
            raise Exception("network not found")

        network.connect(container, ipv4_address=container_host)
        container.start()

        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = (container_host, 15672)
        result_of_check = a_socket.connect_ex(location)
        while True:
            if result_of_check == 0:
                a_socket.close()
                break
            time.sleep(1)

        url = f"http://{container_host}:15672/api/exchanges/%2F/toc"
        body = {
            "type": "direct",
            "durable": True,
        }
        userAndPass = b64encode(b"admin:password").decode("ascii")
        headers = {
            "Authorization": f"Basic {userAndPass}",
            "Content-Type": "application/json",
        }
        r = requests.put(url=url, data=json.dumps(body), headers=headers)
        if r.status_code != 201:
            raise Exception("RabbitMQ container start fail")
