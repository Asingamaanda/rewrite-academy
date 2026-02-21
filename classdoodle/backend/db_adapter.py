"""
db_adapter.py
─────────────
Unified database adapter.

  • DATABASE_URL set   → psycopg2 + ThreadedConnectionPool (PostgreSQL on Render)
  • DATABASE_URL unset → sqlite3, fresh connection per call   (local dev)

All calling code uses:
  conn = get_connection()
  result = qexec(conn, sql, params)   # returns a _Result
  row  = result.fetchone()            # dict or None
  rows = result.fetchall()            # list of dicts
  conn.commit()
  release_connection(conn)

Or the convenience helpers fetchone() / fetchall() for read-only one-liners.
"""

import os
import threading

DATABASE_URL = os.environ.get('DATABASE_URL', '')
POSTGRES     = bool(DATABASE_URL)
PH           = '%s' if POSTGRES else '?'          # parameterised placeholder
SERIAL_PK    = 'BIGSERIAL PRIMARY KEY' if POSTGRES else 'INTEGER PRIMARY KEY AUTOINCREMENT'

# ── PostgreSQL connection pool (lazy init) ────────────────────────────────────
_pool      = None
_pool_lock = threading.Lock()


def _ensure_pool():
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                import psycopg2.pool
                url = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
                _pool = psycopg2.pool.ThreadedConnectionPool(1, 10, url)
    return _pool


# ── Public connection helpers ─────────────────────────────────────────────────

def get_connection():
    """Return a live database connection."""
    if POSTGRES:
        return _ensure_pool().getconn()
    import sqlite3
    from pathlib import Path
    db_path = Path(__file__).parent.parent / 'data' / 'classdoodle.db'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def release_connection(conn):
    """Return a pg connection to the pool, or close a sqlite connection."""
    if POSTGRES:
        _ensure_pool().putconn(conn)
    else:
        conn.close()


# ── Internal cursor factory ───────────────────────────────────────────────────

def _make_cursor(conn):
    if POSTGRES:
        import psycopg2.extras
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn.cursor()


# ── Result wrapper ────────────────────────────────────────────────────────────

class _Result:
    """
    Pre-fetches all rows so the connection can be released before the caller
    reads results.  Supports fetchone() / fetchall() like a real cursor.
    """
    def __init__(self, rows):
        self._rows = [dict(r) for r in (rows or [])]
        self._idx  = 0

    def fetchone(self):
        if self._idx < len(self._rows):
            row = self._rows[self._idx]
            self._idx += 1
            return row
        return None

    def fetchall(self):
        rows = self._rows[self._idx:]
        self._idx = len(self._rows)
        return rows

    def __iter__(self):
        return iter(self._rows[self._idx:])

    def __len__(self):
        return len(self._rows)


# ── Core execute helper ───────────────────────────────────────────────────────

def qexec(conn, sql, params=None):
    """
    Execute SQL on *conn* (no commit).
    Returns a _Result whose rows are pre-fetched and safe to read after
    release_connection() is called.
    """
    cur = _make_cursor(conn)
    cur.execute(sql, params or ())
    try:
        rows = cur.fetchall()
    except Exception:
        rows = []
    return _Result(rows)


# ── Read-only convenience helpers ─────────────────────────────────────────────

def fetchone(conn, sql, params=None):
    """Execute and return one row as a plain dict, or None."""
    return qexec(conn, sql, params).fetchone()


def fetchall(conn, sql, params=None):
    """Execute and return all rows as plain dicts."""
    return qexec(conn, sql, params).fetchall()
