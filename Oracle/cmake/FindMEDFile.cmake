# - Find MED file installation
#
# The following variable are set:
#   MEDFILE_INCLUDE_DIRS
#   MEDFILE_LIBRARIES
#   MEDFILE_C_LIBRARIES
#   MEDFILE_F_LIBRARIES
#
#  The CMake (or environment) variable MEDFILE_ROOT_DIR can be set to
#  guide the detection and indicate a root directory to look into.
#
############################################################################
# Copyright (C) 2007-2014  CEA/DEN, EDF R&D, OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

# ------

MESSAGE(STATUS "Looking for MEDFile...")

# ------

file(GLOB T4_MEDFILE_INSTALL_DIRS "${T4_PREREQUISITES_INSTALL_PATH}/med*")
set(T4_MEDFILE_INSTALL_DIRS "${T4_PREREQUISITES_INSTALL_PATH}/med-${MEDFile_VERSION_REQUIRED}" "${T4_MEDFILE_INSTALL_DIRS}")
message(STATUS "Will look for MEDFile in ${T4_MEDFILE_INSTALL_DIRS}")

FIND_PATH(MEDFILE_INCLUDE_DIRS med.h
  PATHS ENV MED_PREFIX ENV MEDFILE_ROOT_DIR ${T4_MEDFILE_INSTALL_DIRS}
  PATH_SUFFIXES include)
#FIND_PROGRAM(MDUMP mdump)
FIND_LIBRARY(MEDFILE_C_LIBRARIES NAMES medC
  PATHS ENV MED_PREFIX ENV MEDFILE_ROOT_DIR ${T4_MEDFILE_INSTALL_DIRS}
  PATH_SUFFIXES lib)

#FIND_LIBRARY(MEDFILE_F_LIBRARIES NAMES med
#  PATHS ENV MED_PREFIX ENV MEDFILE_ROOT_DIR ${T4_MEDFILE_INSTALL_DIRS}
#  PATH_SUFFIXES lib)
#IF(MEDFILE_F_LIBRARIES)
#  SET(MEDFILE_LIBRARIES ${MEDFILE_C_LIBRARIES} ${MEDFILE_F_LIBRARIES})
#ELSE(MEDFILE_F_LIBRARIES)
#  SET(MEDFILE_LIBRARIES ${MEDFILE_C_LIBRARIES})
#ENDIF(MEDFILE_F_LIBRARIES)

SET(MEDFILE_LIBRARIES ${MEDFILE_C_LIBRARIES})

INCLUDE(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MEDFILE REQUIRED_VARS MEDFILE_INCLUDE_DIRS MEDFILE_C_LIBRARIES)
mark_as_advanced(MEDFILE_C_LIBRARIES MEDFILE_INCLUDE_DIRS)
