from lark import Visitor, Tree

class Parent(Visitor):
    def visit(self, tree):
        for subtree in tree.children:
            if isinstance(subtree, Tree):
                assert not hasattr(subtree, 'parent')
                subtree.parent = tree