# CMake file for the Visualizer library
cmake_minimum_required(VERSION 3.2)
project(OracleMCNPT4 C CXX)

message(STATUS "********** OracleMCNPT4 ********** ")

# Path for cmake files shipped with the project
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

include(LibUtils)
include(FindMEDFile)
include(DetectOS)

set(CMAKE_CXX_STANDARD 11)
find_package(T4 REQUIRED)

# LAPACK/BLAS
import_LAPACK_library(LAPACK_FOUND REQUIRED)
# MEDFile
set(HDF5_VERSION_REQUIRED 1.8.14)
set(MEDFile_VERSION_REQUIRED 3.2.0)
import_MEDFile23_library(MEDFile23_FOUND REQUIRED)
# Boost
import_Boost_library(Boost_FOUND REQUIRED)


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
target_link_libraries(oracle visutripoli4 t4core t4)
compilation_info(oracle)

file(GLOB test_SRC "src/tests/*.cc")

add_executable(tests ${test_SRC} src/Statistics.cc src/T4Geometry.cc src/MCNPGeometry.cc)
target_include_directories(tests PUBLIC "${ORACLE_INCLUDE_DIR}")
target_compile_options(tests PUBLIC -Wall -Wextra -pedantic -Wuninitialized )
target_link_libraries(tests visutripoli4 t4core t4 gtest_main)
compilation_info(tests)
