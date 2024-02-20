# Copyright 2019-2024 French Alternative Energies and Atomic Energy Commission
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :
'''Useful tools for debugging.'''

from functools import wraps


def debug(wrapped):
    '''Prints input and output values of any function it decorates.'''
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        print(f'call to {wrapped.__name__}:\n  args: {args}\n'
              f'kwargs: {kwargs}')
        ret = wrapped(*args, **kwargs)
        print(f'  return value: {ret}')
        return ret
    return wrapper
