from tatsu.ast import AST

class Cell(str):
    def evaluate(self):
        return str(self)

class Surface(int):
    def inverse(self):
        return Surface(-1 * self)

    def evaluate(self):
        return str(self)


class GeomExpression(tuple):
    """
    Any binary operation. Can be inversed.
    """

    def inverse(self):
        if self[0] == '*':
            return GeomExpression((':', self[1].inverse(), self[2].inverse()))
        elif self[0] == ':':
            return GeomExpression(('*', self[1].inverse(), self[2].inverse()))
        else:
            return self[0].inverse()

    def evaluate(self):
        if self[0] in '*:':
            return '({} {} {})'.format(self[1].evaluate(), self[0], self[2].evaluate())
        else:
            return str(self[0])



class GeomSemantics(object):
    def surface(self, ast):
        return Surface(ast)

    def cell(self, ast):
        return Cell(ast[1:])

    def complcell(self, ast):
        return Cell(ast)

    def operand(self, ast):
        if ast.l == '_(':
            return ast.o.inverse()
        elif ast.l == '(':
            return ast.o
        elif ast.l == '^(':
            e = GeomExpression(('^', Cell(ast.o)))
            return e
        else:
            return ast.o

    def isect(self, ast):
        if ast.o == '*':
            e = GeomExpression(('*', ast.l, ast.r))
            return e
        else:
            return ast.o

    def union(self, ast):
        if ast.o == ':':
            e = GeomExpression((':', ast.l, ast.r))
            return e
        else:
            return ast.o
