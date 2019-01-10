import re


def shorten(s, N=80):
    """
    Return short representation of string s.
    """
    if len(s) <= N:
        return s[:]
    else:
        l = (N - 5)/2
        return '{} ... {}'.format(s[:l], s[-l:])


def newlineindex(mlstring, start=0):
    """
    Return two indices, for the end of the 1-st line and start of the next one.
    """
    r = re.compile('[\r\n]+')
    m = r.search(mlstring, start)
    return m.start(), m.end()


def nol(txt, start=None, end=None):
    """
    Return number of lines in the multi-line string txt.
    """
    if start is None:
        start = 0
    if end is None:
        end = len(txt)
    if '\r' in txt:
        return txt.count('\r', start, end) + 1
    else:
        return txt.count('\n', start, end) + 1
