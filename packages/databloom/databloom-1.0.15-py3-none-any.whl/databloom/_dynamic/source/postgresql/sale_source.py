# --- render code block -----
from databloom._core.postgres_core import PostgresqlBase

class sale_source(PostgresqlBase):
    def __init__(self, get_credential_from_server) -> None:
        self.id = "67baf5f6f83cc8e6de00477f"
        self.credential = get_credential_from_server(self.id)
# --- render code block -----
