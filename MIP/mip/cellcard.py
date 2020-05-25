#!/urs/bin/env python
# -*- coding: utf-8 -*-

# Split cell card in name, material, geometry and options.
#
# A cells card always starts with its name followed by one or more spaces. The
# rest has two forms:
#
#     * "LIKE n but ..." form. Here the keywords "like" and "but" are delimited
#     by space(s).  The "but" keyword is followed by optional paramters,
#     including those using parentheses (trcl, fill) and multiple entries (fill
#     in presence of lat).
#
#     * Material (one or two entires delimited by one or more spaces), followed
#     by geometry description where entries can be delimited by spaces, colon
#     and parentheses, followed by optional parameters (like in the "like n but"
#     form).
#
# Therefore, the cell name (number) is always delimited from the following part
# by space(s).  The "like n but" entries also delimited by spaces. But geometry
# description part can be delimited from the material part and the part
# containing optional parameters with both space(s) and parentheses.
#
# The part with optional parameters starts with an alphabet character. It
# preceeded with a number followed by one or more space, or closing parenthesis,
# followed by zero or more spaces.
#
# Patterns of the cell card. Parts are delimited by '|' (one or more spaces) or
# by '||' (zero or more spaces, or parentheses).
#
#     N | like    | n | but        | options
#     N | zero            || geom || options
#     N | non-zero | dens || geom || options
#
# Options are optional.

import re

# RE to find where options start, not for like-but syntax.
re_options = re.compile('([\)\s])([\*a-zA-Z].*)$')

re_likebut = re.compile(r"""^(\s*[0-9]+)     # name
                             (\s+like.*but)  # like-but geometry
                             (.*)$           # options""",
                        re.IGNORECASE + re.VERBOSE)
re_void = re.compile(r"""^(\s*[0-9]+)        # name
                          (\s+\S+)           # zero material
                          (.*)$              # geometry""",
                     re.IGNORECASE + re.VERBOSE)
re_nonvoid = re.compile(r"""^(\s*[0-9]+)        # name
                             (\s+\S+\s+[^\s(]+) # material and density
                             (.*)$              # geometry""",
                        re.IGNORECASE + re.VERBOSE)


def split(txt):
    """
    Split cell card txt into parts.

    String `txt` must have no comments and new-line characters.
    """
    # Extract name
    name, t2, _ = txt.split(None, 2)
    if t2.lower() == 'like':
        name, geom, opts = re_likebut.findall(txt)[0]
        mat = ''
    else:
        # Extract options
        parts = re_options.split(txt)
        if len(parts) == 4:
            # txt has options
            p1, p2, opts, _ = parts
            txt = p1 + p2
        else:
            opts = ''
        if float(t2) == 0:
            name, mat, geom = re_void.findall(txt)[0]
        else:
            name, mat, geom = re_nonvoid.findall(txt)[0]
    return name, mat, geom, opts
