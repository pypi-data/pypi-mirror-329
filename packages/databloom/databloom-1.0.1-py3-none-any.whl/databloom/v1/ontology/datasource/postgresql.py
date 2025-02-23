import databloom._dynamic.source.postgresql as db
from typing import Callable

class Postgres:
    """
    data source type is postgresql
    """
    def __init__(self, get_credential_from_sdk: Callable) -> None:
        ## ----render code block-----
        
        self.databum = db.databum(get_credential_from_sdk)
        
        self.databummmm = db.databummmm(get_credential_from_sdk)
        
        self.bumdata = db.bumdata(get_credential_from_sdk)
        
        ## ----render code block----
        pass