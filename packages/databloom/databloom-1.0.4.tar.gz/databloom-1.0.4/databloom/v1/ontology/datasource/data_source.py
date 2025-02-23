import os
from .mysql import Mysql
from .postgresql import Postgres
from databloom._core import ApiClient 

class Datasource:
    """
    Datasource is responsible for accessing data from your source
    """
    def __init__(self):
        self.api_client = ApiClient(os.environ.get("API_SERVER_DOMAIN"), os.environ.get("SDK_SERVER_DOMAIN"))       
        self.mysql = Mysql(self.__get_credential_from_sdk)
        self.postgres = Postgres(self.__get_credential_from_sdk)
        pass    

    def __get_credential_from_sdk(self, source_uuid: str) -> dict:
        """
        get credential from sdk server by source uuid and token
        """
        token = self.api_client.get_token(os.environ.get("SDK_SERVER_USERNAME"), os.environ.get("SDK_SERVER_PASSWORD"))

        credential = self.api_client.get_source_credential(source_uuid, token)

        return credential