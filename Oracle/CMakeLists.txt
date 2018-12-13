# CMake file for the Visualizer library
cmake_minimum_required(VERSION 3.2)
project(OracleMCNPT4 C CXX)

message(STATUS "********** OracleMCNPT4 ********** ")

# Path for cmake files shipped with the project
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

find_package(T4 REQUIRED)

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
endfunction()

function(import_ROOT_library VAR)
  # try in Config mode first
  find_package(ROOT ${ARGN}
    QUIET
    HINTS "$ENV{ROOTSYS}/cmake")
  if(NOT ROOT_FOUND)
    # fall back to module mode if necessary
    if(EXISTS $ENV{ROOTSYS})
      list(APPEND CMAKE_MODULE_PATH "$ENV{ROOTSYS}/etc/cmake")
    endif()

    find_package(ROOT ${ROOT_VERSION_REQUIRED} ${ARGN})
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
      COMPILE_DEFINITIONS "HAS_ROOT;${ROOT_DEFINITIONS}"
      COMPILE_OPTIONS "${ROOT_CXX_FLAGS}"
      LINK_LIBRARIES "${ROOT_LIBRARIES}"
      )
    message(STATUS "  ... rootcint: ${ROOTCINT_EXECUTABLE}")
  else()
    message(STATUS "ROOT: not found")
  endif()
  set(${VAR} ${ROOT_FOUND} PARENT_SCOPE)
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


function(compilation_info TARGET)
  message(STATUS "compilation info for target: " ${TARGET})

  # COMPILE_DEFINITIONS
  get_target_property(TARGET_COMPILE_DEFINITIONS "${TARGET}" COMPILE_DEFINITIONS)
  if(TARGET_COMPILE_DEFINITIONS)
    message(STATUS " ... compile definitions: ${TARGET_COMPILE_DEFINITIONS}")
  endif()

  # COMPILE_OPTIONS
  get_target_property(TARGET_COMPILE_OPTIONS "${TARGET}" COMPILE_OPTIONS)
  if(TARGET_COMPILE_OPTIONS)
    message(STATUS " ... compile options: ${TARGET_COMPILE_OPTIONS}")
  endif()

  # INCLUDE_DIRECTORIES
  get_target_property(TARGET_INCLUDE_DIRECTORIES "${TARGET}" INCLUDE_DIRECTORIES)
  if(TARGET_INCLUDE_DIRECTORIES)
    message(STATUS " ... include directories: ${TARGET_INCLUDE_DIRECTORIES}")
  endif()

  # INTERFACE_INCLUDE_DIRECTORIES
  get_target_property(TARGET_INTERFACE_INCLUDE_DIRECTORIES "${TARGET}" INTERFACE_INCLUDE_DIRECTORIES)
  if(TARGET_INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS " ... interface include directories: ${TARGET_INTERFACE_INCLUDE_DIRECTORIES}")
  endif()

  # LINK_LIBRARIES
  get_target_property(TARGET_LINK_LIBRARIES "${TARGET}" LINK_LIBRARIES)
  if(TARGET_LINK_LIBRARIES)
    message(STATUS " ... link libraries: ${TARGET_LINK_LIBRARIES}")
  endif()
endfunction()

# ROOT
import_ROOT_library(ROOT_FOUND COMPONENTS Geom)
# DL
import_dl_library(DL_FOUND REQUIRED)

###############
#    gtest    #
###############
# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
                 ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
                 EXCLUDE_FROM_ALL)

# The gtest/gtest_main targets carry header search path
# dependencies automatically when using CMake 2.8.11 or
# later. Otherwise we have to add them here ourselves.
if (CMAKE_VERSION VERSION_LESS 2.8.11)
  include_directories("${gtest_SOURCE_DIR}/include")
endif()

###############
# executables #
###############
# set include directory
set(ORACLE_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)

file(GLOB oracle_SRC "src/*.cc")

add_executable(oracle ${oracle_SRC})
target_include_directories(oracle PUBLIC "${ORACLE_INCLUDE_DIR}")
target_compile_options(oracle PUBLIC -Wall -Wextra -pedantic -Wuninitialized)
target_link_libraries(oracle visutripoli4 t4random t4core)
compilation_info(oracle)

file(GLOB test_SRC "src/tests/*.cc")

add_executable(tests ${test_SRC} src/Statistics.cc src/T4Geometry.cc src/MCNPGeometry.cc)
target_include_directories(tests PUBLIC "${ORACLE_INCLUDE_DIR}")
target_compile_options(tests PUBLIC -Wall -Wextra -pedantic -Wuninitialized )
target_link_libraries(tests visutripoli4 t4random t4core gtest_main)
compilation_info(tests)
