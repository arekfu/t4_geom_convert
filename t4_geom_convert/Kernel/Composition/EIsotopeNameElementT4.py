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

from enum import Enum

EIsotopeNameElement = Enum('EIsotopeNameElement', 'H HE LI BE B C N O F NE NA '
                           'MG AL SI P S CL AR K CA SC TI V CR MN FE CO NI CU '
                           'ZN GA GE AS SE BR KR RB SR Y ZR NB MO TC RU RH PD '
                           'AG CD IN SN SB TE I XE CS BA LA CE PR ND PM SM EU '
                           'GD TB DY HO ER TM YB LU HF TA W RE OS IR PT AU HG '
                           'TL PB BI PO AT RN FR RA AC TH PA U NP PU AM CM BK '
                           'CF ES FM MD NO LR RF DB SG BH HS MT DS RG CN NH '
                           'FL MC LV TS OG')
