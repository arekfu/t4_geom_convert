'''The module containing the :class:`Abundances` class.'''


class Abundances:  # pylint: disable=too-few-public-methods
    '''A class that represents a set of isotopes, along with their
    abundances.'''

    def __init__(self, isotopes, atom_fracs):
        '''Create a :class:`Abundances`.

        :param isotopes: the isotopes in the composition, along with their
                         abundances.
        :type isotopes: list((str, float))
        :param bool atom_fracs: `True` if the abundances represent atomic
                                fractions, `False` if they represent mass
                                fractions.
        '''
        if not isinstance(isotopes, list):
            raise ValueError('Expecting a list in Abundances, got a {}: {}'
                             .format(type(isotopes), isotopes))
        self.isotopes = isotopes.copy()
        self.atom_fracs = atom_fracs
