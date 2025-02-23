"""Drolta SQLite Database Wrappers.

The way that Drolta wraps database instances is adapted from Pandas.

References:
- https://github.com/pandas-dev/pandas/blob/main/pandas/io/sql.py
"""

import sqlite3
from contextlib import contextmanager
from typing import Any, Optional


class SQLiteDatabase:
    """Manages a sqlite database connection."""

    __slots__ = ("conn",)

    conn: sqlite3.Connection
    """The connection to the database."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        super().__init__()
        self.conn = conn

    @contextmanager
    def run_transaction(self):
        """Execute a transaction on the database."""

        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def execute(self, sql: str, params: Optional[tuple[Any, ...]] = None) -> None:
        """Execute an operation on the database.

        Parameters
        ----------
        sql: str
            A SQL expression.
        params: tuple of Any, optional
            Parameters to pass to the SQL expression.
        """
        with self.run_transaction() as cur:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
