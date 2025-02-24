# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class chinhtt_marketing(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67bc0bc6f1ba9a2bf4a678b7"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
