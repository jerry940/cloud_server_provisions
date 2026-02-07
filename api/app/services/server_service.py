

from api.app.models.server import ServerCreate, ServerOut, ServerUpdate
from api.app.repos.server_repo import create_server_repo, delete_server_repo, get_server_repo, list_servers_repo, update_server_repo


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

def update_server_service(conn, id, payload):
    data = ServerUpdate.model_validate(payload)
    row = update_server_repo(conn, id, data.hostname, str(data.ip_address), data.state.value)
    return ServerOut(**row).model_dump() 

def delete_server_service(conn, id):
    delete_server_repo(conn, id)
