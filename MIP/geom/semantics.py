from tatsu.ast import AST

class Cell(str):
    def evaluate(self):
        return str(self)

class Surface:
    def __init__(self, surface, sub=None):
        self.surface = int(surface)
        self.sub = int(sub) if sub is not None else None

    def __repr__(self):
        return 'Surface({!r}, {!r})'.format(self.surface, self.sub)

    def __str__(self):
        if self.sub is None:
            return 'Surface({!s})'.format(self.surface)
        return 'Surface({!s}.{!s})'.format(self.surface, self.sub)

    def inverse(self):
        return Surface(-self.surface, self.sub)

    def evaluate(self):
        if self.sub is None:
            return str(self)
        return str(self) + '.' + str(self.sub)

    def __abs__(self):
        return Surface(abs(self.surface), self.sub)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.surface == other.surface and self.sub == other.sub
        return False

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        if isinstance(other, int):
            return self.surface > other
        return self.surface > other.surface

    def __ge__(self, other):
        if isinstance(other, int):
            return self.surface >= other
        return self.surface >= other.surface

    def __lt__(self, other):
        if isinstance(other, int):
            return self.surface < other
        return self.surface < other.surface

    def __le__(self, other):
        if isinstance(other, int):
            return self.surface <= other
        return self.surface <= other.surface

    def __neg__(self):
        return Surface(-self.surface, self.sub)

    def __hash__(self):
        # required to use Surfaces as dictionary keys or set elements
        return hash((self.surface, self.sub))

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



class GeomSemantics:
    def surface(self, ast):
        if '.' in ast:
            surface, sub = ast.split('.')
            return Surface(surface, sub)
        else:
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
