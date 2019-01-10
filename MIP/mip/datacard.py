
"""
Split data card into its name, type and the rest parameters.
"""

import re

re_data = re.compile('^\s*(\**[a-zA-Z]+[^0-9]*)([0-9]*)(.*)$')

def split(txt):
    m = re_data.search(txt)
    return m.groups()
