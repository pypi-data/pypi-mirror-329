"""Drolta abstract syntax tree implementation."""

from __future__ import annotations

import enum
import logging
from abc import ABC, abstractmethod
from sqlite3 import ProgrammingError
from typing import Any, Optional, cast

import antlr4
import attrs

from drolta.parsing.DroltaLexer import DroltaLexer
from drolta.parsing.DroltaListener import DroltaListener
from drolta.parsing.DroltaParser import DroltaParser

_logger = logging.getLogger(__name__)


class ExpressionType(enum.IntEnum):
    """All expressions supported by drolta scripts."""

    PROGRAM = enum.auto()
    DECLARE_ALIAS = enum.auto()
    DECLARE_RULE = enum.auto()
    QUERY = enum.auto()
    ORDER_BY = enum.auto()
    GROUP_BY = enum.auto()
    LIMIT = enum.auto()
    PREDICATE_CALL = enum.auto()
    PREDICATE_NOT = enum.auto()
    VARIABLE = enum.auto()
    INT = enum.auto()
    FLOAT = enum.auto()
    STRING = enum.auto()
    BOOL = enum.auto()
    NULL = enum.auto()
    BINARY_LOGICAL_FILTER = enum.auto()
    COMPARISON_FILTER = enum.auto()
    MEMBERSHIP_FILTER = enum.auto()
    RESULT_VARIABLE = enum.auto()


_VALID_VALUE_EXPRESSIONS = (
    ExpressionType.INT,
    ExpressionType.FLOAT,
    ExpressionType.STRING,
    ExpressionType.BOOL,
    ExpressionType.NULL,
)
"""Subset of expression types used to represent values."""

_VALID_FILTER_EXPRESSIONS = (
    ExpressionType.BINARY_LOGICAL_FILTER,
    ExpressionType.COMPARISON_FILTER,
    ExpressionType.MEMBERSHIP_FILTER,
)
"""The subset of expression types used for filters."""

_VALID_WHERE_EXPRESSIONS = (
    ExpressionType.PREDICATE_CALL,
    ExpressionType.BINARY_LOGICAL_FILTER,
    ExpressionType.COMPARISON_FILTER,
    ExpressionType.MEMBERSHIP_FILTER,
)
"""The subset of expression types used in where clauses."""


class LogicalOp(enum.IntEnum):
    """Logical operators."""

    AND = enum.auto()
    OR = enum.auto()


class ComparisonOp(enum.IntEnum):
    """Comparison operators."""

    LT = enum.auto()
    GT = enum.auto()
    LTE = enum.auto()
    GTE = enum.auto()
    EQ = enum.auto()
    NEQ = enum.auto()


class ExpressionNode(ABC):
    """Abstract base class implemented by all AST Nodes."""

    @abstractmethod
    def get_expression_type(self) -> ExpressionType:
        """Return the type of this expression."""
        raise NotImplementedError()


def is_filter_expression(node: ExpressionNode) -> bool:
    """Check if the given node is a valid filter expression."""

    return node.get_expression_type() in _VALID_FILTER_EXPRESSIONS


def is_where_expression(node: ExpressionNode) -> bool:
    """Check if a given node is a valid where expression."""

    return node.get_expression_type() in _VALID_WHERE_EXPRESSIONS


def is_value_expression(node: ExpressionNode) -> bool:
    """Check if a given node is a valid value expression."""

    return node.get_expression_type() in _VALID_VALUE_EXPRESSIONS


class ProgramNode(ExpressionNode):
    """The root node of Drolta ASTs."""

    __slots__ = ("children",)

    children: list[ExpressionNode]

    def __init__(self, children: list[ExpressionNode]) -> None:
        super().__init__()
        self.children = children

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.PROGRAM


class DeclareAliasExpression(ExpressionNode):
    """Expression node for declaring new predicate aliases."""

    __slots__ = ("original_name", "alias")

    original_name: str
    alias: str

    def __init__(self, original_name: str, alias: str) -> None:
        super().__init__()
        self.original_name = original_name
        self.alias = alias

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.DECLARE_ALIAS


