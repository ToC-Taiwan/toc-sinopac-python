import os

from dotenv import load_dotenv

# load .env file
load_dotenv()


class RequiredEnv:  # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.log_format = os.environ.get("LOG_FORMAT")
        self.grpc_port = os.environ.get("GRPC_PORT")
        self.person_id = os.environ.get("PERSON_ID")
        self.password = os.environ.get("PASSWORD")
        self.ca_password = os.environ.get("CA_PASSWORD")
        self.request_limit_per_second = int(
            str(os.environ.get("REQUEST_LIMIT_PER_SECOND"))
        )
        self.rabbitmq_host = os.environ.get("RABBITMQ_HOST")
        self.rabbitmq_user = os.environ.get("RABBITMQ_USER")
        self.rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")
        self.rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE")
        self.rabbitmq_url = os.environ.get("RABBITMQ_URL")
        self.connection_count = int(str(os.environ.get("CONNECTION_COUNT")))

        if self.log_format is None:
            raise Exception("Missing environment LOG_FORMAT")
        if self.grpc_port is None:
            raise Exception("Missing environment GRPC_PORT")
        if self.person_id is None:
            raise Exception("Missing environment PERSON_ID")
        if self.password is None:
            raise Exception("Missing environment PASSWORD")
        if self.ca_password is None:
            raise Exception("Missing environment CA_PASSWORD")
        if self.request_limit_per_second is None:
            raise Exception("Missing environment REQUEST_LIMIT_PER_SECOND")
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
