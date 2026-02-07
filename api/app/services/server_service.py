

from api.app.models.server import ServerCreate, ServerOut
from api.app.repos.server_repo import create_server_repo, get_server_repo, list_servers_repo

class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def create_server_service(conn, payload):
    data = ServerCreate.model_validate(payload)
    row = create_server_repo(conn, data.hostname, str(data.ip_address), data.state.value)
    return ServerOut(**row).model_dump()

def list_servers_service(conn):
    rows = list_servers_repo(conn)
    return [ServerOut(**row).model_dump() for row in rows]

def get_server_service(conn, id):
    row = get_server_repo(conn, id)
    return ServerOut(**row).model_dump() 