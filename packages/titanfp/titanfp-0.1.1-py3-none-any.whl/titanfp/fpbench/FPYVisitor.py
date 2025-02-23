# Generated from FPY.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FPYParser import FPYParser
else:
    from FPYParser import FPYParser

# This class defines a complete generic visitor for a parse tree produced by FPYParser.

class FPYVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FPYParser#parse_fpy.
    def visitParse_fpy(self, ctx:FPYParser.Parse_fpyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#fpy.
    def visitFpy(self, ctx:FPYParser.FpyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#arglist.
    def visitArglist(self, ctx:FPYParser.ArglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#argument.
    def visitArgument(self, ctx:FPYParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#dimlist.
    def visitDimlist(self, ctx:FPYParser.DimlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#dimension.
    def visitDimension(self, ctx:FPYParser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#number.
    def visitNumber(self, ctx:FPYParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#expr.
    def visitExpr(self, ctx:FPYParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#note.
    def visitNote(self, ctx:FPYParser.NoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#comp.
    def visitComp(self, ctx:FPYParser.CompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#arith.
    def visitArith(self, ctx:FPYParser.ArithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#term.
    def visitTerm(self, ctx:FPYParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#factor.
    def visitFactor(self, ctx:FPYParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#power.
    def visitPower(self, ctx:FPYParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#atom.
    def visitAtom(self, ctx:FPYParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#prop.
    def visitProp(self, ctx:FPYParser.PropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#simple_stmt.
    def visitSimple_stmt(self, ctx:FPYParser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#binding.
    def visitBinding(self, ctx:FPYParser.BindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#block.
    def visitBlock(self, ctx:FPYParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#if_stmt.
    def visitIf_stmt(self, ctx:FPYParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#let_stmt.
    def visitLet_stmt(self, ctx:FPYParser.Let_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#while_stmt.
    def visitWhile_stmt(self, ctx:FPYParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#for_stmt.
    def visitFor_stmt(self, ctx:FPYParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#tensor_stmt.
    def visitTensor_stmt(self, ctx:FPYParser.Tensor_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#compound_stmt.
    def visitCompound_stmt(self, ctx:FPYParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#statement.
    def visitStatement(self, ctx:FPYParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#datum.
    def visitDatum(self, ctx:FPYParser.DatumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#simple_data.
    def visitSimple_data(self, ctx:FPYParser.Simple_dataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#data_suite.
    def visitData_suite(self, ctx:FPYParser.Data_suiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#annotation.
    def visitAnnotation(self, ctx:FPYParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#suite.
    def visitSuite(self, ctx:FPYParser.SuiteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#symbolic.
    def visitSymbolic(self, ctx:FPYParser.SymbolicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#symbolic_data.
    def visitSymbolic_data(self, ctx:FPYParser.Symbolic_dataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#open_.
    def visitOpen_(self, ctx:FPYParser.Open_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPYParser#close_.
    def visitClose_(self, ctx:FPYParser.Close_Context):
        return self.visitChildren(ctx)



del FPYParser