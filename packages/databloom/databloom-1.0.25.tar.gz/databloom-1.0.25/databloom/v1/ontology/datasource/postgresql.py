import databloom._dynamic.source.postgresql as db
from typing import Callable

class Postgres:
    """
    data source type is postgresql
    """
    def __init__(self, get_credential_from_sdk: Callable) -> None:
        ## ----render code block-----
        
        self.bumdata = db.bumdata(get_credential_from_sdk)
        
        self.marketing_source2 = db.marketing_source2(get_credential_from_sdk)
        
        self.sale_source = db.sale_source(get_credential_from_sdk)
        
        self.hainv4test2 = db.hainv4test2(get_credential_from_sdk)
        
        self.hainv4_source = db.hainv4_source(get_credential_from_sdk)
        
        self.neww222 = db.neww222(get_credential_from_sdk)
        
        self.chinhtt_marketing = db.chinhtt_marketing(get_credential_from_sdk)
        
        self.dep-1 = db.dep-1(get_credential_from_sdk)
        
        self.dep-2 = db.dep-2(get_credential_from_sdk)
        
        self.dep-3 = db.dep-3(get_credential_from_sdk)
        
        self.dep-4 = db.dep-4(get_credential_from_sdk)
        
        self.dep-5 = db.dep-5(get_credential_from_sdk)
        
        self.hainv4sourceabc = db.hainv4sourceabc(get_credential_from_sdk)
        
        ## ----render code block----
        pass