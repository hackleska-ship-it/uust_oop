cmake_minimum_required(VERSION 3.10)
project(oop_lab2 LANGUAGES CXX)

add_executable(lab2 main.cpp objects.cpp objects.h)
target_compile_features(lab2 PRIVATE cxx_std_11)
set_target_properties(lab2 PROPERTIES CXX_EXTENSIONS OFF)

if(MSVC)
    target_compile_options(lab2 PRIVATE /W4 /WX /utf-8)
else()
    target_compile_options(lab2 PRIVATE -Wall -Wextra -pedantic -Werror)
endif()
