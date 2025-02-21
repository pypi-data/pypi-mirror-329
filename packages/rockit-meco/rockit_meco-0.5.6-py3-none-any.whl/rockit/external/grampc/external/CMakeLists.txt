project(grampc)

set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

cmake_minimum_required(VERSION 3.0)

add_library(grampc SHARED
src/euler1.c     src/grampc_alloc.c      src/grampc_init.c  src/grampc_run.c     src/grampc_setparam.c  src/heun2.c  src/ruku45.c   src/trapezodial.c
src/eulermod2.c  src/grampc_fixedsize.c  src/grampc_mess.c  src/grampc_setopt.c  src/grampc_util.c      src/rodas.c  src/simpson.c
include/euler1.h     include/f2cmod.h        include/grampc_fixedsize.h  include/grampc_init.h   include/grampc_mess.h  include/grampc_setopt.h    include/grampc_util.h  include/probfct.h           include/rodas.h   include/simpson.h
include/eulermod2.h  include/grampc_alloc.h  include/grampc.h            include/grampc_macro.h  include/grampc_run.h   include/grampc_setparam.h  include/heun2.h        include/rodas_decsol_f2c.h  include/ruku45.h  include/trapezodial.h
)
target_include_directories(grampc PRIVATE include)

install(TARGETS grampc RUNTIME DESTINATION libs LIBRARY DESTINATION libs)

            
