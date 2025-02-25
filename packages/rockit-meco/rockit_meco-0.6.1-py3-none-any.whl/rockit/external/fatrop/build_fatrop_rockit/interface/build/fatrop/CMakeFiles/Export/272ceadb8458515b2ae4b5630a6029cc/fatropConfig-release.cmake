#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "fatrop::fatrop" for configuration "Release"
set_property(TARGET fatrop::fatrop APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fatrop::fatrop PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libfatrop.so"
  IMPORTED_SONAME_RELEASE "libfatrop.so"
  )

list(APPEND _cmake_import_check_targets fatrop::fatrop )
list(APPEND _cmake_import_check_files_for_fatrop::fatrop "${_IMPORT_PREFIX}/lib/libfatrop.so" )

# Import target "fatrop::blasfeo" for configuration "Release"
set_property(TARGET fatrop::blasfeo APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(fatrop::blasfeo PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "ASM;C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libblasfeo.a"
  )

list(APPEND _cmake_import_check_targets fatrop::blasfeo )
list(APPEND _cmake_import_check_files_for_fatrop::blasfeo "${_IMPORT_PREFIX}/lib/libblasfeo.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
