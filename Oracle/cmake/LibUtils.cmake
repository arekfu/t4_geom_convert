# architecture
include(DetectOS)

# set the path to the official T4 prerequisites
set(T4_PREREQUISITES_INSTALL_PATH "/home/tri4dev/developers/prerequisites/install/${OS_ID}"
  CACHE PATH "Path to the installation folder for T4 prerequisites")

# output directory for libraries
set(T4_LIB_OUTPUT_DIR "${CMAKE_BINARY_DIR}/${OS_ID}/lib" CACHE PATH "Output directory for T4 libraries")
# output directory for executables
set(T4_EXE_OUTPUT_DIR "${CMAKE_BINARY_DIR}/${OS_ID}/bin" CACHE PATH "Output directory for T4 executables")
mark_as_advanced(T4_LIB_OUTPUT_DIR T4_EXE_OUTPUT_DIR)

########################
# functions start here #
########################

function(prepend VAR PREFIX)
  if(PREFIX)
    set(LISTVAR "")
    foreach(F ${ARGN})
      list(APPEND LISTVAR "${PREFIX}/${F}")
    endforeach(F)
    set(${VAR} "${LISTVAR}" PARENT_SCOPE)
  endif()
endfunction(prepend)

function(is_even N VAR)
  math(EXPR REMAINDER "(${N}+1)%2")
  set(${VAR} ${REMAINDER} PARENT_SCOPE)
endfunction()

function(has_even_length _LIST VAR)
  list(LENGTH _LIST _N)
  is_even(${_N} _EVEN)
  set(${VAR} ${_EVEN} PARENT_SCOPE)
endfunction()

include(CMakeParseArguments)
include(GNUInstallDirs)

# Helper function to add libraries.
#
# t4_add_library(<libname>
#   [SOURCES_PATH path]
#   [SOURCES source1 [source2 ...]]
#   [SOURCES_WARNINGS source1 [source2 ...]]
#   [SOURCES_OUTSIDE_PATH source1 [source2 ...]]
#   [INCLUDE_DIRS dir1 [dir2 ...]]
#   [DEFINITIONS def1 [def2 ...]]
#   [COMPILE_OPTIONS flag1 [flag2 ...]]
#   [LINK_LIBRARIES lib1 [lib2 ...]]
#  )
#
# The SOURCES option specifies the list of source files for the library
# <libname>. The SOURCES_WARNINGS option adds source files and activates
# several compilation warnings (-Wall on gcc/g++). If the files specified with
# SOURCES or SOURCES_WARNINGS are all in the same directory, the path can be
# omitted from the file names and specified only once using the SOURCES_PATH
# option.  The SOURCES_OUTSIDE_PATH option can then be used to specify
# additional source files that do not reside in SOURCES_PATH (this is useful
# for generated files, such as ROOT dictionaries).
#
# INCLUDE_DIRS specifies the list of include directories for <libname>. Any
# target linking to <libname> will also automatically inherit its include
# directories.
#
# DEFINITIONS specifies the list of preprocessor definitions for <libname>.
# Any target linking to <libname> will also automatically inherit its
# preprocessor definitions.
#
# COMPILE_OPTIONS specifies the list of compiler flags for <libname>. Any target
# linking to <libname> will also automatically inherit its compiler flags.
#
# LINK_LIBRARIES specifies the list of targets (libraries) that <libname> links
# to, and depends on.
function(t4_add_library LIBNAME)
  cmake_parse_arguments(T4
    ""
    "SOURCES_PATH"
    "SOURCES;SOURCES_WARNINGS;SOURCES_OUTSIDE_PATH;INCLUDE_DIRS;DEFINITIONS;COMPILE_OPTIONS;LINK_LIBRARIES"
    ${ARGN})

  if(T4_UNPARSED_ARGUMENTS)
    message(WARNING "Unrecognized arguments to t4_add_library: ${T4_UNPARSED_ARGUMENTS}")
  endif()

  # convert sources path to relative paths
  if(IS_ABSOLUTE "${T4_SOURCES_PATH}")
    file(RELATIVE_PATH T4_SOURCES_PATH "${CMAKE_CURRENT_SOURCE_DIR}" "${T4_SOURCES_PATH}")
  endif()

  # convert include paths to absolute paths
  set(T4_INCLUDE_DIRS_LOOP "${T4_INCLUDE_DIRS}")
  unset(T4_INCLUDE_DIRS)
  foreach(DIR IN LISTS T4_INCLUDE_DIRS_LOOP)
    get_filename_component(DIR_ABS "${DIR}" ABSOLUTE)
    list(APPEND T4_INCLUDE_DIRS "${DIR_ABS}")
  endforeach()

  # massage paths by adding a common prefix
  prepend(T4_SOURCES "${T4_SOURCES_PATH}" ${T4_SOURCES})
  prepend(T4_SOURCES_WARNINGS "${T4_SOURCES_PATH}" ${T4_SOURCES_WARNINGS})

  # set high-verbosity warning compiler flags for the given source files
  set_source_files_properties(${T4_SOURCES_WARNINGS} PROPERTIES COMPILE_FLAGS "${WARNINGS_FLAGS}")
  if(T4_WARNINGS_ALL)
    set_source_files_properties(${T4_SOURCES} PROPERTIES COMPILE_FLAGS "${WARNINGS_FLAGS}")
  endif()

  # define the library
  add_library(${LIBNAME} ${T4_SOURCES} ${T4_SOURCES_OUTSIDE_PATH} ${T4_SOURCES_WARNINGS})
  if(T4_INCLUDE_DIRS)
    foreach(DIR IN LISTS T4_INCLUDE_DIRS)
      target_include_directories(${LIBNAME} PUBLIC
        $<BUILD_INTERFACE:${DIR}>
        $<INSTALL_INTERFACE:include/>)
    endforeach()
  endif()
  if(T4_DEFINITIONS)
    target_compile_definitions(${LIBNAME} PUBLIC ${T4_DEFINITIONS})
  endif()
  if(T4_COMPILE_OPTIONS)
    target_compile_options(${LIBNAME} PUBLIC ${T4_COMPILE_OPTIONS})
  endif()
  if(T4_LINK_LIBRARIES)
    target_link_libraries(${LIBNAME} PUBLIC "${T4_LINK_LIBRARIES}")
  endif()

  # set the output directory for static and dynamic builds
  set_target_properties(${LIBNAME} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${T4_LIB_OUTPUT_DIR}
    ARCHIVE_OUTPUT_DIRECTORY ${T4_LIB_OUTPUT_DIR})

  install(TARGETS ${LIBNAME}
    EXPORT T4Config
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    )
  install(DIRECTORY "${T4_SOURCES_PATH}/"
          DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
          FILES_MATCHING PATTERN "*.hh")
