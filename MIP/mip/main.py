import re
from functools import wraps

from .blocks import get_block_positions
from .cards import get_cards

from . import cellcard
from . import surfacecard
from . import datacard

re_comment = re.compile('[$&].*$', re.MULTILINE)
re_spaces = re.compile('\s+')


def card_debugger(meth):
    @wraps(meth)
    def wrapper(*a, **kwa):
        try:
            return meth(*a, **kwa)
        except Exception as e:
            print("On line", a[0].position)
            print("Card lines:")
            for l in a[0].lines:
                print('    ', repr(l))
            raise e
    return wrapper


class Card:
    """
    Representation of a card in the MCNP input file.

    The methods helps to get a content of a card (stripping out the comments)
    and split a card into logical parts.
    """
    def __init__(self, lines=[], position=0, type=None):
        self.lines = lines
        self.position = position
        self.type = type
        return

    @card_debugger
    def content(self):
        """
        return one line containing only meaningful part of the card.

        From a list of lines representing a card with comments, extract only
        meaningfull part (i.e. remove all comments and extra-spaces). The result
        is a one-line string.

        It is assumed that 1-st and last lines in the list are not comment lines
        (i.e.  that this text is obtained from
        cards.get_cards(skipcomments=True) generator.
        """

        # Remove in-line comments denoted by $ or &
        res = []
        for l in self.lines:
            res.extend(re_comment.split(l))

        # Remove multiple spaces
        res = ' '.join(res)
        res = re_spaces.sub(' ', res)
        return res

    @card_debugger
    def parts(self):
        """
        Returns a tuple of strings representing different parts of a card.

        How the card is splitted, depends wether it is a cell, surface or a data
        card:

            A cell card is splitted into its name, material, geometry and
            options.

            A surface card is splitted into its name, transformation, type and
            parameters.

            A data card is splitted into its name, type and parameters.
        """
        if self.type == 'c':
            name, mat, geom, opts = cellcard.split(self.content())
            return name, mat, geom, opts

        if self.type == 's':
            name, tr, typ, params = surfacecard.split(self.content())
            return name, tr, typ, params

        if self.type == 'd':
            typ, name, params = datacard.split(self.content())
            return name, typ, params
        else:
            raise NotImplementedError


class MIP:
    """
    Class to read general structure of an MCNP input file.

    When created a new instance, it reads the content of the specified input
    file.  Methods of the class help to access separate blocks and cards of the
    input file.
    """
    def __init__(self, fname, firstblock=None, encoding=None):

        # Text from the input file
        self.text = open(fname, 'r', encoding=encoding).read()

        # Dictioary of indices describing position of blocks
        self.bi = get_block_positions(self.text, firstblock=firstblock)
        return

    def block(self, bid):
        """
        Return text of the specififed block.
        """
        ii, l = self.bi[bid]
        return l, self.text[slice(*ii)]

    def blocks(self, blocks='mtcsd'):
        """
        Generator, returns blocks in the specified order.
        """
        for b in blocks:
            if b in self.bi:
                ii, l = self.bi[b]
                yield b, l, self.text[slice(*ii)]

    def cards(self, blocks='csd', skipcomments=False):
        """
        Generator returns instances of Card class for blocks specified by the
        user.

        The c-comment lines between cards can be skipped if `skipcomments` is
        True.
        """
        for b, n0, txt in self.blocks(blocks):
            for c, n, t in get_cards(txt, skipcomments=skipcomments):
                if t == 'card':
                    t = b
                yield Card(lines=c, position=n0 + n, type=t)


if __name__ == '__main__':
    from sys import argv
    from . import utils

    input = MIP(argv[1])

    print('Start cycling cards', datetime.now().isoformat())
    for c in input.cards():
        print(c.position)
        pass
    print('End   cycling cards', datetime.now().isoformat())

    exit(0)
    # print blocs
    for b, l, txt in input.blocks():
        print(b, l, utils.shorten(repr(txt)))

    # split cards to parts
    for c in input.cards(blocks='csd', skipcomments=True):
        print('*'*60)
        print(c.position)
        print(c.content())
        print(c.parts())
