# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class hainv4sourceabc(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67bc29daf1ba9a2bf4a678bf"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
