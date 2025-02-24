# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class hainv4_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67bbe01cf1ba9a2bf4a678b0"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
