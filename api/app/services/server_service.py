

from api.app.models.server import ServerCreate, ServerOut
from api.app.repos.server_repo import create_server

class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def create_server_service(conn, payload):
    data = ServerCreate.model_validate(payload)
    row = create_server(conn, data.hostname, str(data.ip_address), data.state.value)
    return ServerOut(**row).model_dump()