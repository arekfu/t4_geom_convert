# script that detects the OS version and sets the following cache variables:
#   OS_NAME
#   OS_RELEASE
#   OS_MAJOR_RELEASE
#   OS_ARCHITECTURE
#   OS_ID

if(NOT OS_ID)

  find_program(LSB_RELEASE lsb_release)
  find_program(SW_VERS sw_vers)
  find_program(UNAME uname)
  mark_as_advanced(LSB_RELEASE SW_VERS UNAME)


  if(LSB_RELEASE) # Linux systems
    # OS_NAME
    execute_process(COMMAND ${LSB_RELEASE} -s -i
      OUTPUT_VARIABLE OS_NAME
      OUTPUT_STRIP_TRAILING_WHITESPACE)
    string(TOLOWER "${OS_NAME}" OS_NAME)

    # Calibre 9 says "Debian" at this point, look in /etc/issue
    if(OS_NAME MATCHES "debian" AND EXISTS /etc/issue)
      file(READ /etc/issue ETC_ISSUE)
      string(REGEX MATCH "^([^ ]+) +([0-9]+(\\.[0-9]+)*)" ETC_ISSUE_MATCHES "${ETC_ISSUE}")
      set(ETC_ISSUE_NAME "${CMAKE_MATCH_1}")
      set(ETC_ISSUE_RELEASE "${CMAKE_MATCH_2}")
      if(ETC_ISSUE_NAME STREQUAL "Calibre")
        set(OS_NAME "calibre")
      endif()
    endif()

    # OS_RELEASE
    if(OS_NAME MATCHES "calibre")
      set(OS_RELEASE "${ETC_ISSUE_RELEASE}")
    else()
      execute_process(COMMAND ${LSB_RELEASE} -s -r
        OUTPUT_VARIABLE OS_RELEASE
        OUTPUT_STRIP_TRAILING_WHITESPACE)
    endif()

    if(UNAME)
      # OS_ARCHITECTURE
      execute_process(COMMAND ${UNAME} -m
        OUTPUT_VARIABLE OS_ARCHITECTURE
        OUTPUT_STRIP_TRAILING_WHITESPACE)
      string(REPLACE "_" "-" OS_ARCHITECTURE ${OS_ARCHITECTURE})
    elseif(NOT OS_ARCHITECTURE)
      set(OS_ARCHITECTURE "NOTFOUND")
    endif()

    # OS_MAJOR_RELEASE
    if(OS_RELEASE)
      string(REPLACE "." ";" RELEASE_LIST ${OS_RELEASE})
      list(GET RELEASE_LIST 0 OS_MAJOR_RELEASE)
    else()
      set(OS_MAJOR_RELEASE "NOTFOUND")
    endif()

  elseif(SW_VERS) # Mac OS
    # OS_NAME
    execute_process(COMMAND ${SW_VERS} -productName
      OUTPUT_VARIABLE OS_NAME
      OUTPUT_STRIP_TRAILING_WHITESPACE)
    string(TOLOWER "${OS_NAME}" OS_NAME)

    # OS_RELEASE
    if(UNAME)
      execute_process(COMMAND ${UNAME} -r
        OUTPUT_VARIABLE OS_RELEASE
        OUTPUT_STRIP_TRAILING_WHITESPACE)
    else()
      set(OS_RELEASE "NOTFOUND")
    endif()

    # OS_ARCHITECTURE
    set(OS_ARCHITECTURE "x86-64")

    # OS_MAJOR_RELEASE
    if(OS_RELEASE)
      string(REPLACE "." ";" RELEASE_LIST ${OS_RELEASE})
      list(GET RELEASE_LIST 0 RELEASE_LIST_0)
      list(GET RELEASE_LIST 1 RELEASE_LIST_1)
      set(OS_MAJOR_RELEASE "${RELEASE_LIST_0}${RELEASE_LIST_1}")
    else()
      set(OS_MAJOR_RELEASE "NOTFOUND")
    endif()

  else()
    if(NOT OS_NAME)
      set(OS_NAME "NOTFOUND")
    endif()
    if(NOT OS_RELEASE)
      set(OS_RELEASE "NOTFOUND")
    endif()
  endif()

  if(OS_ARCHITECTURE AND OS_MAJOR_RELEASE)
    # OS_ID
    if(OS_NAME STREQUAL "ubuntu")
      set(OS_ID "lin-${OS_ARCHITECTURE}-ubu${OS_MAJOR_RELEASE}")
    elseif(OS_NAME MATCHES "centos")
      set(OS_ID "lin-${OS_ARCHITECTURE}-cen${OS_MAJOR_RELEASE}")
    elseif(OS_NAME MATCHES "calibre")
      set(OS_ID "lin-${OS_ARCHITECTURE}-cal${OS_MAJOR_RELEASE}")
    elseif(OS_NAME MATCHES "mac os x")
      set(OS_ID "mac-${OS_ARCHITECTURE}-dw${OS_MAJOR_RELEASE}")
    else()
      message(FATAL_ERROR "Unrecognized OS: \n  * OS_NAME: ${OS_NAME}\n  * OS_RELEASE: ${OS_RELEASE}\n  * OS_MAJOR_RELEASE: ${OS_MAJOR_RELEASE}\n  * OS_ARCHITECTURE: ${OS_ARCHITECTURE}\n  * OS_ID: ${OS_ID}")
    endif()
  elseif(NOT OS_ID)
    set(OS_ID "NOTFOUND")
  endif()

  # store the detected properties in the cache
  set(OS_NAME "${OS_NAME}" CACHE STRING "Name of the OS")
  set(OS_RELEASE "${OS_RELEASE}" CACHE STRING "Full version of the OS")
  set(OS_MAJOR_RELEASE "${OS_MAJOR_RELEASE}" CACHE STRING "Major version of the OS")
  set(OS_ARCHITECTURE "${OS_ARCHITECTURE}" CACHE STRING "Architecture for this OS")
  set(OS_ID "${OS_ID}" CACHE STRING "ID string for the OS")
  mark_as_advanced(OS_NAME OS_RELEASE OS_MAJOR_RELEASE OS_ARCHITECTURE OS_ID)

  message(STATUS "Detected operating system:")
  message(STATUS "  ID:            ${OS_ID}")
  message(STATUS "  name:          ${OS_NAME}")
  message(STATUS "  release:       ${OS_RELEASE}")
  message(STATUS "  major release: ${OS_MAJOR_RELEASE}")
  message(STATUS "  architecture:  ${OS_ARCHITECTURE}")

endif()
