import databloom._dynamic.source.postgresql as db
from typing import Callable

class Postgres:
    """
    data source type is postgresql
    """
    def __init__(self, get_credential_from_sdk: Callable) -> None:
        ## ----render code block-----
        
        self.report-c-level = db.report-c-level(get_credential_from_sdk)
        
        self.bumdata = db.bumdata(get_credential_from_sdk)
        
        self.hr-t1 = db.hr-t1(get_credential_from_sdk)
        
        self.finance-t1 = db.finance-t1(get_credential_from_sdk)
        
        self.marketing_source2 = db.marketing_source2(get_credential_from_sdk)
        
        ## ----render code block----
        pass