class ResultVarExpression(ExpressionNode):
    """Expression node for result vars for rules and queries."""

    __slots__ = ("aggregate_name", "var_name", "alias")

    aggregate_name: str
    var_name: str
    alias: str

    def __init__(
        self, var_name: str, aggregate_name: str = "", alias: str = ""
    ) -> None:
        super().__init__()
        self.var_name = var_name
        self.aggregate_name = aggregate_name
        self.alias = alias

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.RESULT_VARIABLE

    def __str__(self):
        final_str = self.var_name

        if self.aggregate_name:
            final_str = f"{self.aggregate_name}({final_str})"

        if self.alias:
            final_str = f'{final_str} AS "{self.alias}"'

        return final_str


class DeclareRuleExpression(ExpressionNode):
    """Expression node for declaring new rules."""

    __slots__ = (
        "name",
        "result_vars",
        "where_expressions",
        "order_by",
        "group_by",
        "limit",
    )

    name: str
    result_vars: list[ResultVarExpression]
    where_expressions: list[ExpressionNode]
    order_by: Optional[OrderByExpression]
    group_by: Optional[GroupByExpression]
    limit: Optional[LimitExpression]

    def __init__(
        self,
        name: str,
        result_vars: list[ResultVarExpression],
        where_expressions: list[ExpressionNode],
        order_by: Optional[OrderByExpression] = None,
        group_by: Optional[GroupByExpression] = None,
        limit: Optional[LimitExpression] = None,
    ) -> None:
        super().__init__()
        self.name = name
        self.result_vars = result_vars
        self.where_expressions = where_expressions
        self.order_by = order_by
        self.group_by = group_by
        self.limit = limit
        self.validate()

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.DECLARE_RULE

    def validate(self) -> None:
        """Validate the fields."""
        if len(self.where_expressions) == 0:
            raise ProgrammingError(
                "WHERE section of rule declaration is missing statements."
            )

        if len(self.result_vars) == 0:
            raise ProgrammingError("Rule declaration is missing result variables.")


class BinaryExpression(ExpressionNode, ABC):
    """Abstract base class implemented by all binary operator expressions."""

    __slots__ = ("left", "right")

    left: ExpressionNode
    right: ExpressionNode

    def __init__(self, left: ExpressionNode, right: ExpressionNode) -> None:
        super().__init__()
        self.left = left
        self.right = right


class NotFilterExpression(ExpressionNode):
    """Logical NOT filter expressions."""

    __slots__ = ("expr",)

    expr: ExpressionNode

    def __init__(self, expr: ExpressionNode) -> None:
        super().__init__()
        self.expr = expr

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.BINARY_LOGICAL_FILTER

    def __str__(self):
        return f"(NOT {self.expr})"


class BinaryLogicalFilterExpression(BinaryExpression):
    """Logical AND/OR filter expressions."""

    __slots__ = ("op",)

    op: LogicalOp

    def __init__(
        self, left: ExpressionNode, right: ExpressionNode, op: LogicalOp
    ) -> None:
        super().__init__(left, right)
        self.op = op

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.BINARY_LOGICAL_FILTER

    def __str__(self) -> str:
        if self.op == LogicalOp.AND:
            return f"({self.left} AND {self.right})"
        else:
            return f"({self.left} OR {self.right})"


class ComparisonFilterExpression(BinaryExpression):
    """Comparison filter expressions."""

    __slots__ = ("op",)

    op: ComparisonOp

    def __init__(
        self, left: ExpressionNode, right: ExpressionNode, op: ComparisonOp
    ) -> None:
        super().__init__(left, right)
        self.op = op

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.COMPARISON_FILTER

    def __str__(self) -> str:
        if self.op == ComparisonOp.GT:
            return f"({self.left} > {self.right})"
        elif self.op == ComparisonOp.LT:
            return f"({self.left} < {self.right})"
        elif self.op == ComparisonOp.GTE:
            return f"({self.left} >= {self.right})"
        elif self.op == ComparisonOp.LTE:
            return f"({self.left} <= {self.right})"
        elif self.op == ComparisonOp.EQ:
            if self.right.get_expression_type() == ExpressionType.NULL:
                return f"({self.left} IS {self.right})"
            else:
                return f"({self.left} = {self.right})"
        else:
            if self.right.get_expression_type() == ExpressionType.NULL:
                return f"({self.left} IS NOT {self.right})"
            else:
                return f"({self.left} != {self.right})"


