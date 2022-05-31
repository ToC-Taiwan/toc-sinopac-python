import os

from dotenv import load_dotenv

# load .env file
load_dotenv()


class RequiredEnv:
    def __init__(self):

        self.deployment = os.environ.get("DEPLOYMENT")
        self.person_id = os.environ.get("PERSON_ID")
        self.password = os.environ.get("PASSWORD")
        self.ca_password = os.environ.get("CA_PASSWORD")
        self.grpc_port = os.environ.get("GRPC_PORT")
        self.connection_count = os.environ.get("CONNECTION_COUNT")

        if self.deployment is None:
            raise Exception("Missing environment DEPLOYMENT")
        if self.person_id is None:
            raise Exception("Missing environment PERSON_ID")
        if self.password is None:
            raise Exception("Missing environment PASSWORD")
        if self.ca_password is None:
            raise Exception("Missing environment CA_PASSWORD")
        if self.grpc_port is None:
            raise Exception("Missing environment GRPC_PORT")
        if self.connection_count is None:
            raise Exception("Missing environment CONNECTION_COUNT")
