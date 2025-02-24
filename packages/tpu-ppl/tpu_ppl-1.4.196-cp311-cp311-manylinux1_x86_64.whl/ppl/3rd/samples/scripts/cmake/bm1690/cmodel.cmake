if(DEBUG)
  set(CMAKE_BUILD_TYPE "Debug")
  add_definitions(-DDEBUG)
else()
  set(CMAKE_BUILD_TYPE "Release")
  if(NOT USING_CUDA)
    add_definitions(-O3)
  endif()
endif()


if(DEFINED RUNTIME_PATH)
  set(RUNTIME_TOP ${RUNTIME_PATH})
  message(NOTICE "RUNTIME PATH: ${RUNTIME_PATH}")
else()
  set(RUNTIME_TOP ${PPL_TOP}/runtime/bm1690/tpuv7-runtime-emulator)
  set(BMLIB_CMODEL_PATH ${RUNTIME_TOP}/lib/libtpuv7_emulator.so)
endif()

set(TPUKERNEL_TOP ${PPL_TOP}/runtime/${CHIP}/TPU1686)
set(KERNEL_TOP ${PPL_TOP}/runtime/kernel)
set(CUS_TOP ${PPL_TOP}/runtime/customize)

# 包含自定义的包含目录和链接目录
#include(../custom_includes.cmake)
include(${PPL_TOP}/samples/scripts/cmake/custom_includes.cmake)

include_directories(${CMAKE_CURRENT_BINARY_DIR}/include)
#include_directories(${TPUKERNEL_TOP}/kernel/include)
#include_directories(${KERNEL_TOP})
#include_directories(${RUNTIME_TOP}/include)
#include_directories(${CUS_TOP}/include)
#link_directories(${PPL_TOP}/runtime/${CHIP}/lib)
#link_directories(${RUNTIME_TOP}/lib)

# Add chip arch defination
# add_definitions(-D__${CHIP}__)

set(SCRIPTS_CMAKE_DIR "${PPL_TOP}/runtime/scripts/")
list(APPEND CMAKE_MODULE_PATH "${SCRIPTS_CMAKE_DIR}")
include(AddPPL)  #AddPPL.cmake including pplgen

# add_ppl_include(./include)
# add_ppl_include(../include)
# add_ppl_def("-DTEST")
# set_ppl_no_gen_dir()
file(GLOB PPL_SOURCE ppl/*.pl)
set(OPT_LEVEL 2)
foreach(ppl_file ${PPL_SOURCE})
	set(input ${ppl_file})
	set(output ${CMAKE_CURRENT_BINARY_DIR})
	ppl_gen(${input} ${CHIP} ${output} ${OPT_LEVEL})
endforeach()

aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/host PPL_SRC_FILES)
aux_source_directory(src SRC_FILES)

# 统一的设备和内核名称
#set(KERNEL_NAME "kernel_shared")

# 创建可执行文件
add_executable(test_case ${PPL_SRC_FILES} ${SRC_FILES})

target_link_libraries(test_case PRIVATE tpuv7_rt cdm_daemon_emulator pthread)
install(TARGETS test_case DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})

aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/device KERNEL_SRC_FILES)

# 创建共享库
add_library(kernel SHARED ${KERNEL_SRC_FILES} ${CUS_TOP}/src/ppl_helper.c)
#add_library(${KERNEL_NAME} SHARED ${DEVICE_SRC_FILES} ${CUS_TOP}/src/ppl_helper.c)
target_include_directories(kernel PRIVATE
#target_include_directories(${KERNEL_NAME} PRIVATE
  include
  ${PPL_TOP}/include
  ${CUS_TOP}/include
  ${TPUKERNEL_TOP}/common/include
  ${TPUKERNEL_TOP}/kernel/include
)

target_link_libraries(kernel PRIVATE ${BMLIB_CMODEL_PATH} m)
install(TARGETS kernel DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/lib)
#target_link_libraries(${KERNEL_NAME} PRIVATE ${BMLIB_CMODEL_PATH} m)
#install(TARGETS ${KERNEL_NAME} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/lib)
