set(additional_include "path1;path2,path3 path4")
set(additional_link "")

string(REPLACE " " ";" additional_include "${additional_include}")
string(REPLACE "," ";" additional_link "${additional_link}")

# try download cross toolchain
if(NOT DEFINED ENV{CROSS_TOOLCHAINS})
    message("CROSS_TOOLCHAINS was not defined, try source download_toolchain.sh")
    execute_process(
        COMMAND bash -c "CHIP=${CHIP} DEV_MODE=${DEV_MODE} source $ENV{PPL_PROJECT_ROOT}/samples/scripts/download_toolchain.sh && env"
        RESULT_VARIABLE result
        OUTPUT_VARIABLE output
    )
    if(NOT result EQUAL "0")
        message(FATAL_ERROR "Not able to source download_toolchain.sh: ${output}")
    endif()
    string(REGEX MATCH "CROSS_TOOLCHAINS=([^\n]*)" _ ${output})
    set(ENV{CROSS_TOOLCHAINS} "${CMAKE_MATCH_1}")
endif()
# Set the C compiler
set(CMAKE_C_COMPILER $ENV{CROSS_TOOLCHAINS}/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.1/bin/riscv64-unknown-linux-gnu-gcc)

# Set the include directories for the shared library
set(TPUKERNEL_TOP ${PPL_TOP}/runtime/${CHIP}/TPU1686)
set(KERNEL_TOP ${PPL_TOP}/runtime/kernel)
set(CUS_TOP ${PPL_TOP}/runtime/customize)
if(DEFINED RUNTIME_PATH)
	set(RUNTIME_TOP ${RUNTIME_PATH})
  message(NOTICE "RUNTIME PATH: ${RUNTIME_PATH}")
else()
	set(RUNTIME_TOP ${PPL_TOP}/runtime/bm1690/tpuv7-runtime-emulator)
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR}/include)
include_directories(${TPUKERNEL_TOP}/kernel/include)
include_directories(${KERNEL_TOP})
include_directories(${CUS_TOP}/include)
include_directories(${RUNTIME_TOP}/include)
include_directories(${additional_include})

# generate ppl
set(SCRIPTS_CMAKE_DIR "${PPL_TOP}/runtime/scripts/")
list(APPEND CMAKE_MODULE_PATH "${SCRIPTS_CMAKE_DIR}")
include(AddPPL)  #AddPPL.cmake including pplgen
file(GLOB PPL_SOURCE ppl/*.pl)
set(OPT_LEVEL 2)
foreach(ppl_file ${PPL_SOURCE})
	set(input ${ppl_file})
	set(output ${CMAKE_CURRENT_BINARY_DIR})
	ppl_gen(${input} ${CHIP} ${output} ${OPT_LEVEL})
endforeach()

# Set the library directories for the shared library (link lib${CHIP}.a)
link_directories(${PPL_TOP}/runtime/${CHIP}/lib)
link_directories(${RUNTIME_TOP}/lib)

# Create the kernel library
aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/device DEVICE_SRCS)
set(LIBBMCHIP_PATH "${PPL_TOP}/runtime/${CHIP}/lib/lib${CHIP}.a")
set(SHARED_LIBRARY_OUTPUT_FILE libkernel)

add_library(${SHARED_LIBRARY_OUTPUT_FILE} SHARED ${DEVICE_SRCS} ${CUS_TOP}/src/ppl_helper.c)

# Link the libraries for the shared library
target_link_libraries(${SHARED_LIBRARY_OUTPUT_FILE} -Wl,--whole-archive lib${CHIP}.a -Wl,--no-whole-archive m)
install(TARGETS ${SHARED_LIBRARY_OUTPUT_FILE} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/lib)

if ("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
  MESSAGE (STATUS "Current is Debug mode")
  SET (FW_DEBUG_FLAGS "-DUSING_FW_DEBUG")
ENDIF ()
# Set the output file properties for the shared library
set_target_properties(${SHARED_LIBRARY_OUTPUT_FILE} PROPERTIES PREFIX "" SUFFIX ".so" COMPILE_FLAGS "-fPIC ${FW_DEBUG_FLAGS}" LINK_FLAGS "-shared")

# Create host exe
aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/host PPL_SRC_FILES)
aux_source_directory(src SRC_FILES)
add_executable(test_case ${PPL_SRC_FILES} ${SRC_FILES})
target_link_libraries(test_case PRIVATE tpuv7_rt cdm_daemon_emulator pthread ${additional_link})
install(TARGETS test_case DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
