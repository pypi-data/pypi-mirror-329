# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class marketing_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67b75ace938bda1ece86f30c"
        self.credential = get_credential_from_server(self.id) or None
# --- render code block -----
