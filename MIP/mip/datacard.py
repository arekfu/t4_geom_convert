
"""
Split data card into its name, type and the rest parameters.
"""

import re

re_data = re.compile('^\s*(\**[a-zA-Z]+[^0-9]*)([0-9]*)(.*)$')

def split(txt):
    m = re_data.search(txt)
    return m.groups()


def expand_data_card(tokens, *, expected=None, dtype='float'):
    '''Expand the numerical data described by `tokens` into a full list of
    numbers, without any abbreviation.

    :param list(str) tokens: a list of tokens to convert, as strings, in
        reverse order.
    :param expected: the number of expected arguments, or `None` if as many
        tokens as possible should be parsed.
    :param str dtype: the type of the elements of the resulting list, as a
        string. Possible values: ``'int'``, ``'float'`` (default).
    :returns: a pair consisting of a list of expanded data, with type `dtype`,
        and the number of tokens consumed.
    :rtype: (list, int)

    Examples:

    >>> expand_data_card(['1', '3M', '2R'])
    ([1.0, 3.0, 3.0, 3.0], 3)

    Converting to ints:
    >>> expand_data_card(['1', '3M', '2R'], dtype='int')
    ([1, 3, 3, 3], 3)

    :func:`expand_data_card` is case-insensitive:
    >>> expand_data_card(['1', '3m', '2r'], dtype='int')
    ([1, 3, 3, 3], 3)

    >>> expand_data_card(['1', '3M', 'I', '4'])
    ([1.0, 3.0, 3.5, 4.0], 4)
    >>> expand_data_card(['1', '3M', '3M'], dtype='int')
    ([1, 3, 9], 3)
    >>> expand_data_card(['1', '2R', '2I', '2.5'])
    ([1.0, 1.0, 1.0, 1.5, 2.0, 2.5], 4)
    >>> expand_data_card(['1', 'R', '2M'], dtype='int')
    ([1, 1, 2], 3)
    >>> expand_data_card(['1', 'R', 'R'], dtype='int')
    ([1, 1, 1], 3)
    >>> expand_data_card(['1', '2I', '4', '3M'], dtype='int')
    ([1, 2, 3, 4, 12], 4)
    >>> expand_data_card(['1', '2I', '4', '2I', '10'], dtype='int')
    ([1, 2, 3, 4, 6, 8, 10], 5)
    >>> expand_data_card(['0.1', '2ILOG', '0.8'])
    ([0.1, 0.2, 0.4, 0.8], 3)
    >>> expand_data_card(['0.1', '2LOG', '0.8'])
    ([0.1, 0.2, 0.4, 0.8], 3)
    >>> expand_data_card(['0.1', '2j', '0.8'])
    ([0.1, None, None, 0.8], 3)

    Expand until a certain number of values have been collected:

    >>> expand_data_card(['1', '2I', '4', '3M', 'other'],
    ...                  dtype='int', expected=5)
    ([1, 2, 3, 4, 12], 4)
    '''
    if dtype == 'int':
        conv = round
    elif dtype == 'float':
        conv = float
    else:
        raise ValueError('unrecognized dtype: {}'.format(dtype))

    result = []
    tokens = [token.strip().lower() for token in reversed(tokens)]
    consumed = 0
    while tokens and (expected is None or len(result) < expected):
        token = tokens.pop()
        consumed += 1
        last_char = token[-1]
        if last_char == 'r':
            n_reps = int(token[:-1]) if len(token) > 1 else 1
            result.extend([result[-1]]*n_reps)
        elif last_char == 'i':
            result.extend(linspace(result[-1], tokens.pop(), token))
            consumed += 1
        elif last_char == 'm':
            if len(token) == 1:
                raise ValueError('"m" data specifier requires a multiplier')
            factor = float(token[:-1])
            result.append(result[-1] * factor)
        elif last_char == 'j':
            n_reps = int(token[:-1]) if len(token) > 1 else 1
            result.extend([None]*n_reps)
        elif len(token) >= 3 and token[-3:] == 'log':
            result.extend(logspace(result[-1], tokens.pop(), token))
            consumed += 1
        else:
            result.append(float(token))
    if expected is not None and len(result) != expected:
        raise ValueError('expected exactly {:d} items in data card, found {:d}'
                         .format(expected, len(result)))
    return [conv(res) if res is not None else None for res in result], consumed


def linspace(lower_token, upper_token, n_vals_token):
    '''Generate `n_vals` linearly spaced values from `lower` to `upper`,
    including `upper` but not `lower`.

    The values for `lower`, `upper` and `n_vals` are obtained by respectively
    parsing `lower_token`, `upper_token` and `n_vals_token`, that must be
    strings.
    '''
    upper = float(upper_token)
    lower = float(lower_token)
    n_vals = int(n_vals_token[:-1]) if len(n_vals_token) > 1 else 1
    step = (upper - lower) / (n_vals + 1)
    yield from (float(lower+i*step) for i in range(1, n_vals+1))
    yield float(upper)


def logspace(lower_token, upper_token, n_vals_token):
    '''Generate `n_vals` logarithmically spaced values from `lower` to `upper`,
    including `upper` but not `lower`.

    The values for `lower`, `upper` and `n_vals` are obtained by respectively
    parsing `lower_token`, `upper_token` and `n_vals_token`, that must be
    strings.
    '''
    upper = float(upper_token)
    lower = float(lower_token)
    if len(n_vals_token) >= 4 and n_vals_token[-4] == 'i':
        n_vals = int(n_vals_token[:-4]) if len(n_vals_token) > 4 else 1.0
    else:
        n_vals = int(n_vals_token[:-3]) if len(n_vals_token) > 1 else 1.0
    factor = (upper/lower)**(1.0/(n_vals + 1))
    yield from (float(lower*(factor**i)) for i in range(1, n_vals+1))
    yield float(upper)
