import os

from dotenv import load_dotenv

# load .env file
load_dotenv()


class RequiredEnv:
    def __init__(self):

        self.deployment = os.environ.get("DEPLOYMENT")
        self.grpc_port = os.environ.get("GRPC_PORT")
        self.person_id = os.environ.get("PERSON_ID")
        self.password = os.environ.get("PASSWORD")
        self.ca_password = os.environ.get("CA_PASSWORD")

        self.rabbitmq_host = os.environ.get("RABBITMQ_HOST")
        self.rabbitmq_user = os.environ.get("RABBITMQ_USER")
        self.rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")
        self.rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE")
        self.rabbitmq_url = os.environ.get("RABBITMQ_URL")
        self.connection_count = os.environ.get("CONNECTION_COUNT")

        if self.deployment is None:
            raise Exception("Missing environment DEPLOYMENT")
        if self.grpc_port is None:
            raise Exception("Missing environment GRPC_PORT")
        if self.person_id is None:
            raise Exception("Missing environment PERSON_ID")
        if self.password is None:
            raise Exception("Missing environment PASSWORD")
        if self.ca_password is None:
            raise Exception("Missing environment CA_PASSWORD")
        if self.rabbitmq_host is None:
            raise Exception("Missing environment RABBITMQ_HOST")
        if self.rabbitmq_user is None:
            raise Exception("Missing environment RABBITMQ_USER")
        if self.rabbitmq_password is None:
            raise Exception("Missing environment RABBITMQ_PASSWORD")
        if self.rabbitmq_exchange is None:
            raise Exception("Missing environment RABBITMQ_EXCHANGE")
        if self.rabbitmq_url is None:
            raise Exception("Missing environment RABBITMQ_URL")
        if self.connection_count is None:
            raise Exception("Missing environment CONNECTION_COUNT")
