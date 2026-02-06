from flask import Blueprint, request, jsonify



servers_bp = Blueprint("servers", __name__)

@servers_bp.route('/servers', methods=['POST'])
def create_server():
    pass


@servers_bp.route('/servers', methods=['GET'])
def list_servers():
    pass


@servers_bp.route('/servers/{id}', methods=['GET'])
def get_server():
    pass


@servers_bp.route('/servers/{id}', methods=['PUT'])
def update_server():
    pass


@servers_bp.route('/servers/{id}', methods=['DELETE'])
def delete_server():
    pass

