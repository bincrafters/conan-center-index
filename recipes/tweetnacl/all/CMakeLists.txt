cmake_minimum_required(VERSION 3.4)
project(tweetnacl LANGUAGES C)

include(conanbuildinfo.cmake)
conan_basic_setup()

if (WIN32 AND MSVC AND BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

add_library(${PROJECT_NAME} tweetnacl.c tweetnacl.h)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})

include(GNUInstallDirs)

install(TARGETS ${PROJECT_NAME}
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin)
install(FILES tweetnacl.h DESTINATION include)
