"""Drolta Interpreter."""

from __future__ import annotations

import logging
import sqlite3
from typing import Any, Generator, Iterable, Optional, cast

import attrs
import sqlparse

from drolta.ast import (
    ASTVisitor,
    DeclareAliasExpression,
    DeclareRuleExpression,
    ExpressionNode,
    ExpressionType,
    NotPredicateExpression,
    PredicateExpression,
    ProgramNode,
    QueryExpression,
    is_filter_expression,
)
from drolta.data import EngineData, ResultVariable, RuleData
from drolta.db import SQLiteDatabase
from drolta.errors import ProgrammingError

_logger = logging.getLogger(__name__)


def get_execution_order(node: ExpressionNode) -> int:
    """Get the order number of the expression (Lower is higher priority)."""
    expression_type = node.get_expression_type()

    if expression_type == ExpressionType.PREDICATE_CALL:
        return 0

    if is_filter_expression(node):
        return 1

    if expression_type == ExpressionType.PREDICATE_NOT:
        return 1

    return 2


def cycle_check_dfs(
    aliases: dict[str, str], value: str, visited: set[str], stack: list[str]
) -> tuple[bool, str]:
    """Perform Depth-First Search to check for cycles."""

    if value not in visited:
        visited.add(value)
        stack.append(value)

        if value in aliases:
            target = aliases[value]

            if target not in visited:
                result = cycle_check_dfs(aliases, target, visited, stack)
                if result[0] is True:
                    return result

            if target in stack:
                return True, target

    stack.pop()
    return False, ""


def has_alias_cycle(aliases: dict[str, str]) -> tuple[bool, str]:
    """Check if the alias dictionary has a cycle."""

    stack: list[str] = []
    visited: set[str] = set()

    for alias in aliases.keys():
        if alias not in visited:
            result = cycle_check_dfs(aliases, alias, visited, stack)
            if result[0] is True:
                return result

    return False, ""


def sqlite_dtype_to_py(d_type: str) -> str:
    """Convert SQLite data type name to python type name."""

    if d_type == "INT":
        return "int"
    elif d_type == "TEXT":
        return "str"
    elif d_type == "REAL":
        return "float"

    return "object"


@attrs.define(frozen=True, slots=True)
class TempResult:
    """Information about an intermediate result of a query."""

    table_name: str
    """The name of the temporary table with this result's data"""
    output_vars: set[str]
    """The column names of the temp table"""

    @staticmethod
    def get_common_vars(b: TempResult, a: TempResult) -> list[str]:
        """Get common variables between two temp results."""
        return sorted(a.output_vars.intersection(b.output_vars))


@attrs.define(frozen=True, slots=True)
class ColumnInfo:
    """Information about a column in a table."""

    name: str
    """The name of the column."""
    d_type: str
    """The data type (int | str)."""


class DroltaResult:
    """The result of a Drolta Query.

    This class wraps a sqlite3 Cursor object to ensure that all temporary
    tables are removed at the start of a new query.
    """

    __slots__ = ("_column_info", "_has_read_data", "_cursor", "_db", "_result_table")

    _column_info: list[ColumnInfo]
    _has_read_data: bool
    _result_table: TempResult
    _db: SQLiteDatabase
    _cursor: Optional[sqlite3.Cursor]

    def __init__(
        self,
        columns: list[ColumnInfo],
        db: SQLiteDatabase,
        result_table: TempResult,
        cursor: Optional[sqlite3.Cursor] = None,
    ) -> None:
        self._column_info = [*columns]
        self._has_read_data = False
        self._cursor = cursor
        self._db = db
        self._result_table = result_table

    @property
    def description(self) -> Iterable[ColumnInfo]:
        """Get information about the columns in the result."""
        return [*self._column_info]

    def fetch_all(self) -> list[Any]:
        """Get all results from the last query."""

        if self._has_read_data:
            raise RuntimeError("Data already fetched from this result.")

        self._has_read_data = True

        if self._cursor is None:
            return []

        result = self._cursor.fetchall()

        self.destroy()

        return result

    def fetch_chunks(self, size: int) -> Generator[list[Any], Any, None]:
        """Fetch the next batch of results."""

        if self._has_read_data:
            raise RuntimeError("Data already fetched from this result.")

        self._has_read_data = True

        if self._cursor is None:
            yield []
            return

        next_batch = self._cursor.fetchmany(size)

        while next_batch:
            yield next_batch
            next_batch = self._cursor.fetchmany(size)

        self.destroy()

    def destroy(self):
        """Destroy this result, freeing resources."""
        if self._cursor:
            self._cursor.close()
            self._db.execute(f"DROP TABLE IF EXISTS {self._result_table.table_name};")
            self._cursor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
        self.destroy()


