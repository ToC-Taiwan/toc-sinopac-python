import os

from dotenv import load_dotenv

# load .env file
load_dotenv()


class RequiredEnv:  # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.log_format = os.environ.get("LOG_FORMAT")
        if self.log_format is None:
            raise Exception("Missing environment LOG_FORMAT")

        self.grpc_port = os.environ.get("GRPC_PORT")
        if self.grpc_port is None:
            raise Exception("Missing environment GRPC_PORT")

        self.person_id = str(os.environ.get("PERSON_ID"))
        if self.person_id is None:
            raise Exception("Missing environment PERSON_ID")

        self.api_key = str(os.environ.get("API_KEY"))
        if self.api_key is None:
            raise Exception("Missing environment API_KEY")

        self.api_key_secret = str(os.environ.get("API_KEY_SECRET"))
        if self.api_key_secret is None:
            raise Exception("Missing environment API_KEY_SECRET")

        self.ca_password = str(os.environ.get("CA_PASSWORD"))
        if self.ca_password is None:
            raise Exception("Missing environment CA_PASSWORD")

        self.request_limit_per_second = int(
            str(os.environ.get("REQUEST_LIMIT_PER_SECOND"))
        )
        if self.request_limit_per_second is None:
            raise Exception("Missing environment REQUEST_LIMIT_PER_SECOND")

        self.rabbitmq_host = os.environ.get("RABBITMQ_HOST")
        if self.rabbitmq_host is None:
            raise Exception("Missing environment RABBITMQ_HOST")

        self.rabbitmq_user = os.environ.get("RABBITMQ_USER")
        if self.rabbitmq_user is None:
            raise Exception("Missing environment RABBITMQ_USER")

        self.rabbitmq_password = os.environ.get("RABBITMQ_PASSWORD")
        if self.rabbitmq_password is None:
            raise Exception("Missing environment RABBITMQ_PASSWORD")

        self.rabbitmq_exchange = os.environ.get("RABBITMQ_EXCHANGE")
        if self.rabbitmq_exchange is None:
            raise Exception("Missing environment RABBITMQ_EXCHANGE")

        self.rabbitmq_url = os.environ.get("RABBITMQ_URL")
        if self.rabbitmq_url is None:
            raise Exception("Missing environment RABBITMQ_URL")

        self.connection_count = int(str(os.environ.get("CONNECTION_COUNT")))
        if self.connection_count is None:
            raise Exception("Missing environment CONNECTION_COUNT")
        if self.connection_count <= 1:
            raise Exception("CONNECTION_COUNT must be greater than 1")
        if self.connection_count > 5:
            raise Exception("CONNECTION_COUNT must be less or equal to 5")
