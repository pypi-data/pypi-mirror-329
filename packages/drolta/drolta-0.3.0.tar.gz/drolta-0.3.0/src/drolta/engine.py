"""Drolta Query Engine."""

from __future__ import annotations

import sqlite3

from drolta.ast import generate_ast
from drolta.data import EngineData
from drolta.db import SQLiteDatabase
from drolta.interpreter import DroltaResult, QueryInterpreter, ScriptInterpreter


class QueryEngine:
    """
    A QueryEngine manages user-defined content and handles queries to SQLite.
    """

    __slots__ = ("_data",)

    _data: EngineData

    def __init__(self) -> None:
        self._data = EngineData()

    def execute_script(self, drolta_script: str) -> None:
        """Load rules and aliases from a Drolta script.

        Parameters
        ----------
        drolta_script : str
            Drolta script text containing rule and alias definitions.
        """

        drolta_ast = generate_ast(drolta_script)
        interpreter = ScriptInterpreter(self._data)
        interpreter.visit(drolta_ast)

    def query(self, drolta_query: str, conn: sqlite3.Connection) -> DroltaResult:
        """Query the SQLite database and return a cursor to the results.

        Parameters
        ----------
        drolta_query : str
            Text defining a Drolta query.
        conn: sqlite3.Connection
            A sqlite3 Connection object.

        Returns
        -------
        DroltaResult
            The result of the query.
        """

        drolta_ast = generate_ast(drolta_query)
        interpreter = QueryInterpreter(SQLiteDatabase(conn), self._data)
        interpreter.visit(drolta_ast)

        return interpreter.result