class FormattedSqlString:
    """Represents a SQL string."""

    __slots__ = ("raw_sql",)

    raw_sql: str

    def __init__(self, raw_sql: str) -> None:
        self.raw_sql = raw_sql

    def __str__(self) -> str:
        return sqlparse.format(self.raw_sql, reindent=True, keyword_case="upper")  # type: ignore


@attrs.define(slots=True)
class Scope:
    """Information about the current variable scope of the query."""

    scope_id: int
    """The ID of the current scope."""
    output_vars: list[ResultVariable] = attrs.field(factory=list)
    """Variables output by this scope."""
    tables: list[TempResult] = attrs.field(factory=list)
    """Temporary result tables."""
    next_table_id: int = 1
    """The ID assigned to the next table in this scope."""


SUPPORTED_AGGREGATES = ("COUNT", "MAX", "MIN", "AVG", "SUM")
"""Aggregate functions supported by Drolta."""


class ScriptInterpreter(ASTVisitor):
    """Interpreter used for scripts."""

    __slots__ = ("engine_data",)

    engine_data: EngineData
    """State data for the query engine."""

    def __init__(self, engine_data: EngineData) -> None:
        super().__init__()
        self.engine_data = engine_data

    def visit_program(self, node: ProgramNode):
        for child in node.children:
            self.visit(child)

    def visit_declare_alias(self, node: DeclareAliasExpression):
        new_alias_dict = {**self.engine_data.aliases, node.alias: node.original_name}

        has_cycle, cycled_alias = has_alias_cycle(new_alias_dict)

        if has_cycle:
            raise ProgrammingError(f"Circular aliases for: {cycled_alias}.")

        self.engine_data.aliases[node.alias] = node.original_name

        _logger.debug("Declared alias: %s -> %s", node.alias, node.original_name)

    def visit_declare_rule(self, node: DeclareRuleExpression):
        result_vars: list[ResultVariable] = []
        for entry in node.result_vars:
            result_vars.append(
                ResultVariable(
                    var_name=entry.var_name,
                    aggregate_name=entry.aggregate_name,
                    alias=entry.alias,
                )
            )

        rule = RuleData(
            name=node.name,
            result_vars=result_vars,
            where_expressions=[*node.where_expressions],
            group_by=node.group_by,
            order_by=node.order_by,
            limit=node.limit,
        )

        self.engine_data.rules[rule.name] = rule

        _logger.debug("Declared rule: %s", rule.name)

    def visit_query(self, node: QueryExpression):
        raise ProgrammingError("Queries not allowed while executing scripts.")


_next_query_id: int = 0
"""Gives each query a unique ID to prevent table name clashes."""


