from flask import Blueprint, request, jsonify

from api.app.db.pool import get_conn, put_conn
from api.app.repos.server_repo import DuplicateHostnameError, InvalidIPAddressError, InvalidStateError, NotFoundError, RepoError
from api.app.services.server_service import create_server_service, delete_server_service, get_server_service, list_servers_service, update_server_service



servers_bp = Blueprint("servers", __name__)

@servers_bp.route('/servers', methods=['POST'])
def create_server():
    payload = request.get_json(force=True)
    conn = get_conn()
    try:
        result = create_server_service(conn, payload)
        return jsonify(result), 201
    except DuplicateHostnameError as e:
        return jsonify({"error": str(e)}), 409
    except InvalidIPAddressError as e:
        return jsonify({"error": str(e)}), 400
    except InvalidStateError as e:
        return jsonify({"error": str(e)}), 400
    except RepoError as e:
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
def update_server(id: int):
    payload = request.get_json(force=True)
    conn = get_conn()
    try:
        result = update_server_service(conn, id, payload)
        return jsonify(result), 200
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except DuplicateHostnameError as e:
        return jsonify({"error": str(e)}), 409
    except InvalidIPAddressError as e:
        return jsonify({"error": str(e)}), 400
    except InvalidStateError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        put_conn(conn)


@servers_bp.route('/servers/<int:id>', methods=['DELETE'])
def delete_server(id: int):
    conn = get_conn()
    try:
        delete_server_service(conn, id)
        return "", 204
    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        put_conn(conn)

