# custom_includes.cmake

# 定义设备相关的包含目录
set(DEVICE_INCLUDE_DIRS
    ${TPUKERNEL_TOP}/kernel/include
    ${CUS_TOP}/include
)

# 定义主机相关的包含目录
set(HOST_INCLUDE_DIRS
    ${KERNEL_TOP}
    ${RUNTIME_TOP}/include
)

# 定义设备和主机的链接目录
set(DEVICE_LINK_DIRS
    ${PPL_TOP}/runtime/${CHIP}/lib
)

set(HOST_LINK_DIRS
    ${RUNTIME_TOP}/lib
)

# 提供给用户使用的变量
set(DEVICE_INCLUDE "${DEVICE_INCLUDE_DIRS}" CACHE STRING "Device include directories")
set(HOST_INCLUDE "${HOST_INCLUDE_DIRS}" CACHE STRING "Host include directories")
set(DEVICE_LINK_DIR "${DEVICE_LINK_DIRS}" CACHE STRING "Device link directories")
set(HOST_LINK_DIR "${HOST_LINK_DIRS}" CACHE STRING "Host link directories")

# 输出信息
message(STATUS "Device Include Directories: ${DEVICE_INCLUDE}")
message(STATUS "Host Include Directories: ${HOST_INCLUDE}")
message(STATUS "Device Link Directories: ${DEVICE_LINK_DIR}")
message(STATUS "Host Link Directories: ${HOST_LINK_DIR}")

# 包含目录
include_directories(${DEVICE_INCLUDE})
include_directories(${HOST_INCLUDE})

# 链接目录
link_directories(${DEVICE_LINK_DIR})
link_directories(${HOST_LINK_DIR})
