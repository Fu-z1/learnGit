# Compute the installation prefix relative to this file.
# strip file name
get_filename_component(_IMPORT_PREFIX ${CMAKE_CURRENT_LIST_FILE} PATH)

# strip ext.wxwidgets
get_filename_component(_IMPORT_PREFIX ${_IMPORT_PREFIX} PATH)

# strip cmake
get_filename_component(_IMPORT_PREFIX ${_IMPORT_PREFIX} PATH)

# strip lib
get_filename_component(_IMPORT_PREFIX ${_IMPORT_PREFIX} PATH)

# Strip also usr
get_filename_component(_IMPORT_BASE_PREFIX ${_IMPORT_PREFIX} PATH)

add_library(ext.wxwidgets INTERFACE IMPORTED GLOBAL)

ADD_LIBRARY(ext.wxwidgets.pd INTERFACE)
ADD_LIBRARY(ext.wxwidgets.pi INTERFACE)
target_link_libraries(ext.wxwidgets.pd INTERFACE ext.wxwidgets)
target_link_libraries(ext.wxwidgets.pi INTERFACE ext.wxwidgets)


SET(wxWidgets_CONFIG_OPTIONS --prefix=${_IMPORT_PREFIX} --libdir=${_IMPORT_BASE_PREFIX}/${CMAKE_INSTALL_LIBDIR})
find_package(wxWidgets)
if(NOT wxWidgets_FOUND)
   message(ERROR " wxWidgets not found. Something is weird.\n")
else()
   message(STATUS " wxWidgets ${wxWidgets_VERSION_STRING} found.\n")
endif()

# c++ is used for linking, so we need to add -Wl for linker flags too

set_target_properties(ext.wxwidgets PROPERTIES
   INTERFACE_COMPILE_DEFINITIONS "${wxWidgets_DEFINITIONS}"
   INTERFACE_INCLUDE_DIRECTORIES "${wxWidgets_INCLUDE_DIRS}"
   INTERFACE_LINK_LIBRARIES "${wxWidgets_LIBRARIES} -Wl,-rpath=${wxWidgets_LIBRARY_DIRS}"
)

