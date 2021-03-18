'''Useful tools for debugging.'''

from functools import wraps

def debug(wrapped):
    '''Prints input and output values of any function it decorates.'''
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        print('call to {}:\n  args: {}\n  kwargs: {}'
              .format(wrapped.__name__, args, kwargs))
        ret = wrapped(*args, **kwargs)
        print('  return value: {}'.format(ret))
        return ret
    return wrapper