endfunction()

# Helper function to add executables.
#
# t4_add_executable(<exe_name>
#   [SOURCES_PATH path]
#   [SOURCES source1 [source2 ...]]
#   [SOURCES_WARNINGS source1 [source2 ...]]
#   [SOURCES_OUTSIDE_PATH source1 [source2 ...]]
#   [INCLUDE_DIRS dir1 [dir2 ...]]
#   [DEFINITIONS def1 [def2 ...]]
#   [COMPILE_OPTIONS flag1 [flag2 ...]]
#   [LINK_LIBRARIES lib1 [lib2 ...]]
#  )
#
# See t4_add_library for the meaning of the options
function(t4_add_executable EXENAME)
  cmake_parse_arguments(T4
    "EXCLUDE_FROM_ALL"
    "SOURCES_PATH"
    "SOURCES;SOURCES_WARNINGS;SOURCES_OUTSIDE_PATH;INCLUDE_DIRS;DEFINITIONS;COMPILE_OPTIONS;LINK_LIBRARIES"
    ${ARGN})

  if(T4_EXCLUDE_FROM_ALL)
    set(EXCLUDE_FROM_ALL_ARG EXCLUDE_FROM_ALL)
  else()
    unset(EXCLUDE_FROM_ALL_ARG)
  endif()

  # convert sources path to relative paths
  if(IS_ABSOLUTE "${T4_SOURCES_PATH}")
    file(RELATIVE_PATH T4_SOURCES_PATH "${CMAKE_CURRENT_SOURCE_DIR}" "${T4_SOURCES_PATH}")
  endif()

  # convert include paths to absolute paths
  set(T4_INCLUDE_DIRS_LOOP "${T4_INCLUDE_DIRS}")
  unset(T4_INCLUDE_DIRS)
  foreach(DIR IN LISTS T4_INCLUDE_DIRS_LOOP)
    get_filename_component(DIR_ABS "${DIR}" ABSOLUTE)
    list(APPEND T4_INCLUDE_DIRS "${DIR_ABS}")
  endforeach()

  # massage paths by adding a common prefix
  prepend(T4_SOURCES "${T4_SOURCES_PATH}" ${T4_SOURCES})
  prepend(T4_SOURCES_WARNINGS "${T4_SOURCES_PATH}" ${T4_SOURCES_WARNINGS})

  # set high-verbosity warning compiler flags for the given source files
  set_source_files_properties(${T4_SOURCES_WARNINGS} PROPERTIES COMPILE_FLAGS "${WARNINGS_FLAGS}")
  if(T4_WARNINGS_ALL)
    set_source_files_properties(${T4_SOURCES} PROPERTIES COMPILE_FLAGS "${WARNINGS_FLAGS}")
  endif()

  # define the executable
  add_executable(${EXENAME} ${EXCLUDE_FROM_ALL_ARG} ${T4_UNPARSED_ARGUMENTS}
    ${T4_SOURCES} ${T4_SOURCES_OUTSIDE_PATH} ${T4_SOURCES_WARNINGS})
  if(T4_INCLUDE_DIRS)
    foreach(DIR IN LISTS T4_INCLUDE_DIRS)
      target_include_directories(${EXENAME} PUBLIC
        $<BUILD_INTERFACE:${T4_INCLUDE_DIRS}>
        $<INSTALL_INTERFACE:include/>)
    endforeach()
  endif()
  if(T4_DEFINITIONS)
    target_compile_definitions(${EXENAME} PUBLIC ${T4_DEFINITIONS})
  endif()
  if(T4_COMPILE_OPTIONS)
    target_compile_options(${EXENAME} PUBLIC ${T4_COMPILE_OPTIONS})
  endif()
  if(T4_LINK_LIBRARIES)
    target_link_libraries(${EXENAME} LINK_PUBLIC "${T4_LINK_LIBRARIES}")
  endif()

  # set the output directory
  set_target_properties(${EXENAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${T4_EXE_OUTPUT_DIR})

  if(NOT T4_EXCLUDE_FROM_ALL)
    install(TARGETS ${EXENAME}
      EXPORT T4Config
      RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
  endif()
endfunction()

# helper function to define imported libraries
function(define_imported_target TARGET_NAME)
  if(TARGET ${TARGET_NAME})
    return()
  endif()

  cmake_parse_arguments(TARGET
    ""
    "VERSION"
    "INCLUDE_DIRS;COMPILE_DEFINITIONS;COMPILE_OPTIONS;LINK_LIBRARIES"
    ${ARGN})

  # create the library
  add_library(${TARGET_NAME} INTERFACE IMPORTED)

  message(STATUS "${TARGET_NAME} dependency found:")
  if(TARGET_VERSION)
    message(STATUS "  ... version: ${TARGET_VERSION}")
  endif()
  if(TARGET_INCLUDE_DIRS)
    message(STATUS "  ... include dirs: ${TARGET_INCLUDE_DIRS}")
    set_target_properties(${TARGET_NAME}
      PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES "${TARGET_INCLUDE_DIRS}"
      INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${TARGET_INCLUDE_DIRS}"
      )
  endif()
  if(TARGET_COMPILE_DEFINITIONS)
    message(STATUS "  ... definitions: ${TARGET_COMPILE_DEFINITIONS}")
    set_target_properties(${TARGET_NAME}
      PROPERTIES INTERFACE_COMPILE_DEFINITIONS "${TARGET_COMPILE_DEFINITIONS}"
      )
  endif()
  if(TARGET_COMPILE_OPTIONS)
    message(STATUS "  ... compile options: ${TARGET_COMPILE_OPTIONS}")
    set_target_properties(${TARGET_NAME}
      PROPERTIES INTERFACE_COMPILE_OPTIONS "${TARGET_COMPILE_OPTIONS}"
      )
  endif()
  if(TARGET_LINK_LIBRARIES)
    message(STATUS "  ... link libraries: ${TARGET_LINK_LIBRARIES}")
    set_target_properties(${TARGET_NAME}
      PROPERTIES INTERFACE_LINK_LIBRARIES "${TARGET_LINK_LIBRARIES}"
      )
  endif()

  # install library along with T4
  ship_libraries(${TARGET_LINK_LIBRARIES})
endfunction()

function(import_ROOT_library VAR)
  # try in Config mode first
  if(T4_STRICT_DEPENDENCIES)
    find_package(ROOT ${ROOT_VERSION_REQUIRED} ${ARGN}
      QUIET
      HINTS "$ENV{ROOTSYS}/cmake"
      EXACT)
  else()
    find_package(ROOT ${ROOT_VERSION_REQUIRED} ${ARGN}
      QUIET
      HINTS "$ENV{ROOTSYS}/cmake")
  endif()
  if(NOT ROOT_FOUND)
    # fall back to module mode if necessary
    if(EXISTS $ENV{ROOTSYS})
      list(APPEND CMAKE_MODULE_PATH "$ENV{ROOTSYS}/etc/cmake")
    endif()

    if(T4_STRICT_DEPENDENCIES)
      find_package(ROOT ${ROOT_VERSION_REQUIRED} ${ARGN} EXACT)
    else()
      find_package(ROOT ${ROOT_VERSION_REQUIRED} ${ARGN})
    endif()
  endif()
  if(ROOT_FOUND)
    mark_as_advanced(ROOT_DIR)
  else()
    return()
  endif()

  message(STATUS "ROOT_CXX_FLAGS: ${ROOT_CXX_FLAGS}")
  message(STATUS "ROOT_DEFINITIONS: ${ROOT_DEFINITIONS}")
  # extract the real macro definitions from the list
  separate_arguments(ROOT_DEFINITIONS)
  string(REGEX MATCHALL "(^|;)-D[^;]*" ROOT_DEFINITIONS "${ROOT_DEFINITIONS}")
  string(REGEX REPLACE "(^|;)-D" "\\1" ROOT_DEFINITIONS "${ROOT_DEFINITIONS}")
  string(REGEX REPLACE " +" " " ROOT_CXX_FLAGS "${ROOT_CXX_FLAGS}")
  string(REGEX REPLACE "^ +" "" ROOT_CXX_FLAGS "${ROOT_CXX_FLAGS}")
  string(REGEX REPLACE "-std=c[^ ]*" "" ROOT_CXX_FLAGS "${ROOT_CXX_FLAGS}")
  separate_arguments(ROOT_CXX_FLAGS)

  if(ROOT_rootcint_CMD)
    set(ROOTCINT_EXECUTABLE ${ROOT_rootcint_CMD} CACHE FILEPATH "Path to the rootcint executable" FORCE)
  elseif(ROOT_EXECUTABLE)
    set(ROOTCINT_EXECUTABLE ${ROOTCINT_EXECUTABLE} CACHE FILEPATH "Path to the rootcint executable" FORCE)
  endif()
  mark_as_advanced(ROOTCINT_EXECUTABLE)

  if(ROOT_FOUND)
    define_imported_target(ROOT
      VERSION "${ROOT_VERSION}"
      INCLUDE_DIRS "${ROOT_INCLUDE_DIRS}"
      COMPILE_DEFINITIONS "HAS_ROOT;HAS_PYROOT;${ROOT_DEFINITIONS}"
      COMPILE_OPTIONS "${ROOT_CXX_FLAGS}"
      LINK_LIBRARIES "${ROOT_LIBRARIES}"
      )
    message(STATUS "  ... rootcint: ${ROOTCINT_EXECUTABLE}")
  else()
    message(STATUS "ROOT: not found")
  endif()
  set(${VAR} ${ROOT_FOUND} PARENT_SCOPE)
endfunction()

function(import_Geant4_library VAR)
  import_dl_library(DL_FOUND)
  if(NOT DL_FOUND)
    message(WARNING "Could not find required dependency DL for Geant4")
    set(${VAR} FALSE PARENT_SCOPE)
    return()
  endif()

  if(T4_STRICT_DEPENDENCIES)
    find_package(Geant4 ${Geant4_VERSION_REQUIRED} ${ARGN} EXACT)
  else()
    find_package(Geant4 ${Geant4_VERSION_REQUIRED} ${ARGN})
  endif()

  # remove -D from the list of definitions
  string(REGEX REPLACE "(^|;)-D" "\\1" Geant4_DEFINITIONS "${Geant4_DEFINITIONS}")
  string(REGEX REPLACE "(-std=.*)" "" Geant4_CXX_FLAGS "${Geant4_CXX_FLAGS}")
  string(REGEX REPLACE " +" " " Geant4_CXX_FLAGS ${Geant4_CXX_FLAGS})
  string(REGEX REPLACE "^ +" "" Geant4_CXX_FLAGS ${Geant4_CXX_FLAGS})
  separate_arguments(Geant4_CXX_FLAGS)

  if(Geant4_FOUND)
    define_imported_target(Geant4
      VERSION "${Geant4_VERSION}"
      INCLUDE_DIRS "${Geant4_INCLUDE_DIRS}"
      COMPILE_DEFINITIONS "HAS_G4;${Geant4_DEFINITIONS};$<TARGET_PROPERTY:DL,INTERFACE_COMPILE_DEFINITIONS>"
      COMPILE_OPTIONS "${Geant4_CXX_FLAGS}"
      LINK_LIBRARIES "${Geant4_LIBRARIES};$<TARGET_PROPERTY:DL,INTERFACE_LINK_LIBRARIES>"
      )
  else()
    message(STATUS "Geant4: not found")
  endif()
  set(${VAR} ${Geant4_FOUND} PARENT_SCOPE)
endfunction()

function(import_X11_library VAR)
  find_package(X11 ${ARGN})
  if(X11_FOUND)
    define_imported_target(X11
      INCLUDE_DIRS "${X11_INCLUDE_DIR}"
      COMPILE_DEFINITIONS "HAS_XLIB"
      LINK_LIBRARIES "${X11_LIBRARIES}"
      )
  else()
    message(STATUS "X11: not found")
  endif()
  set(${VAR} ${X11_FOUND} PARENT_SCOPE)
endfunction()

function(import_LAPACK_library VAR)
  if(T4_STRICT_DEPENDENCIES)
    find_package(LAPACK ${LAPACK_VERSION_REQUIRED} EXACT ${ARGN})
  else()
    find_package(LAPACK ${LAPACK_VERSION_REQUIRED} ${ARGN})
  endif()
  if(LAPACK_FOUND)
    define_imported_target(LAPACK
      COMPILE_DEFINITIONS "T4_LAPACK"
      LINK_LIBRARIES "${LAPACK_LIBRARIES}"
      )
  else()
    message(STATUS "LAPACK: not found")
  endif()
  set(${VAR} ${LAPACK_FOUND} PARENT_SCOPE)
endfunction()

function(import_HDF5_library VAR)

  file(GLOB T4_HDF5_INSTALL_DIRS "${T4_PREREQUISITES_INSTALL_PATH}/hdf5*")
  if(T4_HDF5_INSTALL_DIRS)
    message(STATUS "Will look for HDF5 in ${T4_HDF5_INSTALL_DIRS}")
  endif()

  # is the package required?
  list(FIND ARGN "REQUIRED" IS_REQUIRED)
  if(IS_REQUIRED EQUAL -1)
    set(REQUIRED_FLAG "")
  else()
    set(REQUIRED_FLAG "REQUIRED")
  endif()

  set(HDF5_FOUND FALSE)
  if(T4_HDF5_INSTALL_DIRS)
    list(APPEND T4_HDF5_INSTALL_DIRS "")
  else()
    set(T4_HDF5_INSTALL_DIRS ";")       # a one-element list with an empty value
  endif()
  if(HDF5_DIR)
    list(INSERT T4_HDF5_INSTALL_DIRS 0 "${HDF5_DIR}")
  endif()
  foreach(T4_HDF5_INSTALL_DIR IN LISTS T4_HDF5_INSTALL_DIRS)
    if(T4_HDF5_INSTALL_DIR STREQUAL "")
      unset(ENV{HDF5_ROOT})
    else()
      unset(HDF5_ROOT)
      set(ENV{HDF5_ROOT} "${T4_HDF5_INSTALL_DIR}")
    endif()
    if(T4_STRICT_DEPENDENCIES)
      find_package(HDF5 ${HDF5_VERSION_REQUIRED} ${REQUIRED_FLAG} EXACT)
    else()
      find_package(HDF5 ${HDF5_VERSION_REQUIRED} ${REQUIRED_FLAG})
    endif()
    if(HDF5_FOUND)
      break()
    endif()
  endforeach()
  mark_as_advanced(HDF5_DIR)

  # imported target for HDF5
  if(HDF5_FOUND)
    define_imported_target(HDF5
      INCLUDE_DIRS "${HDF5_INCLUDE_DIRS}"
      LINK_LIBRARIES "${HDF5_C_LIBRARIES}"
      )
  else()
    message(STATUS "HDF5: not found")
  endif()
  set(${VAR} ${HDF5_FOUND} PARENT_SCOPE)
endfunction()

function(import_XTools_library VAR)

  import_HDF5_library(HDF5_FOUND)
  if(NOT HDF5_FOUND)
    message(WARNING "Could not find required dependency HDF5 for XTools")
    set(${VAR} FALSE PARENT_SCOPE)
    return()
  endif()

  set(XTOOLS_INSTALL_DIRS "/home/xtools/MinorReleases/XTools-${XTools_VERSION_REQUIRED}")
  set(T4_XTOOLS_INSTALL_DIRS "${T4_PREREQUISITES_INSTALL_PATH}/XTools-${XTools_VERSION_REQUIRED}")
  message(STATUS "Will look for XTools in ${T4_XTOOLS_INSTALL_DIRS};${XTOOLS_INSTALL_DIRS}")

  # is the package required?
  list(FIND ARGN "REQUIRED" IS_REQUIRED)

  set(XTOOLS_LIBRARY NOTFOUND)
  find_library(XTOOLS_LIBRARY libxtools_no_omp.a
    PATHS "${T4_XTOOLS_INSTALL_DIRS}" "${XTOOLS_INSTALL_DIRS}"
    PATH_SUFFIXES lib lib/lin-x86-64)

  # imported target for XTOOLS
  if(XTOOLS_LIBRARY)
    define_imported_target(XTools
      LINK_LIBRARIES "${XTOOLS_LIBRARY};HDF5"
      )
    set(${VAR} TRUE PARENT_SCOPE)
  else()
    message(STATUS "XTools: not found")
    set(${VAR} FALSE PARENT_SCOPE)
  endif()
endfunction()

function(import_MEDFile23_library VAR)
  import_HDF5_library(HDF5_FOUND)
  if(NOT HDF5_FOUND)
    message(WARNING "Could not find required dependency HDF5 for MEDFile")
    set(${VAR} FALSE PARENT_SCOPE)
    return()
  endif()

  if(T4_STRICT_DEPENDENCIES)
    find_package(MEDFile ${MEDFile_VERSION_REQUIRED} EXACT ${ARGN})
  else()
    find_package(MEDFile ${MEDFile_VERSION_REQUIRED} ${ARGN})
  endif()
  # Tripoli-4 uses the MEDFile API v2.3; jump through some hoops to set the
  # correct include path
  foreach(INCLUDE_DIR ${MEDFILE_INCLUDE_DIRS})
    set(MEDFILE_23_INCLUDE_DIRS "${MEDFILE_23_INCLUDE_DIRS}" "${INCLUDE_DIR}/2.3.6")
  endforeach()

  if(MEDFILE_FOUND)
    define_imported_target(MEDFile23
      INCLUDE_DIRS "${MEDFILE_23_INCLUDE_DIRS}"
      COMPILE_DEFINITIONS "HAS_MED;MED_API_23=1"
      COMPILE_OPTIONS "${MEDFILE_CXX_FLAGS}"
      LINK_LIBRARIES "${MEDFILE_LIBRARIES};HDF5"
      )
  else()
    message(STATUS "MEDFile: not found")
  endif()
  set(${VAR} ${MEDFILE_FOUND} PARENT_SCOPE)
endfunction()

function(import_MENDEL_library VAR)
  import_XTools_library(XTOOLS_FOUND)
  if(NOT XTOOLS_FOUND)
    message(SEND_ERROR "Could not find required dependency XTools for MENDEL")
    set(${VAR} FALSE PARENT_SCOPE)
    return()
  endif()

  # we require a given version of MENDEL if T4_STRICT_DEPENDENCIES is set;
  # however, currently MENDEL does not actually expose its version number
  if(T4_STRICT_DEPENDENCIES)
    find_package(MENDEL EXACT ${ARGN})
  else()
    find_package(MENDEL ${ARGN})
  endif()

  if(MENDEL_FOUND)
    define_imported_target(MENDEL
      INCLUDE_DIRS "${MENDEL_INCLUDE_DIRS};$<TARGET_PROPERTY:XTools,INTERFACE_INCLUDE_DIRECTORIES>"
      COMPILE_DEFINITIONS "$<TARGET_PROPERTY:XTools,INTERFACE_COMPILE_DEFINITIONS>"
      COMPILE_OPTIONS "$<TARGET_PROPERTY:XTools,INTERFACE_COMPILE_OPTIONS>"
      LINK_LIBRARIES "${MENDEL_LIBRARIES};$<TARGET_PROPERTY:XTools,INTERFACE_LINK_LIBRARIES>"
      )
  else()
    message(STATUS "MENDEL: not found")
  endif()

  set(${VAR} ${MENDEL_FOUND} PARENT_SCOPE)
endfunction()

function(import_Boost_library VAR)
  if(T4_STRICT_DEPENDENCIES)
    find_package(Boost ${Boost_VERSION_REQUIRED} EXACT ${ARGN})
  else()
    find_package(Boost ${Boost_VERSION_REQUIRED} ${ARGN})
  endif()

  if(Boost_FOUND)
    define_imported_target(Boost
      INCLUDE_DIRS "${Boost_INCLUDE_DIRS}"
      )
  else()
    message(STATUS "Boost: not found")
  endif()

  set(${VAR} ${Boost_FOUND} PARENT_SCOPE)
endfunction()

function(import_dl_library VAR)
  cmake_parse_arguments(T4 "REQUIRED" "" "" ${ARGN})

  find_library(DL_LIB dl)
  if(NOT DL_LIB)
    if(T4_REQUIRED)
      message(FATAL_ERROR "libdl was required, but could not be found")
    else()
      message(WARNING "libdl was required, but could not be found")
    endif()
  endif()
  mark_as_advanced(DL_LIB)

  if(DL_LIB)
    define_imported_target(DL
      COMPILE_DEFINITIONS "HAS_DL"
      LINK_LIBRARIES "${DL_LIB}"
      )
    set(${VAR} TRUE PARENT_SCOPE)
  else()
    message(STATUS "dl: not found")
    set(${VAR} FALSE PARENT_SCOPE)
  endif()

endfunction()

function(import_MPI_library VAR)
  find_package(MPI ${ARGN})

  if(MPI_CXX_FOUND)
    string(REGEX REPLACE "^ " "" MPI_CXX_COMPILE_FLAGS "${MPI_CXX_COMPILE_FLAGS}")
    string(REGEX REPLACE "^ " "" MPI_CXX_LINK_FLAGS "${MPI_CXX_LINK_FLAGS}")
    define_imported_target(MPI
      INCLUDE_DIRS ${MPI_CXX_INCLUDE_PATH}
      COMPILE_DEFINITIONS HAS_MPI
      COMPILE_OPTIONS ${MPI_CXX_COMPILE_FLAGS}
      LINK_LIBRARIES ${MPI_CXX_LINK_FLAGS} ${MPI_CXX_LIBRARIES}
      )
  else()
    message(STATUS "MPI: not found")
  endif()

  set(${VAR} ${MPI_FOUND} PARENT_SCOPE)
endfunction()

# Optionally include third-party libraries into packaged .deb and .rpm
# archives. The logic is handled by the ship_library function.
option(T4_SHIP_THIRD_PARTY_LIBS "Include third-party libraries in generated packages" OFF)
mark_as_advanced(T4_SHIP_THIRD_PARTY_LIBS)

function(ship_libraries)
  if(T4_SHIP_THIRD_PARTY_LIBS)
    set(REAL_LIBS)
    foreach(LIB IN LISTS ARGN)
      get_filename_component(REAL_LIB ${LIB} REALPATH)
      get_filename_component(LIBNAME ${LIB} NAME)
      install(FILES ${REAL_LIB} RENAME ${LIBNAME} DESTINATION ${CMAKE_INSTALL_LIBDIR})
    endforeach()
  endif()
endfunction()
