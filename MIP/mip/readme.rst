the mip package
==================

This package helps to split an MCNP input file into blocks, cards and card parts.

Example of use::

    from mip import MIP

    # read input file
    input = MIP('inp')

    # Get separate blocks of the input file
    for b, l, txt in input.blocks():
        print 'block {} starting on line {}'.format(b, l)
        print txt 

    # Get cell and surface cards
    for c in input.cards(blocks='cs', skipcomments=True):
        # Metadata of a card
        print 'Card of type {} on line {}'.format(c.type, c.position)
        # Original lines of the card
        print '\n'.join(c.lines)
        # String representing the card with comments removed
        print c.content()
        # The card, splitted into parts:
        p = c.parts()
        if c.type == 'c':
            name, mat, geom, opts = p
            print name, mat, geom, opts
        elif c.type == 's':
            name, tr, st, params = p
            print name, tr, st, params