class MembershipFilterExpression(ExpressionNode):
    """Membership checking filter expression."""

    __slots__ = ("expr", "is_inverted", "values")

    expr: ExpressionNode
    is_inverted: bool
    values: list[ExpressionNode]

    def __init__(
        self, is_inverted: bool, expr: ExpressionNode, values: list[ExpressionNode]
    ) -> None:
        super().__init__()
        self.is_inverted = is_inverted
        self.expr = expr
        self.values = values
        self.validate()

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.MEMBERSHIP_FILTER

    def validate(self) -> None:
        """Validate this expression's fields."""
        expression_op = "NOT IN" if self.is_inverted else "IN"

        if self.expr.get_expression_type() != ExpressionType.VARIABLE:
            raise ProgrammingError(
                f"Expected variable for left side of '{expression_op}'"
            )

        for entry in self.values:
            expr_type = entry.get_expression_type()
            if expr_type == ExpressionType.VARIABLE:
                raise ProgrammingError(
                    f"Value list in '{expression_op}'-expression cannot contain variables."
                )
            if expr_type == ExpressionType.NULL:
                raise ProgrammingError(
                    f"Value list in '{expression_op}'-expression cannot contain NULL."
                )

    def __str__(self) -> str:
        value_list = ", ".join(str(v) for v in self.values)
        expression_op = "NOT IN" if self.is_inverted else "IN"
        return f"({self.expr} {expression_op} ({value_list}))"


class PredicateExpression(ExpressionNode):
    """A predicate expression."""

    __slots__ = ("name", "params")

    name: str
    params: list[tuple[str, ExpressionNode]]

    def __init__(self, name: str, params: list[tuple[str, ExpressionNode]]) -> None:
        super().__init__()
        self.name = name
        self.params = params

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.PREDICATE_CALL


class VariableExpression(ExpressionNode):
    """Expression for a variable."""

    __slots__ = ("variable",)

    variable: str

    def __init__(self, variable: str) -> None:
        super().__init__()
        self.variable = variable

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.VARIABLE

    def __str__(self) -> str:
        return f"{self.variable}"


class IntExpression(ExpressionNode):
    """An integer expression"""

    __slots__ = ("value",)

    value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.INT

    def __str__(self) -> str:
        return f"{self.value}"


class FloatExpression(ExpressionNode):
    """An float expression"""

    __slots__ = ("value",)

    value: float

    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.FLOAT

    def __str__(self) -> str:
        return f"{self.value}"


class StringExpression(ExpressionNode):
    """A string expression"""

    __slots__ = ("value",)

    value: str

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.STRING

    def __str__(self) -> str:
        return f"{self.value}"


class BoolExpression(ExpressionNode):
    """A boolean expression"""

    __slots__ = ("value",)

    value: bool

    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.BOOL

    def __str__(self) -> str:
        return f"{self.value}"


class NullExpression(ExpressionNode):
    """A null expression"""

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.NULL

    def __str__(self) -> str:
        return "NULL"


class NotPredicateExpression(ExpressionNode):
    """Not predicate expression."""

    __slots__ = ("expr",)

    expr: ExpressionNode

    def __init__(self, expr: ExpressionNode) -> None:
        super().__init__()
        self.expr = expr

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.PREDICATE_NOT


