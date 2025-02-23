# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class marketing_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67ba24caf83cc8e6de004779"
        self.credential = get_credential_from_server(self.id) or None
# --- render code block -----
