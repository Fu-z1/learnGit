#!/bin/bash

# check platform
if [[ ! -e /lib64/ld-linux-x86-64.so.2 ]] ; then
   echo "This toolchain can only run on GNU-Linux x86_64!" >&2
   exit 1
fi

D="$(cd "${0%/*}" && pwd)"

cat >"$D/environment-setup-%AUTOCONF_HOST%" <<EOF
export SDKTARGETSYSROOT=$D/%AUTOCONF_HOST%
export PATH=$D/toolchain/bin:\$PATH
export PKG_CONFIG_SYSROOT_DIR=\$SDKTARGETSYSROOT
export PKG_CONFIG_PATH="\$SDKTARGETSYSROOT/usr/lib/pkgconfig:\$SDKTARGETSYSROOT/usr/share/pkgconfig"
export CC="%CC% --sysroot=\$SDKTARGETSYSROOT"
export CXX="%CXX% --sysroot=\$SDKTARGETSYSROOT"
export CPP="%CPP% --sysroot=\$SDKTARGETSYSROOT"
export AS="%AS%"
export LD="%LD% --sysroot=\$SDKTARGETSYSROOT"
export GDB=%GDB%
export STRIP=%STRIP%
export RANLIB=%RANLIB%
export OBJCOPY=%OBJCPY%
export OBJDUMP=%OBJDMP%
export AR=%AR%
export NM=%NM%
export CONFIGURE_FLAGS="--build=%AUTOCONF_BUILD% --host=%AUTOCONF_HOST% --target=%AUTOCONF_TARGET%"
export CFLAGS="%CFLAGS%"
export CXXFLAGS="%CXXFLAGS%"
export LDFLAGS="%LDFLAGS%"
export ARCH=%ARCH%
export CROSS_COMPILE=%CROSS_COMPILE%
EOF

# create toolchain file
cat > aarch64-linux-gnu.toolchain <<EOF
# tell cmake the name of our target system
set (CMAKE_SYSTEM_NAME "Linux")

# set compiler
SET(CMAKE_C_COMPILER   "aarch64-linux-gnu-gcc")
SET(CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++")

# set root path
SET(CMAKE_SYSROOT "$D/%AUTOCONF_HOST%")

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER CACHE INTERNAL "")
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY CACHE INTERNAL "")
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY CACHE INTERNAL "")
EOF

echo "Source environment-setup-%AUTOCONF_HOST% in your shell to setup the build environment..."
