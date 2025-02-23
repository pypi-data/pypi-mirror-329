# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class marketing_2(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67ba8e9df83cc8e6de00477a"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
