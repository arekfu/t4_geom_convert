#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

"""
"""

re_comment = re.compile(r'^\s{0,4}[cC](\s|$)')
re_continuation_spaces = re.compile(r'^\s{5,}')
re_continuation_prev = re.compile(r'[^$]*&\s*($|\$.*$)')


# Function used at two places below
def _yield(c1, n1, f, c2, n2):
    if c1:
        yield c1, n1, 'card'
    if not f and c2:
        yield c2, n2, 'cmnt'


def get_cards(block, skipcomments=False):
    """
    Split text in `block` into cards. Return card text, line number in the block
    and type ('card' or 'cmnt').

    The `block` represents one block of MCNP input file, which in general
    consists of one or more cards and zero or more comment lines.

    Definition: C-comment is a comment line inside a card. B-comment is a
    comment line between cards, i.e. above the line where the next card begins.
    Several lines with B-comments compose a multi-line B-comment.

    The C-comments are returned within cards. The B-comments are returned
    separately, when the `skipcomments` flag is False. Thus, Two types of
    elements are returned: cards and B-comments. Both are, generally, multi-line
    strings.

    A card is a part of the block containing all lines belonging to a card,
    including the C-comments.

    """

    # List of comment lines
    cmnt = []
    # List of lines describing a card
    card = []
    # Line number where card or block of comments starts:
    n_card = 0
    n_cmnt = 0

    lprev = None  # previous card line
    for n, l in enumerate(block.splitlines()):
        # if comment, then  add to block of comments
        # if continuation, then append block of comment this line to current
        # card
        # if new card, then yield current card or current block of comments and
        # create a new current card
        if re_comment.match(l):
            cmnt.append(l)
        elif is_continuation(l, lprev):
            if not skipcomments:
                card.extend(cmnt)
            cmnt = []
            n_cmnt = n + 1
            card.append(l)
            lprev = l
        else:
            # this must be begin of a new card
            for r in _yield(card, n_card, skipcomments, cmnt, n_cmnt):
                yield r
            cmnt = []
            n_cmnt = n + 1
            card = [l]
            n_card = n
            lprev = l
    # At the end of block, yield the last card and comments (this code must be
    # the same as in `else` clause above)
    for r in _yield(card, n_card, skipcomments, cmnt, n_cmnt):
        yield r


def expand_tabs(line):
    r'''Expand tabs in a line.

    The MCNP manual says that "tabs are replaced by blanks to the next
    8-character tab stop.

    >>> expand_tabs('\tdodo')
    '        dodo'
    >>> expand_tabs('  \tdodo')
    '        dodo'
    >>> expand_tabs('      \tdodo')
    '        dodo'
    >>> expand_tabs('       \tdodo')
    '        dodo'
    >>> expand_tabs('        \tdodo')
    '                dodo'
    >>> expand_tabs('\t\tdodo')
    '                dodo'
    '''
    expanded = []
    i = 0
    for char in line:
        if char != '\t':
            expanded.append(char)
            i += 1
        else:
            n_spaces = 8-(i%8)
            expanded.append(' '*n_spaces)
            i += n_spaces
    return ''.join(expanded)

def is_continuation(l, prev=None):
    """
    Check if l is a continuation line.

    l and prev must not be comment lines.
    """
    # If l has 5 or more leading spaces, it is a continuation independently
    # on prev
    l = expand_tabs(l)
    if re_continuation_spaces.match(l):
        return True
    elif prev and re_continuation_prev.match(prev):
        return True
    return False
