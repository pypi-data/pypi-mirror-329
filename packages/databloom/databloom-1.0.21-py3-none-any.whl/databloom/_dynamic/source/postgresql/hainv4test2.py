# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class hainv4test2(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67bb1afdf83cc8e6de004780"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
