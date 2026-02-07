from flask import Blueprint, request, jsonify

from api.app.db.pool import get_conn, put_conn
from api.app.repos.server_repo import NotFoundError
from api.app.services.server_service import create_server_service, ValidationError, get_server_service, list_servers_service



servers_bp = Blueprint("servers", __name__)

@servers_bp.route('/servers', methods=['POST'])
def create_server():
    payload = request.json(force=True)
    conn = get_conn()
    try:
        result = create_server_service(conn, payload)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        put_conn(conn)

@servers_bp.route('/servers', methods=['GET'])
def list_servers():
    conn = get_conn()
    try:
        result = list_servers_service(conn)
        return jsonify(result), 200
    finally:
        put_conn(conn)


@servers_bp.route('/servers/<int:id>', methods=['GET'])
def get_server(id: int):
    conn = get_conn()
    try:
        result = get_server_service(conn, id)
        return jsonify(result), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        put_conn(conn)


@servers_bp.route('/servers/<int:id>', methods=['PUT'])
def update_server():
    pass


@servers_bp.route('/servers/<int:id>', methods=['DELETE'])
def delete_server():
    pass

