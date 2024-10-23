cmake_minimum_required(VERSION 3.29)

project(project1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)



# add_definitions( -DBOOST_ALL_NO_LIB )
# set(Boost_NO_SYSTEM_PATHS true)
set(Boost_USE_STATIC_LIBS ON)
# set(Boost_USE_MULTITHREADED ON)
# set(Boost_USE_STATIC_RUNTIME ON)

find_package(Boost 1.81 COMPONENTS program_options REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})



set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++")

set(EXECUTABLES_LIST
  generator
  verifier
  solution
)

foreach(EXECUTABLE_NAME IN LISTS EXECUTABLES_LIST)
  add_executable(${EXECUTABLE_NAME} "${EXECUTABLE_NAME}.cpp")
  target_include_directories(${EXECUTABLE_NAME} PRIVATE "${CMAKE_SOURCE_DIR}/include")

  target_link_libraries(${EXECUTABLE_NAME} PRIVATE ${Boost_LIBRARIES})
endforeach()
