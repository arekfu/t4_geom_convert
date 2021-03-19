# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
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
'''Implementation of a simple progress meter.'''


class Progress:  # pylint: disable=too-few-public-methods
    '''A simple progress Meter.'''

    def __init__(self, message, n_items, longest_item):
        self.n_items = n_items
        self.fmt_string = ('\r{message} {{:{max_item_width}d}} '
                           '({{:{n_items_width}d}}/{n_items:d}, '
                           '{{:3d}}%)...'
                           .format(message=message,
                                   n_items=n_items,
                                   max_item_width=len(str(longest_item)),
                                   n_items_width=len(str(n_items))))
        self.prev_percent = -1

    def update(self, iteration, item):
        '''Update the object that we have reached `iteration` and that we are
        treating `item`.

        The :class:`Progress` object will print to stdout if we have
        gained at least one percentage point.
        '''
        percent = (int(100.0 * iteration / (self.n_items - 1))
                   if self.n_items > 1 else 100)
        if percent == self.prev_percent:
            return
        print(self.fmt_string.format(item, iteration + 1, percent), end='',
              flush=True)
        self.prev_percent = percent

    def __enter__(self):
        '''Make :class:`Progress` usable as a context manager.'''
        return self

    def __exit__(self, exc_type, _exc_value, _traceback):
        '''Make :class:`Progress` usable as a context manager.'''
        if exc_type is None:
            print(' done', flush=True)
        return False  # do not suppress exceptions
