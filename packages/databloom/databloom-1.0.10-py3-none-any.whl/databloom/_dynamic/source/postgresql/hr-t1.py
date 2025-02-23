# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class hr-t1(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67ba908ff83cc8e6de00477b"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
