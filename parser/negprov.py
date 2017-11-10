import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from tatsu.model import ModelBuilderSemantics
from pprint import pprint
import os

from dedalus import TrivialSemantics

class NegNodeWalker(NodeWalker):

    def walk_program(self,node):
        # Walk the includes
        print "WALK_PROGRAM"
        print self.walk(node.includes)
        # Walk the rules
        print self.walk(node.rules)

    def walk_stmlist(self,node):
        ret = ""
        # Walk each statment in the statement list.
        for stmt in node.stmts:
            ret += self.walk(stmt[0]) + ";\n"

        return ret

    def walk_includelist(self, node):
        ret = ""
        for include in node.includelist:
            ret += self.walk(include) + ";\n"
        return ret

    def walk_statement(self, node):
        return self.walk(node.stmt)

    def walk_rule(self, node):
        return self.walk(node.lhs) + self.walk(node.merge) + ":-" + self.walk(node.rhs)

    def walk_rhs(self, node):
        return self.walk(node.rhs)

    def walk_lhs(self, node):
        return self.walk(node.predicate)

    def walk_subgoallist(self, node):
        if isinstance(node.subgoals, list):
            ret = ""
            for subgoal in node.subgoals:
                ret += self.walk(subgoal) + ","
            return ret[:len(ret)-1]
        else:
            return self.walk(node.subgoals)

    def walk_subgoal(self, node):
        return self.walk(node.subgoal)

    def walk_catalog_entry(self, node):
        return node.entry

    def walk_rhspredicate(self, node):
        return self.walk(node.pred)

    def walk_predicate(self, node):
        return self.walk(node.table) + ' (' + self.walk(node.args) + ')'

    def walk_exprlist(self, node):
        if isinstance(node.exprs, list):
            ret = ""
            for expr in node.exprs:
                ret += self.walk(expr) + ", "
            return ret[:len(ret)-2]
        else:
            return self.walk(node.exprs)

    def walk_expr(self, node):
        return self.walk(node.expr)

    def walk_var(self, node):
        return node.val

    def walk_notin(self, node):
        return 'notin ' + self.walk(node.pred)

    def walk_merge(self, node):
        return node.merge

    # Here to check if a node being used hasn't been defined yet.
    def walk_Node(self, node):
        print "node undefined"
        print node
        return ""