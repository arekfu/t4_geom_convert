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

class CTransformationMCNP:
    '''Class which permit to access precisely to the information of the
    transformation part of the block DATA.'''

    def __init__(self, l_originTransformation, l_rotationTransformation):
        '''
        Constructor
        :param: l_originTransformation : list of the coordinates points of
        the new cartesian axes
        :param: l_rotationTransformation : coordinates of the matrix of rotation
        '''
        self.originTransformation = l_originTransformation
        self.rotationTransformation = l_rotationTransformation
