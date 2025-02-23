import databloom._dynamic.source.postgresql as db
from typing import Callable

class Postgres:
    """
    data source type is postgresql
    """
    def __init__(self, get_credential_from_sdk: Callable) -> None:
        ## ----render code block-----
        
        self.bumdata = db.bumdata(get_credential_from_sdk)
        
        self.marketing_source = db.marketing_source(get_credential_from_sdk)
        
        self.hr-t1 = db.hr-t1(get_credential_from_sdk)
        
        self.finance-t1 = db.finance-t1(get_credential_from_sdk)
        
        self.report-c-level = db.report-c-level(get_credential_from_sdk)
        
        ## ----render code block----
        pass