# -*- coding: utf-8 -*-

class CSurfaceCollection:
    def __init__(self, main, fixed=None):
        self.main = main
        self.fixed = fixed.copy() if fixed is not None else []
