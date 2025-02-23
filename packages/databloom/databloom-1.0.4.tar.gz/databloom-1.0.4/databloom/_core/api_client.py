import requests
from typing import Union

class ApiClient:
    """
    :param sdk_domain: sdk server domain
    """

    def __init__(self, api_domain: str, sdk_domain: str) -> None:
        self.sdk_domain = sdk_domain
        self.api_domain = api_domain
        pass

    def get_token(self, username: str, password: str) -> Union[str, None]:
        """
        get token from sdk server by username and password
        """
        try:
            response = requests.post(f"{self.api_domain}/oauth/token", json={"user": {"username": username, "password": password}, "grant_type": "password"})
            response.raise_for_status() 
           
            return response.json().get("access_token") 
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to get the token: {e}")
            return None        
        

    def get_source_credential(self, source_uuid: str, token: str) -> Union[dict, None]:
        """
        get source credential from sdk server by source uuid and token
        in progress
        """
        try:
            response = requests.get(f"{self.sdk_domain}/sources/{source_uuid}", headers={"Authorization": f"Bearer {token}"})
            print("check", source_uuid, response.json())
            if response == None or response.json() == None:
                return None
            response.raise_for_status() 
            return response.json().get("data").get("information")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to get the source credential: {e}")
            return None