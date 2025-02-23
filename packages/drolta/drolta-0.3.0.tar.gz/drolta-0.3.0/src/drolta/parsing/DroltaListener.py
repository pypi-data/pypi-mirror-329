# Generated from ./Drolta.g4 by ANTLR 4.13.2
from antlr4 import *

from drolta.parsing.DroltaParser import DroltaParser


# This class defines a complete listener for a parse tree produced by DroltaParser.
class DroltaListener(ParseTreeListener):

    # Enter a parse tree produced by DroltaParser#prog.
    def enterProg(self, ctx: DroltaParser.ProgContext):
        pass

    # Exit a parse tree produced by DroltaParser#prog.
    def exitProg(self, ctx: DroltaParser.ProgContext):
        pass

    # Enter a parse tree produced by DroltaParser#prog_statement.
    def enterProg_statement(self, ctx: DroltaParser.Prog_statementContext):
        pass

    # Exit a parse tree produced by DroltaParser#prog_statement.
    def exitProg_statement(self, ctx: DroltaParser.Prog_statementContext):
        pass

    # Enter a parse tree produced by DroltaParser#alias_declaration.
    def enterAlias_declaration(self, ctx: DroltaParser.Alias_declarationContext):
        pass

    # Exit a parse tree produced by DroltaParser#alias_declaration.
    def exitAlias_declaration(self, ctx: DroltaParser.Alias_declarationContext):
        pass

    # Enter a parse tree produced by DroltaParser#rule_declaration.
    def enterRule_declaration(self, ctx: DroltaParser.Rule_declarationContext):
        pass

    # Exit a parse tree produced by DroltaParser#rule_declaration.
    def exitRule_declaration(self, ctx: DroltaParser.Rule_declarationContext):
        pass

    # Enter a parse tree produced by DroltaParser#define_clause.
    def enterDefine_clause(self, ctx: DroltaParser.Define_clauseContext):
        pass

    # Exit a parse tree produced by DroltaParser#define_clause.
    def exitDefine_clause(self, ctx: DroltaParser.Define_clauseContext):
        pass

    # Enter a parse tree produced by DroltaParser#query.
    def enterQuery(self, ctx: DroltaParser.QueryContext):
        pass

    # Exit a parse tree produced by DroltaParser#query.
    def exitQuery(self, ctx: DroltaParser.QueryContext):
        pass

    # Enter a parse tree produced by DroltaParser#find_clause.
    def enterFind_clause(self, ctx: DroltaParser.Find_clauseContext):
        pass

    # Exit a parse tree produced by DroltaParser#find_clause.
    def exitFind_clause(self, ctx: DroltaParser.Find_clauseContext):
        pass

    # Enter a parse tree produced by DroltaParser#result_var.
    def enterResult_var(self, ctx: DroltaParser.Result_varContext):
        pass

    # Exit a parse tree produced by DroltaParser#result_var.
    def exitResult_var(self, ctx: DroltaParser.Result_varContext):
        pass

    # Enter a parse tree produced by DroltaParser#where_clause.
    def enterWhere_clause(self, ctx: DroltaParser.Where_clauseContext):
        pass

    # Exit a parse tree produced by DroltaParser#where_clause.
    def exitWhere_clause(self, ctx: DroltaParser.Where_clauseContext):
        pass

    # Enter a parse tree produced by DroltaParser#order_by_statement.
    def enterOrder_by_statement(self, ctx: DroltaParser.Order_by_statementContext):
        pass

    # Exit a parse tree produced by DroltaParser#order_by_statement.
    def exitOrder_by_statement(self, ctx: DroltaParser.Order_by_statementContext):
        pass

    # Enter a parse tree produced by DroltaParser#ordering_term.
    def enterOrdering_term(self, ctx: DroltaParser.Ordering_termContext):
        pass

    # Exit a parse tree produced by DroltaParser#ordering_term.
    def exitOrdering_term(self, ctx: DroltaParser.Ordering_termContext):
        pass

    # Enter a parse tree produced by DroltaParser#group_by_statement.
    def enterGroup_by_statement(self, ctx: DroltaParser.Group_by_statementContext):
        pass

    # Exit a parse tree produced by DroltaParser#group_by_statement.
    def exitGroup_by_statement(self, ctx: DroltaParser.Group_by_statementContext):
        pass

    # Enter a parse tree produced by DroltaParser#limit_statement.
    def enterLimit_statement(self, ctx: DroltaParser.Limit_statementContext):
        pass

    # Exit a parse tree produced by DroltaParser#limit_statement.
    def exitLimit_statement(self, ctx: DroltaParser.Limit_statementContext):
        pass

    # Enter a parse tree produced by DroltaParser#where_statement.
    def enterWhere_statement(self, ctx: DroltaParser.Where_statementContext):
        pass

    # Exit a parse tree produced by DroltaParser#where_statement.
    def exitWhere_statement(self, ctx: DroltaParser.Where_statementContext):
        pass

    # Enter a parse tree produced by DroltaParser#ComparisonFilter.
    def enterComparisonFilter(self, ctx: DroltaParser.ComparisonFilterContext):
        pass

    # Exit a parse tree produced by DroltaParser#ComparisonFilter.
    def exitComparisonFilter(self, ctx: DroltaParser.ComparisonFilterContext):
        pass

    # Enter a parse tree produced by DroltaParser#InFilter.
    def enterInFilter(self, ctx: DroltaParser.InFilterContext):
        pass

    # Exit a parse tree produced by DroltaParser#InFilter.
    def exitInFilter(self, ctx: DroltaParser.InFilterContext):
        pass

    # Enter a parse tree produced by DroltaParser#AndFilter.
    def enterAndFilter(self, ctx: DroltaParser.AndFilterContext):
        pass

    # Exit a parse tree produced by DroltaParser#AndFilter.
    def exitAndFilter(self, ctx: DroltaParser.AndFilterContext):
        pass

    # Enter a parse tree produced by DroltaParser#OrFilter.
    def enterOrFilter(self, ctx: DroltaParser.OrFilterContext):
        pass

    # Exit a parse tree produced by DroltaParser#OrFilter.
    def exitOrFilter(self, ctx: DroltaParser.OrFilterContext):
        pass

    # Enter a parse tree produced by DroltaParser#NotFilter.
    def enterNotFilter(self, ctx: DroltaParser.NotFilterContext):
        pass

    # Exit a parse tree produced by DroltaParser#NotFilter.
    def exitNotFilter(self, ctx: DroltaParser.NotFilterContext):
        pass

    # Enter a parse tree produced by DroltaParser#atom_list.
    def enterAtom_list(self, ctx: DroltaParser.Atom_listContext):
        pass

    # Exit a parse tree produced by DroltaParser#atom_list.
    def exitAtom_list(self, ctx: DroltaParser.Atom_listContext):
        pass

    # Enter a parse tree produced by DroltaParser#comparison_operator.
    def enterComparison_operator(self, ctx: DroltaParser.Comparison_operatorContext):
        pass

    # Exit a parse tree produced by DroltaParser#comparison_operator.
    def exitComparison_operator(self, ctx: DroltaParser.Comparison_operatorContext):
        pass

    # Enter a parse tree produced by DroltaParser#Predicate.
    def enterPredicate(self, ctx: DroltaParser.PredicateContext):
        pass

    # Exit a parse tree produced by DroltaParser#Predicate.
    def exitPredicate(self, ctx: DroltaParser.PredicateContext):
        pass

    # Enter a parse tree produced by DroltaParser#PredicateNot.
    def enterPredicateNot(self, ctx: DroltaParser.PredicateNotContext):
        pass

    # Exit a parse tree produced by DroltaParser#PredicateNot.
    def exitPredicateNot(self, ctx: DroltaParser.PredicateNotContext):
        pass

    # Enter a parse tree produced by DroltaParser#predicate_param.
    def enterPredicate_param(self, ctx: DroltaParser.Predicate_paramContext):
        pass

    # Exit a parse tree produced by DroltaParser#predicate_param.
    def exitPredicate_param(self, ctx: DroltaParser.Predicate_paramContext):
        pass

    # Enter a parse tree produced by DroltaParser#atom.
    def enterAtom(self, ctx: DroltaParser.AtomContext):
        pass

    # Exit a parse tree produced by DroltaParser#atom.
    def exitAtom(self, ctx: DroltaParser.AtomContext):
        pass

    # Enter a parse tree produced by DroltaParser#variable.
    def enterVariable(self, ctx: DroltaParser.VariableContext):
        pass

    # Exit a parse tree produced by DroltaParser#variable.
    def exitVariable(self, ctx: DroltaParser.VariableContext):
        pass


del DroltaParser
