import os

from dotenv import load_dotenv


class RequiredEnv:  # pylint: disable=too-many-statements
    def __init__(self):
        # load .env file
        load_dotenv()
        self.mq_host = str(os.environ.get("MQ_HOST"))
        if self.mq_host is None:
            raise RuntimeError("Missing environment MQ_HOST")
        self.mq_port = int(str(os.environ.get("MQ_PORT")))
        if self.mq_port is None:
            raise RuntimeError("Missing environment MQ_PORT")

        self.log_format = os.environ.get("LOG_FORMAT")
        if self.log_format is None:
            raise RuntimeError("Missing environment LOG_FORMAT")

        self.grpc_port = str(os.environ.get("GRPC_PORT"))
        if self.grpc_port is None:
            raise RuntimeError("Missing environment GRPC_PORT")

        self.person_id = str(os.environ.get("PERSON_ID"))
        if self.person_id is None:
            raise RuntimeError("Missing environment PERSON_ID")

        self.api_key = str(os.environ.get("API_KEY"))
        if self.api_key is None:
            raise RuntimeError("Missing environment API_KEY")

        self.api_key_secret = str(os.environ.get("API_KEY_SECRET"))
        if self.api_key_secret is None:
            raise RuntimeError("Missing environment API_KEY_SECRET")

        self.ca_password = str(os.environ.get("CA_PASSWORD"))
        if self.ca_password is None:
            raise RuntimeError("Missing environment CA_PASSWORD")

        self.request_data_limit_per_second = int(str(os.environ.get("REQUEST_DATA_LIMIT_PER_SECOND")))
        if self.request_data_limit_per_second is None:
            raise RuntimeError("Missing environment REQUEST_DATA_LIMIT_PER_SECOND")

        self.request_portfolio_limit_per_second = int(str(os.environ.get("REQUEST_PORTFOLIO_LIMIT_PER_SECOND")))
        if self.request_portfolio_limit_per_second is None:
            raise RuntimeError("Missing environment REQUEST_PORTFOLIO_LIMIT_PER_SECOND")

        self.request_order_limit_per_second = int(str(os.environ.get("REQUEST_ORDER_LIMIT_PER_SECOND")))
        if self.request_order_limit_per_second is None:
            raise RuntimeError("Missing environment REQUEST_ORDER_LIMIT_PER_SECOND")

        self.connection_count = int(str(os.environ.get("CONNECTION_COUNT")))
        if self.connection_count is None:
            raise RuntimeError("Missing environment CONNECTION_COUNT")
        if self.connection_count <= 1:
            raise RuntimeError("CONNECTION_COUNT must be greater than 1")
        if self.connection_count > 5:
            raise RuntimeError("CONNECTION_COUNT must be less or equal to 5")
