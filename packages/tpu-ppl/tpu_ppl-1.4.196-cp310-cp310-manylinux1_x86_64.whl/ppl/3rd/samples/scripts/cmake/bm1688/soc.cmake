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
    message("CROSS_TOOLCHAINS has been set as $ENV{CROSS_TOOLCHAINS} by default.")
endif()

# Set the C compiler
set(CMAKE_C_COMPILER $ENV{CROSS_TOOLCHAINS}/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.1/bin/riscv64-unknown-linux-gnu-gcc)
set(CMAKE_ASM_COMPILER $ENV{CROSS_TOOLCHAINS}/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/bin/aarch64-none-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER $ENV{CROSS_TOOLCHAINS}/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/bin/aarch64-none-linux-gnu-g++)

# Set the include directories for the shared library
set(TPUKERNEL_TOP ${PPL_TOP}/runtime/${CHIP}/TPU1686)
set(KERNEL_TOP ${PPL_TOP}/runtime/kernel)
set(CUS_TOP ${PPL_TOP}/runtime/customize)

if(DEFINED RUNTIME_PATH)
	set(RUNTIME_TOP ${RUNTIME_PATH})
  message(NOTICE "RUNTIME PATH: ${RUNTIME_PATH}")
else()
	set(RUNTIME_TOP ${PPL_TOP}/runtime/${CHIP}/libsophon/bmlib)
endif()

if(NOT DEFINED ENV{SOC_SDK})
  message(FATAL_ERROR "Environment variable SOC_SDK has not been set. Please download libsophon_soc and set SOC_SDK.")
else()
  set(SOC_SDK_INCLUDE_PATH "$ENV{SOC_SDK}/include")
  set(SOC_SDK_LIB_PATH "$ENV{SOC_SDK}/lib")
  if(NOT EXISTS $ENV{SOC_SDK}/include)
    message(FATAL_ERROR "The include path '$ENV{SOC_SDK}/include' does not exist. Please check the path.")
  endif()
  if(NOT EXISTS $ENV{SOC_SDK}/lib)
    message(FATAL_ERROR "The lib path '$ENV{SOC_SDK}/lib' does not exist. Please check the path.")
  endif()
  include_directories($ENV{SOC_SDK}/include)
  link_directories($ENV{SOC_SDK}/lib)
endif()

include_directories(${CMAKE_CURRENT_BINARY_DIR}/include)
include_directories(${TPUKERNEL_TOP}/kernel/include)
include_directories(${KERNEL_TOP})
include_directories(${CUS_TOP}/include)
include_directories(${CMAKE_BINARY_DIR})
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

set(BM_LIBS bmlib dl pthread)

# Set the output file for the shared library
set(SHARED_LIBRARY_OUTPUT_FILE lib${CHIP}_kernel_module)

# Create the shared library
aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/device DEVICE_SRCS)

set(LIBBMCHIP_PATH "${PPL_TOP}/runtime/${CHIP}/lib/lib${CHIP}.a")

execute_process(
    COMMAND nm -g ${LIBBMCHIP_PATH}
    COMMAND grep "__ppl_get_dtype"
    RESULT_VARIABLE result_dtype
    OUTPUT_VARIABLE output_dtype
)

execute_process(
    COMMAND nm -g ${LIBBMCHIP_PATH}
    COMMAND grep "__dtype"
    RESULT_VARIABLE result_dtype_var
    OUTPUT_VARIABLE output_dtype_var
)

if("${result_dtype}" EQUAL "0" AND "${result_dtype_var}" EQUAL "0")
    message(STATUS "Symbols __ppl_get_dtype and __dtype found in ${LIBBMCHIP_PATH}")
    add_library(${SHARED_LIBRARY_OUTPUT_FILE} SHARED ${DEVICE_SRCS})
else()
    message(STATUS "One or both symbols __ppl_get_dtype and __dtype not found in ${LIBBMCHIP_PATH}")
    add_library(${SHARED_LIBRARY_OUTPUT_FILE} SHARED ${DEVICE_SRCS} ${CUS_TOP}/src/ppl_helper.c)
endif()

# Link the libraries for the shared library
target_link_libraries(${SHARED_LIBRARY_OUTPUT_FILE} -Wl,--whole-archive lib${CHIP}.a -Wl,--no-whole-archive m)

# Set the output file properties for the shared library
set_target_properties(${SHARED_LIBRARY_OUTPUT_FILE} PROPERTIES PREFIX "" SUFFIX ".so" COMPILE_FLAGS "-fPIC" LINK_FLAGS "-shared")

# Set the path to the input file
set(INPUT_FILE "${CMAKE_BINARY_DIR}/lib${CHIP}_kernel_module.so")

# Set the path to the output file
set(KERNEL_HEADER "${CMAKE_BINARY_DIR}/kernel_module_data.h")
add_custom_command(
    OUTPUT ${KERNEL_HEADER}
    DEPENDS ${SHARED_LIBRARY_OUTPUT_FILE}
    COMMAND echo "const unsigned int kernel_module_data[] = {" > ${KERNEL_HEADER}
    COMMAND hexdump -v -e '1/4 \"0x%08x,\\n\"' ${INPUT_FILE} >> ${KERNEL_HEADER}
    COMMAND echo "}\;" >> ${KERNEL_HEADER}
)

# Add a custom target that depends on the custom command
add_custom_target(gen_kernel_module_data_target DEPENDS ${KERNEL_HEADER})
# Add a custom target for the shared library
add_custom_target(dynamic_library DEPENDS ${SHARED_LIBRARY_OUTPUT_FILE})

aux_source_directory(${CMAKE_CURRENT_BINARY_DIR}/host PPL_SRC_FILES)
aux_source_directory(src SRC_FILES)
add_executable(test_case ${PPL_SRC_FILES} ${SRC_FILES})
add_dependencies(test_case dynamic_library gen_kernel_module_data_target)
target_link_libraries(test_case PRIVATE ${BM_LIBS} ${additional_link})
install(TARGETS test_case DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