class QueryInterpreter(ASTVisitor):
    """Interpreter used for queries."""

    TEMP_TABLE_PREFIX = "temp__"
    """Name prefix for all temporary tables created by the query engine."""

    __slots__ = ("db", "engine_data", "scope_stack", "result")

    db: SQLiteDatabase
    """Database connection."""
    engine_data: EngineData
    """State data for the query engine."""
    scope_stack: list[Scope]
    """Stack of scopes used during query evaluation."""
    result: DroltaResult
    """Cursor with results."""

    def __init__(self, db: SQLiteDatabase, engine_data: EngineData) -> None:
        super().__init__()
        self.db = db
        self.engine_data = engine_data
        self.scope_stack = []
        self.result = DroltaResult([], db, TempResult("", set()))

    def visit_declare_alias(self, node: DeclareAliasExpression):
        raise ProgrammingError("Alias declarations not allowed while querying.")

    def visit_declare_rule(self, node: DeclareRuleExpression):
        raise ProgrammingError("Rule declarations not allowed while querying.")

    def visit_query(self, node: QueryExpression):
        global _next_query_id  # pylint: disable=W0603
        _next_query_id += 1
        self.clear_scope_stack()

        _logger.debug("Evaluating query.")

        scope = self.new_scope()

        for entry in node.result_vars:
            scope.output_vars.append(
                ResultVariable(
                    var_name=entry.var_name,
                    aggregate_name=entry.aggregate_name,
                    alias=entry.alias,
                )
            )

        # Sort expressions to push filters and not-predicate expressions
        # to the end of the query.
        where_expressions = sorted(node.where_expressions, key=get_execution_order)

        for expr in where_expressions:
            expression_type = expr.get_expression_type()

            if expression_type == ExpressionType.PREDICATE_CALL:
                self.dispatch_visit_predicate(cast(PredicateExpression, expr))

            elif is_filter_expression(expr):
                self.visit_filter(expr)

            elif expression_type == ExpressionType.PREDICATE_NOT:
                self.visit_not_predicate(cast(NotPredicateExpression, expr))

            self._attempt_join_latest_table()

        self._force_join_all_tables()

        result_table = self.get_scope().tables.pop()

        # For the end of the query, we want to select from the result table
        # all the variables in output vars and assign them to any aliases

        output_cols: list[str] = []
        for entry in self.get_scope().output_vars:
            if entry.aggregate_name:
                if entry.aggregate_name not in SUPPORTED_AGGREGATES:
                    raise ProgrammingError(f"Use of unsupported aggregate: {entry}")

            output_cols.append(str(entry))

        sql_statement = f"""
            SELECT DISTINCT {', '.join(output_cols)}
            FROM {result_table.table_name}
            """

        if node.group_by:
            sql_statement += f"{node.group_by} "

        if node.order_by:
            sql_statement += f"{node.order_by} "

        if node.limit:
            sql_statement += f"{node.limit} "

        sql_statement += ";"

        _logger.debug(
            "Calculating Final Output:\n{}".format(  # pylint: disable=W1202, C0209
                FormattedSqlString(sql_statement)
            )
        )

        cursor = self.db.conn.cursor()

        result = cursor.execute(sql_statement)

        column_info_cursor = self.db.conn.cursor()

        raw_column_data: dict[str, str] = {
            k: v
            for k, v in column_info_cursor.execute(
                f"SELECT name, type FROM pragma_table_info('{result_table.table_name}')"
            ).fetchall()
        }

        column_info: list[ColumnInfo] = []
        for entry in self.get_scope().output_vars:
            if entry.var_name in raw_column_data:
                if entry.alias:
                    column_info.append(
                        ColumnInfo(
                            entry.alias,
                            sqlite_dtype_to_py(raw_column_data[entry.var_name]),
                        )
                    )
                else:
                    column_info.append(
                        ColumnInfo(
                            entry.var_name,
                            sqlite_dtype_to_py(raw_column_data[entry.var_name]),
                        )
                    )

        self.result = DroltaResult(
            columns=column_info, db=self.db, result_table=result_table, cursor=result
        )

    def visit_program(self, node: ProgramNode):
        self.result = DroltaResult([], db=self.db, result_table=TempResult("", set()))

        for child in node.children:
            self.visit(child)

    def visit_rule(self, name: str, node: PredicateExpression):
        """Evaluates a predicate expression as a rule."""

        self.new_scope()

        rule = self.engine_data.rules[name]

        # Sort expressions to push filters and not-predicate expressions
        # to the end of the query.
        where_expressions = sorted(rule.where_expressions, key=get_execution_order)

        for expr in where_expressions:
            expression_type = expr.get_expression_type()

            if expression_type == ExpressionType.PREDICATE_CALL:
                self.dispatch_visit_predicate(cast(PredicateExpression, expr))

            elif is_filter_expression(expr):
                self.visit_filter(expr)

            elif expression_type == ExpressionType.PREDICATE_NOT:
                self._force_join_all_tables()
                self.visit_not_predicate(cast(NotPredicateExpression, expr))

            self._attempt_join_latest_table()

        self._force_join_all_tables()

        self.execute_rule_sql(node, rule)

    def dispatch_visit_predicate(self, node: PredicateExpression):
        """Manages visiting predicates as true predicates or rules."""

        predicate_name = self.get_final_predicate_name(node.name)

        if predicate_name in self.engine_data.rules:
            self.visit_rule(predicate_name, node)
        else:
            self.visit_predicate(predicate_name, node)

    def visit_predicate(self, predicate_table_name: str, node: PredicateExpression):
        """Evaluate predicate expression against a table in the database."""

        self.execute_predicate_sql(predicate_table_name, node)

    def visit_filter(self, node: ExpressionNode):
        """Evaluate predicate expression."""

        # This function forces all the previous tables to join and performs a filter
        # on them.
        self._force_join_all_tables()

        result_table = self.get_scope().tables.pop()

        sql_statement = f"SELECT * FROM {result_table.table_name} WHERE {node}"

        table_name = self.get_temp_table_name()

        new_result_table = TempResult(
            table_name=table_name, output_vars=set(result_table.output_vars)
        )

        sql_temp_table_statement = (
            f"CREATE TEMPORARY TABLE {table_name} AS {sql_statement};"
        )

        _logger.debug(
            "Filtering Output:\n{}".format(  # pylint: disable=W1202, C0209
                FormattedSqlString(sql_temp_table_statement)
            )
        )

        self.db.execute(sql_temp_table_statement)

        # delete the old temp_table
        self.db.execute(f"DROP TABLE IF EXISTS {result_table.table_name};")

        self.get_scope().tables.append(new_result_table)

    def visit_not_predicate(self, node: NotPredicateExpression):
        """Evaluate predicate expression."""

        self.new_scope()

        expression_type = node.expr.get_expression_type()

        if expression_type == ExpressionType.PREDICATE_CALL:
            self.dispatch_visit_predicate(cast(PredicateExpression, node.expr))

        else:
            raise ProgrammingError("Not statement expects a predicate or rule.")

        result_table = self.get_scope().tables.pop()

        self.pop_scope()

        last_table = self.get_scope().tables.pop()

        table_name = self.get_temp_table_name()

        not_join_result = TempResult(
            table_name=table_name, output_vars=set(last_table.output_vars)
        )

        shared_vars = TempResult.get_common_vars(last_table, result_table)

        if shared_vars:
            where_filters = " AND ".join(
                f"({result_table.table_name}.{v} = {last_table.table_name}.{v})"
                for v in shared_vars
            )

            sql_statement = f"""
                SELECT *
                FROM {last_table.table_name}
                WHERE
                  NOT EXISTS (
                    SELECT 1
                    FROM {result_table.table_name}
                    WHERE {where_filters}
                  )
                """

            sql_temp_table_statement = (
                f"CREATE TEMPORARY TABLE {table_name} AS {sql_statement};"
            )

            _logger.debug(
                "Joining Not Join:\n{}".format(  # pylint: disable=W1202, C0209
                    FormattedSqlString(sql_temp_table_statement)
                )
            )

            self.db.execute(sql_temp_table_statement)

            self.db.execute(f"DROP TABLE IF EXISTS {result_table.table_name};")

            self.db.execute(f"DROP TABLE IF EXISTS {last_table.table_name};")

            self.get_scope().tables.append(not_join_result)

    def _force_join_all_tables(self) -> None:
        """Force all tables in the scope to join."""

        current_scope = self.get_scope()

        if len(current_scope.tables) > 1:
            last_table = current_scope.tables[-1]

            # Create a large join under a new temp_table.

            sql_join_statement = f"SELECT * FROM {last_table.table_name} "

            output_vars: set[str] = set(last_table.output_vars)

            num_other_tables = len(current_scope.tables) - 1
            for table_idx, other_table in enumerate(current_scope.tables[:-1]):
                shared_vars = TempResult.get_common_vars(last_table, other_table)

                output_vars = output_vars.union(other_table.output_vars)

                if shared_vars:
                    join_cols = " AND ".join(
                        f"({other_table.table_name}.{v} = {last_table.table_name}.{v})"
                        for v in shared_vars
                    )

                    sql_join_statement += (
                        f"JOIN {other_table.table_name} ON {join_cols}"
                    )
                else:
                    sql_join_statement += f"CROSS JOIN {other_table.table_name}"

                if table_idx == num_other_tables - 1:
                    sql_join_statement += ";"

                sql_join_statement += "\n"

            table_name = self.get_temp_table_name()

            sql_temp_table_statement = (
                f"CREATE TEMPORARY TABLE {table_name} AS {sql_join_statement};"
            )

            _logger.debug(
                "Joining All Tables:\n{}".format(  # pylint: disable=W1202, C0209
                    FormattedSqlString(sql_temp_table_statement)
                )
            )

            self.db.execute(sql_temp_table_statement)

            # Remove all tables involved with the join
            for table in current_scope.tables:
                self.db.execute(f"DROP TABLE IF EXISTS {table.table_name};")

            current_scope.tables.clear()

            current_scope.tables.append(
                TempResult(table_name=table_name, output_vars=output_vars)
            )

    def _attempt_join_latest_table(self) -> None:
        """Try to join the latest table with any existing ones."""
        current_scope = self.get_scope()
        if len(current_scope.tables) > 1:
            # Check if the last table has common vars with any
            # of the previous tables
            last_table = current_scope.tables[-1]

            shared_table_indexes: set[int] = set()
            output_vars: set[str] = set(last_table.output_vars)
            have_shared: list[tuple[int, list[str]]] = []

            for table_idx, other_table in enumerate(current_scope.tables[:-1]):
                shared_vars = TempResult.get_common_vars(last_table, other_table)
                if shared_vars:
                    have_shared.append((table_idx, shared_vars))
                    shared_table_indexes.add(table_idx)
                    output_vars = output_vars.union(other_table.output_vars)

            if have_shared:
                # Create a large join under a new temp_table.

                sql_join_statement = f"SELECT * FROM {last_table.table_name} "

                for idx, var_names in have_shared:
                    temp_table = current_scope.tables[idx]

                    join_cols = " AND ".join(
                        f"({temp_table.table_name}.{v} = {last_table.table_name}.{v})"
                        for v in var_names
                    )

                    sql_join_statement += (
                        f"JOIN {temp_table.table_name} ON {join_cols} "
                    )

                table_name = self.get_temp_table_name()

                sql_temp_table_statement = (
                    f"CREATE TEMPORARY TABLE {table_name} AS {sql_join_statement};"
                )

                _logger.debug(
                    "Joining Tables:\n{}".format(  # pylint: disable=W1202, C0209
                        FormattedSqlString(sql_temp_table_statement)
                    )
                )

                self.db.execute(sql_temp_table_statement)

                # Remove all tables involved with the join
                for idx in range(len(current_scope.tables), -1, -1):
                    if (
                        idx == len(current_scope.tables) - 1
                        or idx in shared_table_indexes
                    ):
                        table = current_scope.tables.pop(idx)

                        self.db.execute(f"DROP TABLE IF EXISTS {table.table_name};")

                current_scope.tables.append(
                    TempResult(table_name=table_name, output_vars=output_vars)
                )

    def execute_predicate_sql(self, table_name: str, node: PredicateExpression) -> None:
        """Execute SQL query for a predicate expression."""

        output_vars: set[str] = set()
        column_statements: list[str] = []
        where_statements: list[str] = []

        for column_name, expr in node.params:
            if expr.get_expression_type() == ExpressionType.VARIABLE:
                column_statements.append(f'{column_name} AS "{expr}"')
                output_vars.add(str(expr))
            else:
                if expr.get_expression_type() == ExpressionType.NULL:
                    where_statements.append(f"{column_name} IS {expr}")
                else:
                    where_statements.append(f"{column_name} = {expr}")

        if len(column_statements) == 0:
            raise ProgrammingError(f"Predicate '{node}' expects one output variable.")

        if where_statements:
            select_expr = f"""
                SELECT {', '.join(column_statements)}
                FROM {table_name}
                WHERE {' AND '.join(where_statements)}
                """
        else:
            select_expr = f"SELECT {', '.join(column_statements)} FROM {table_name} "

        temp_table_name = self.get_temp_table_name()

        sql_statement = f"CREATE TEMPORARY TABLE {temp_table_name} AS {select_expr};"

        _logger.debug(
            "Executing predicate select: \n{}".format(  # pylint: disable=W1202, C0209
                FormattedSqlString(sql_statement)
            )
        )

        self.db.execute(sql_statement)

        self.get_scope().tables.append(TempResult(temp_table_name, output_vars))

    def execute_rule_sql(self, node: PredicateExpression, rule: RuleData) -> None:
        """Get the final SQL expression for a rule expression."""

        # The variables output by this rules
        output_vars: set[str] = set()
        # Where statements used in the final SQL query
        where_statements: list[str] = []
        # Column selection statements
        column_statements: list[str] = []
        # Column selection statements used in the CTE
        cte_column_statements: list[str] = []

        for entry in rule.result_vars:
            if entry.aggregate_name:
                if entry.aggregate_name not in SUPPORTED_AGGREGATES:
                    raise ProgrammingError(f"Use of unsupported aggregate: {entry}")

            cte_column_statements.append(str(entry))

        for column_name, expr in node.params:
            # Add input parameters mapped to variables to the set of output vars
            if expr.get_expression_type() == ExpressionType.VARIABLE:
                column_statements.append(f'{column_name} AS "{expr}"')
                output_vars.add(str(expr))

            # If it is not a variable, then this is a column mapped to a constant
            # and must be added to the WHERE section of the final SQL query
            else:
                if expr.get_expression_type() == ExpressionType.NULL:
                    where_statements.append(f"{column_name} IS {expr}")
                else:
                    where_statements.append(f"{column_name} = {expr}")

        result_table = self.get_scope().tables.pop()

        if len(column_statements) == 0:
            raise ProgrammingError(f"Rule '{node}' expects one output variable.")

        if where_statements:

            select_expr = f"""
                WITH {rule.name} AS (
                  SELECT {', '.join(cte_column_statements)}
                  FROM {result_table.table_name}
                  {' ' + str(rule.group_by) + ' ' if rule.group_by else ''}
                  {' ' + str(rule.order_by) + ' ' if rule.order_by else ''}
                  {' ' + str(rule.limit) + ' ' if rule.limit else ''}
                )
                SELECT {', '.join(column_statements)}
                FROM {rule.name}
                WHERE {' AND '.join(where_statements)}
                """

        else:
            select_expr = f"""
                WITH {rule.name} AS (
                  SELECT {', '.join(cte_column_statements)}
                  FROM {result_table.table_name}
                  {' ' + str(rule.group_by) + ' ' if rule.group_by else ''}
                  {' ' + str(rule.order_by) + ' ' if rule.order_by else ''}
                  {' ' + str(rule.limit) + ' ' if rule.limit else ''}
                )
                SELECT {', '.join(column_statements)}
                FROM {rule.name}
                """

        self.pop_scope()

        temp_table_name = self.get_temp_table_name()

        sql_temp_table_statement = (
            f"CREATE TEMPORARY TABLE {temp_table_name} AS {select_expr};"
        )

        _logger.debug(
            "Executing Rule SQL:\n{}".format(  # pylint: disable=W1202, C0209
                FormattedSqlString(sql_temp_table_statement)
            )
        )

        self.db.execute(sql_temp_table_statement)

        self.db.execute(f"DROP TABLE IF EXISTS {result_table.table_name};")

        self.get_scope().tables.append(TempResult(temp_table_name, output_vars))

    def get_final_predicate_name(self, name: str) -> str:
        """Resolve the final name of a predicate from a potential alias."""

        final_name = name

        while final_name in self.engine_data.aliases:
            final_name = self.engine_data.aliases[final_name]

        return final_name

    def get_temp_table_name(self) -> str:
        """Generate a name for the next temporary table."""
        current_scope = self.get_scope()

        table_name = (
            self.TEMP_TABLE_PREFIX
            + f"{_next_query_id}_"
            + f"{current_scope.scope_id}_"
            + str(current_scope.next_table_id)
        )

        current_scope.next_table_id += 1

        return table_name

    def get_scope(self) -> Scope:
        """Get the current scope."""
        if self.scope_stack:
            return self.scope_stack[-1]

        return self.new_scope()

    def new_scope(self) -> Scope:
        """Push a new scope on the stack."""
        if self.scope_stack:
            scope = Scope(scope_id=self.scope_stack[-1].scope_id + 1)
        else:
            scope = Scope(scope_id=0)

        self.scope_stack.append(scope)
        return scope

    def pop_scope(self) -> Scope:
        """Pop the current scope."""
        scope = self.scope_stack.pop()
        self.destroy_temporary_tables(scope)
        return scope

    def clear_scope_stack(self) -> None:
        """Clear all scopes from the stack."""

        while self.scope_stack:
            self.pop_scope()

    def destroy_temporary_tables(self, scope: Scope) -> None:
        """Destroy all temporary tables at the given scope."""

        while scope.tables:
            table = scope.tables.pop()
            self.db.execute(f"DROP TABLE IF EXISTS {table.table_name};")
