from __future__ import annotations

from typing import Any, Dict, List, Tuple

from psycopg2 import errors


class RepoError(Exception):
    pass

class NotFoundError(RepoError):
    pass

class DuplicateHostnameError(RepoError):
    pass

class InvalidStateError(RepoError):
    pass

class InvalidIPAddressError(RepoError):
    pass


def _row_to_server(row: Tuple[Any, ...]) -> Dict[str, Any]:
    return {
        "id": row[0],
        "hostname": row[1],
        "ip_address": row[2],
        "state": row[3],
    }


def create_server(conn, hostname: str, ip_address: str, state: str) -> Dict[str, Any]:
    """
    Insert one server. Relies on DB constraints for:
      - UNIQUE(hostname)
      - CHECK(state in ...)
      - ip_address as inet (if using inet)
    """
    sql = """
        INSERT INTO servers (hostname, ip_address, state)
        VALUES (%s, %s::inet, %s)
        RETURNING id, hostname, ip_address::text, state;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (hostname, ip_address, state))
            row = cur.fetchone()
        conn.commit()
        return _row_to_server(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise DuplicateHostnameError("hostname must be unique")
    except errors.CheckViolation:
        conn.rollback()
        raise InvalidStateError("invalid state")
    except errors.InvalidTextRepresentation:
        conn.rollback()
        raise InvalidIPAddressError("invalid ip_address")
    except Exception as e:
        conn.rollback()
        raise RepoError(str(e))


def list_servers(conn) -> List[Dict[str, Any]]:
    sql = """
        SELECT id, hostname, ip_address::text, state
        FROM servers
        ORDER BY id;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [_row_to_server(r) for r in rows]


def get_server(conn, server_id: int) -> Dict[str, Any]:
    sql = """
        SELECT id, hostname, ip_address::text, state
        FROM servers
        WHERE id = %s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (server_id,))
        row = cur.fetchone()
    if row is None:
        raise NotFoundError(f"server {server_id} not found")
    return _row_to_server(row)


def update_server(conn, server_id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Partial update (works for PUT/PATCH semantics).
    `fields` can contain: hostname, ip_address, state.
    """
    allowed = {"hostname", "ip_address", "state"}
    bad = set(fields.keys()) - allowed
    if bad:
        raise RepoError(f"unknown fields: {sorted(bad)}")

    if not fields:
        return get_server(conn, server_id)

    set_clauses = []
    params: List[Any] = []

    if "hostname" in fields and fields["hostname"] is not None:
        set_clauses.append("hostname = %s")
        params.append(fields["hostname"])

    if "ip_address" in fields and fields["ip_address"] is not None:
        set_clauses.append("ip_address = %s::inet")
        params.append(fields["ip_address"])

    if "state" in fields and fields["state"] is not None:
        set_clauses.append("state = %s")
        params.append(fields["state"])

    set_clauses.append("updated_at = NOW()")

    sql = f"""
        UPDATE servers
        SET {", ".join(set_clauses)}
        WHERE id = %s
        RETURNING id, hostname, ip_address::text, state;
    """
    params.append(server_id)

    try:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
        if row is None:
            conn.rollback()
            raise NotFoundError(f"server {server_id} not found")
        conn.commit()
        return _row_to_server(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise DuplicateHostnameError("hostname must be unique")
    except errors.CheckViolation:
        conn.rollback()
        raise InvalidStateError("invalid state")
    except errors.InvalidTextRepresentation:
        conn.rollback()
        raise InvalidIPAddressError("invalid ip_address")
    except Exception as e:
        conn.rollback()
        raise RepoError(str(e))


def delete_server(conn, server_id: int) -> None:
    sql = "DELETE FROM servers WHERE id = %s;"
    with conn.cursor() as cur:
        cur.execute(sql, (server_id,))
        deleted = cur.rowcount
    if deleted == 0:
        conn.rollback()
        raise NotFoundError(f"server {server_id} not found")
    conn.commit()
