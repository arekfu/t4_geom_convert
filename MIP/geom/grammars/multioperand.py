class Surface(int):
    def inverse(self):
        return Surface(self * -1)


class Cell(str):
    pass


class Operation(tuple):
    def inverse(self):
        return self.io(x.inverse for x in self)

    def __str__(self):
        return self.op + super(Operation, self).__str__()

    def __repr__(self):
        return str(self)


class Union(Operation):
    def __init__(self, *a, **kwa):
        super(Union, self).__init__(*a, **kwa)
        self.op = 'U'
        self.io = Isect
        return


class Isect(Operation):
    def __init__(self, *a, **kwa):
        super(Isect, self).__init__(*a, **kwa)
        self.op = 'I'
        self.io = Union
        return


class Semantics:
    def surface(self, ast):
        return Surface(ast)

    def cell(self, ast):
        return Cell(ast)

    def operand(self, ast):
        print('*** operand', ast)
        if ast.o1 is not None:
            return ast.o1
        if ast.o2 is not None:
            return ast.o2
        if ast.o4 is not None:
            return ast.o4
        if ast.o7 is not None:
            return ast.o7

    def compl(self, ast):
        print('*** compl', repr(ast))
        return ast.inverse()

    def isect(self, ast):
        print('*** isect', repr(ast))
        if ast.i5 is not None:
            return ast.i5
        r = Isect((ast.i1, ast.i4))
        if ast.i3:
            r += Isect(ast.o)
        return r

    def union(self, ast):
        print('*** union', repr(ast))
        if ast.u5 is not None:
            return ast.u5
        r = Union((ast.u1, ast.u4))
        if isinstance(ast.r1, list):
            r += Union(ast.r1)
        else:
            r += Union((ast.r1, ))
        return r