class QueryExpression(ExpressionNode):
    """A query expression."""

    __slots__ = ("result_vars", "where_expressions", "order_by", "group_by", "limit")

    result_vars: list[ResultVarExpression]
    where_expressions: list[ExpressionNode]
    order_by: Optional[OrderByExpression]
    group_by: Optional[GroupByExpression]
    limit: Optional[LimitExpression]

    def __init__(
        self,
        result_vars: list[ResultVarExpression],
        where_expressions: list[ExpressionNode],
        order_by: Optional[OrderByExpression] = None,
        group_by: Optional[GroupByExpression] = None,
        limit: Optional[LimitExpression] = None,
    ) -> None:
        super().__init__()
        self.result_vars = result_vars
        self.where_expressions = where_expressions
        self.order_by = order_by
        self.group_by = group_by
        self.limit = limit
        self.validate()

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.QUERY

    def validate(self) -> None:
        """Validate the fields."""
        if len(self.where_expressions) == 0:
            raise ProgrammingError("WHERE section of query is missing statements.")

        if len(self.result_vars) == 0:
            raise ProgrammingError("Query is missing result variables.")


class OrderingOp(enum.IntEnum):
    """Ordering operation."""

    NONE = 0
    ASC = enum.auto()
    DESC = enum.auto()


class NullsOrderingOp(enum.IntEnum):
    """Ordering operation for nulls in an ORDER BY clause."""

    NONE = 0
    FIRST = enum.auto()
    LAST = enum.auto()


@attrs.define(frozen=True, slots=True)
class OrderingTerm:
    """A term used to order query output."""

    var_name: str
    ordering_op: OrderingOp = OrderingOp.NONE
    nulls_ordering_op: NullsOrderingOp = NullsOrderingOp.NONE

    def __str__(self) -> str:
        asc_desc = ""
        if self.ordering_op != OrderingOp.NONE:
            asc_desc = " ASC" if self.ordering_op == OrderingOp.ASC else " DESC"

        nulls_order = ""
        if self.nulls_ordering_op != NullsOrderingOp.NONE:
            nulls_order = (
                " NULLS FIRST"
                if self.nulls_ordering_op == NullsOrderingOp.FIRST
                else " NULLS LAST"
            )

        return f"{self.var_name}{asc_desc}{nulls_order}"


class OrderByExpression(ExpressionNode):
    """Order by expression."""

    __slots__ = ("terms",)

    terms: list[OrderingTerm]

    def __init__(self, terms: list[OrderingTerm]) -> None:
        super().__init__()
        self.terms = terms

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.ORDER_BY

    def __str__(self) -> str:
        term_list_str = ", ".join(str(term) for term in self.terms)
        return f"ORDER BY {term_list_str}"


class GroupByExpression(ExpressionNode):
    """Group by expression."""

    __slots__ = ("grouping_terms",)

    grouping_terms: list[str]

    def __init__(self, terms: list[str]) -> None:
        super().__init__()
        self.grouping_terms = terms

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.GROUP_BY

    def __str__(self) -> str:
        term_list_str = ", ".join(term for term in self.grouping_terms)
        return f"GROUP BY {term_list_str}"


class LimitExpression(ExpressionNode):
    """Limit expression."""

    __slots__ = ("value", "offset")

    value: int
    offset: int

    def __init__(self, value: int, offset: int = -1) -> None:
        super().__init__()
        self.value = value
        self.offset = offset

    def get_expression_type(self) -> ExpressionType:
        return ExpressionType.LIMIT

    def __str__(self) -> str:
        offset_expr = f" OFFSET {self.offset}" if self.offset > 0 else ""
        return f"LIMIT {self.value}{offset_expr}"


class ASTVisitor(ABC):
    """Abstract base class implemented by visitors that traverse ASTs."""

    @abstractmethod
    def visit_program(self, node: ProgramNode) -> None:
        """Visit Program Node."""
        raise NotImplementedError()

    @abstractmethod
    def visit_declare_alias(self, node: DeclareAliasExpression) -> None:
        """Visit DeclareAliasNode."""
        raise NotImplementedError()

    @abstractmethod
    def visit_declare_rule(self, node: DeclareRuleExpression) -> None:
        """Visit DeclareRuleNode."""
        raise NotImplementedError()

    @abstractmethod
    def visit_query(self, node: QueryExpression) -> None:
        """Visit QueryExpression."""
        raise NotImplementedError()

    def visit(self, node: ExpressionNode) -> None:
        """Dynamic dispatch by node type."""
        expression_type = node.get_expression_type()

        if expression_type == ExpressionType.PROGRAM:
            return self.visit_program(cast(ProgramNode, node))

        if expression_type == ExpressionType.DECLARE_ALIAS:
            return self.visit_declare_alias(cast(DeclareAliasExpression, node))

        if expression_type == ExpressionType.DECLARE_RULE:
            return self.visit_declare_rule(cast(DeclareRuleExpression, node))

        if expression_type == ExpressionType.QUERY:
            return self.visit_query(cast(QueryExpression, node))

        raise TypeError(f"Unsupported node expression type: {expression_type.name}")


