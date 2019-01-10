#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Split surface card into name, transform, type and list of coeffs.
"""

import re

re_surface = re.compile(r"""^\s*([+*]*\d+)\s+
                            ([-+]*\d*\s*)
                            ([a-zA-Z/]+)\s+
                            (.*)$""", re.VERBOSE)


def split(txt):
    m = re_surface.search(txt)
    return m.groups()
