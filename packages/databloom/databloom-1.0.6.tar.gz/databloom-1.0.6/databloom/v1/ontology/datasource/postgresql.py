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
        
        self.marketing_source = db.marketing_source(get_credential_from_sdk)
        
        self.marketing_2 = db.marketing_2(get_credential_from_sdk)
        
        ## ----render code block----
        pass