@attrs.define(slots=True)
class _ListenerScope:
    """A scope of data used within the script listener."""

    rule_name: str = ""
    result_vars: list[ResultVarExpression] = attrs.field(factory=list)
    expr_queue: list[ExpressionNode] = attrs.field(factory=list)
    predicate_params: list[tuple[str, ExpressionNode]] = attrs.field(factory=list)
    order_by_expr: Optional[OrderByExpression] = None
    group_by_expr: Optional[GroupByExpression] = None
    limit_expr: Optional[LimitExpression] = None


class _ScriptListener(DroltaListener):
    """Customize listener for drolta scripts."""

    __slots__ = ("_ast", "_scope_stack")

    _scope_stack: list[_ListenerScope]
    _ast: ExpressionNode

    def __init__(self) -> None:
        self._scope_stack = []
        self._ast = ProgramNode([])

    def get_ast(self) -> ExpressionNode:
        """Get the generated AST."""
        return self._ast

    def enterProg(self, ctx: DroltaParser.ProgContext):
        self.new_scope()

    def exitProg(self, ctx: DroltaParser.ProgContext):
        scope = self.pop_scope()

        self._ast = ProgramNode(scope.expr_queue)

    def exitAlias_declaration(self, ctx: DroltaParser.Alias_declarationContext):
        original_name = str(ctx.original.text)  # type: ignore
        alias_name = str(ctx.alias.text)  # type: ignore

        self.get_scope().expr_queue.append(
            DeclareAliasExpression(original_name, alias_name)
        )

    def enterRule_declaration(self, ctx: DroltaParser.Rule_declarationContext):
        self.new_scope()

    def exitRule_declaration(self, ctx: DroltaParser.Rule_declarationContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            DeclareRuleExpression(
                name=scope.rule_name,
                result_vars=scope.result_vars,
                where_expressions=scope.expr_queue,
                order_by=scope.order_by_expr,
                group_by=scope.group_by_expr,
                limit=scope.limit_expr,
            )
        )

    def exitDefine_clause(self, ctx: DroltaParser.Define_clauseContext):
        rule_name: str = ctx.ruleName.text  # type: ignore
        self.get_scope().rule_name = rule_name

    def exitResult_var(self, ctx: DroltaParser.Result_varContext):
        scope = self.get_scope()

        var_name: str = ctx.variable().IDENTIFIER().getText()  # type: ignore
        aggregate_name: str = ctx.aggregateName.text if ctx.aggregateName else ""  # type: ignore
        alias: str = ctx.alias.text if ctx.alias else ""

        scope.result_vars.append(
            ResultVarExpression(
                var_name=var_name,  # type: ignore
                aggregate_name=aggregate_name,
                alias=alias,
            )
        )

    def enterQuery(self, ctx: DroltaParser.QueryContext):
        self.new_scope()

    def exitQuery(self, ctx: DroltaParser.QueryContext):
        scope = self.pop_scope()

        expr = QueryExpression(
            result_vars=scope.result_vars,
            where_expressions=scope.expr_queue,
            order_by=scope.order_by_expr,
            group_by=scope.group_by_expr,
            limit=scope.limit_expr,
        )

        self.get_scope().expr_queue.append(expr)

    def exitOrder_by_statement(self, ctx: DroltaParser.Order_by_statementContext):
        terms: list[OrderingTerm] = []

        for entry in ctx.ordering_term():  # type: ignore

            ordering_op = OrderingOp.NONE
            if entry.ASC():  # type: ignore
                ordering_op = OrderingOp.ASC
            elif entry.DESC():  # type: ignore
                ordering_op = OrderingOp.DESC

            nulls_ordering_op = NullsOrderingOp.NONE
            if entry.FIRST():  # type: ignore
                nulls_ordering_op = NullsOrderingOp.FIRST
            elif entry.LAST():  # type: ignore
                nulls_ordering_op = NullsOrderingOp.LAST

            terms.append(
                OrderingTerm(
                    var_name=entry.variable().IDENTIFIER().getText(),  # type: ignore
                    ordering_op=ordering_op,
                    nulls_ordering_op=nulls_ordering_op,
                )
            )

        self.get_scope().order_by_expr = OrderByExpression(terms)

    def exitGroup_by_statement(self, ctx: DroltaParser.Group_by_statementContext):
        terms: list[str] = []

        for entry in ctx.variable():  # type: ignore
            terms.append(entry.IDENTIFIER().getText())  # type: ignore

        self.get_scope().group_by_expr = GroupByExpression(terms)

    def exitLimit_statement(self, ctx: DroltaParser.Limit_statementContext):
        limit: int = int(ctx.limitVal.text)  # type: ignore
        offset: int = int(ctx.offsetVal.text) if ctx.offsetVal else -1  # type: ignore

        self.get_scope().limit_expr = LimitExpression(value=limit, offset=offset)

    def enterPredicate(self, ctx: DroltaParser.PredicateContext):
        self.new_scope()

    def exitPredicate(self, ctx: DroltaParser.PredicateContext):
        predicate_name: str = ctx.IDENTIFIER().getText()  # type: ignore

        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            PredicateExpression(name=predicate_name, params=scope.predicate_params)  # type: ignore
        )

    def enterPredicateNot(self, ctx: DroltaParser.PredicateNotContext):
        self.new_scope()

    def exitPredicateNot(self, ctx: DroltaParser.PredicateNotContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(NotPredicateExpression(scope.expr_queue[0]))

    def enterPredicate_param(self, ctx: DroltaParser.Predicate_paramContext):
        self.new_scope()

    def exitPredicate_param(self, ctx: DroltaParser.Predicate_paramContext):
        scope = self.pop_scope()

        atom = scope.expr_queue[0]

        self.get_scope().predicate_params.append(
            (ctx.IDENTIFIER().getText(), atom)  # type: ignore
        )

    def enterComparisonFilter(self, ctx: DroltaParser.ComparisonFilterContext):
        self.new_scope()

    def exitComparisonFilter(self, ctx: DroltaParser.ComparisonFilterContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            ComparisonFilterExpression(
                op=_ScriptListener.parse_comparison_op(ctx.op.getText()),  # type: ignore
                left=VariableExpression(ctx.variable().IDENTIFIER().getText()),  # type: ignore
                right=scope.expr_queue[0],
            )
        )

    def enterAndFilter(self, ctx: DroltaParser.AndFilterContext):
        self.new_scope()

    def exitAndFilter(self, ctx: DroltaParser.AndFilterContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            BinaryLogicalFilterExpression(
                op=LogicalOp.AND, left=scope.expr_queue[0], right=scope.expr_queue[1]
            )
        )

    def enterOrFilter(self, ctx: DroltaParser.OrFilterContext):
        self.new_scope()

    def exitOrFilter(self, ctx: DroltaParser.OrFilterContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            BinaryLogicalFilterExpression(
                op=LogicalOp.OR, left=scope.expr_queue[0], right=scope.expr_queue[1]
            )
        )

    def enterNotFilter(self, ctx: DroltaParser.NotFilterContext):
        self.new_scope()

    def exitNotFilter(self, ctx: DroltaParser.NotFilterContext):
        scope = self.pop_scope()

        self.get_scope().expr_queue.append(
            NotFilterExpression(
                expr=scope.expr_queue[0],
            )
        )

    def enterInFilter(self, ctx: DroltaParser.InFilterContext):
        self.new_scope()

    def exitInFilter(self, ctx: DroltaParser.InFilterContext):
        scope = self.pop_scope()

        is_inverted: bool = ctx.NOT() is not None

        self.get_scope().expr_queue.append(
            MembershipFilterExpression(
                is_inverted=is_inverted,
                expr=VariableExpression(ctx.variable().IDENTIFIER().getText()),  # type: ignore
                values=scope.expr_queue,
            )
        )

    def exitAtom(self, ctx: DroltaParser.AtomContext):
        if ctx.variable():
            self.get_scope().expr_queue.append(
                VariableExpression(ctx.variable().IDENTIFIER().getText())  # type: ignore
            )
            return

        if ctx.INT_LITERAL():
            self.get_scope().expr_queue.append(
                IntExpression(int(ctx.INT_LITERAL().getText()))  # type: ignore
            )
            return

        if ctx.FLOAT_LITERAL():
            self.get_scope().expr_queue.append(
                FloatExpression(float(ctx.FLOAT_LITERAL().getText()))  # type: ignore
            )
            return

        if ctx.STRING_LITERAL():
            self.get_scope().expr_queue.append(
                StringExpression(str(ctx.STRING_LITERAL().getText()))  # type: ignore
            )
            return

        if ctx.getText() == "TRUE":  # type: ignore
            self.get_scope().expr_queue.append(BoolExpression(True))

        if ctx.getText() == "FALSE":  # type: ignore
            self.get_scope().expr_queue.append(BoolExpression(False))

        if ctx.getText() == "NULL":  # type: ignore
            self.get_scope().expr_queue.append(NullExpression())

    def new_scope(self) -> _ListenerScope:
        """Create a new listener scope"""

        scope = _ListenerScope()
        self._scope_stack.append(scope)
        return scope

    def get_scope(self) -> _ListenerScope:
        """Get the current scope."""

        if self._scope_stack:
            return self._scope_stack[-1]

        return self.new_scope()

    def pop_scope(self) -> _ListenerScope:
        """Pop the current scope from the stack."""

        return self._scope_stack.pop()

    @staticmethod
    def parse_comparison_op(text: str) -> ComparisonOp:
        """Convert text to a comparison operation"""
        if text == "=":
            return ComparisonOp.EQ
        if text == "!=":
            return ComparisonOp.NEQ
        if text == "<=":
            return ComparisonOp.LTE
        if text == "<":
            return ComparisonOp.LT
        if text == ">=":
            return ComparisonOp.GTE
        if text == ">":
            return ComparisonOp.GT

        raise ValueError(f"Unrecognized comparison operator: '{text}'.")


def generate_ast(script_text: str) -> ExpressionNode:
    """Generate a Drolta AST from the given script text."""

    input_stream = antlr4.InputStream(script_text)
    lexer = DroltaLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = DroltaParser(stream)
    error_listener = _SyntaxErrorListener()

    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)  # type: ignore

    tree = parser.prog()

    if error_listener.error_count:
        error_message = "Syntax errors found in drolta script:\n"
        for msg in error_listener.error_messages:
            error_message += msg + "\n"

        _logger.error(error_message)

        raise SyntaxError(error_message)

    listener = _ScriptListener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)  # type: ignore

    drolta_ast = listener.get_ast()

    return drolta_ast


class _SyntaxErrorListener(antlr4.DiagnosticErrorListener):
    __slots__ = ("error_count", "error_messages")

    error_count: int
    error_messages: list[str]

    def __init__(self) -> None:
        super().__init__()
        self.error_count = 0
        self.error_messages = []

    def syntaxError(
        self,
        recognizer: Any,
        offendingSymbol: Any,
        line: int,
        column: int,
        msg: str,
        e: Any,
    ) -> None:
        self.error_count += 1
        self.error_messages.append(f"line {line}:{column} {msg}")

    def clear(self) -> None:
        """Clear all cached errors."""
        self.error_count = 0
        self.error_messages.clear()
