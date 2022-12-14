%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/oneapi-compiler-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
%global OAPI_MAJOR_VERSION g
%global OAPI_MINOR_VERSION i
%global OAPI_PATCH_VERSION t
%global OAPI_MAGIC_VERSION none
%global OAPI_INSTALL_DIR /opt/intel/oneapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
%global OAPI_GLOBAL_DIR /opt/intel/oneapi
#%global OAPI_LIBPATCH_VERSION %{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}
%global OAPI_LIBPATCH_VERSION latest
%global OAPI_GIT_DIR %{builddir}/OAPI-build/git
%global OAPI_GIT_TAG master
%global OAPI_BUILD_DIR %{builddir}/OAPI-build/build
%global OAPI_PATCH_DIR %{builddir}/OAPI-build/patch
%global OAPI_GIT_URL https://github.com/intel/cm-compiler
%global OAPI_PATCH_1 include-stdlib.patch

BuildRequires: numactl-devel
BuildRequires: numactl
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: gcc-plugin-devel
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	ninja-build
BuildRequires:	zlib-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	python3-psutil
BuildRequires:	python3-sphinx
BuildRequires:	python3-recommonmark
BuildRequires:	multilib-rpm-config
BuildRequires:	binutils-devel
BuildRequires:	valgrind-devel
BuildRequires:	libedit-devel
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	gnupg2
BuildRequires: git
BuildRequires: oneitt-devel
BuildRequires: wget
BuildRequires: oneapi-core
BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: clang
BuildRequires: libva-devel
BuildRequires: libdrm-devel
BuildRequires: ninja-build
BuildRequires: libglvnd-devel
BuildRequires: ocl-icd-devel
BuildRequires: opencl-headers
BuildRequires: hwloc-devel
BuildRequires:  pkgconfig(libdrm) >= 2.4.91
BuildRequires:  pkgconfig(libva) >= 1.2
BuildRequires:  pkgconfig(libva-drm) >= 1.2
BuildRequires:  pkgconfig(libva-x11) >= 1.10.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.15
BuildRequires:  pkgconfig(x11)
BuildRequires:  python3dist(pybind11)
BuildRequires:  python3-devel
BuildRequires:  python3-devel
BuildRequires:  oneapi-vc-intrinsics
BuildRequires: spirv-llvm8.0-translator-devel
BuildRequires: llvm8.0-devel
BuildRequires: llvm8.0-static

Provides:      oneapi-compiler
Provides:      oneapi-compiler(x86-64)
Requires:      oneapi-core

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Name:     oneapi-compiler
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
URL:      https://oneapi.io
License:       Apache 2.0 + LLVM
Summary:       Intel's oneAPI cm compiler

%description
Intel's oneAPI cm compiler

%build

# Make basic structure
mkdir -p %{builddir}

cd %{builddir}

mkdir -p %{OAPI_GIT_DIR}

mkdir -p %{OAPI_BUILD_DIR}

mkdir -p %{OAPI_PATCH_DIR}

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}

# Level 1 : Download source

cd %{_sourcedir}

git clone -b %{OAPI_GIT_TAG} %{OAPI_GIT_URL}


cd %{builddir}

mv %{_sourcedir}/cm-compiler %{OAPI_GIT_DIR}/cm-compiler-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}


# Level 2 : Patch

#cd %{OAPI_PATCH_DIR}

#wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/oneapi-compiler/%{OAPI_PATCH_1}

#cd %{OAPI_GIT_DIR}/cm-compiler-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/llvm

#patch -Np1 -i "%{OAPI_PATCH_DIR}/%{OAPI_PATCH_1}"


# Level 3 : Build

cd %{OAPI_BUILD_DIR}
export CC=clang
export CXX=clang++

    cmake -GNinja -S %{OAPI_GIT_DIR}/cm-compiler-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/llvm \
    -DCMAKE_BUILD_TYPE=Release  \
    -DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}/oneapi-compiler/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION} \
    -DCMAKE_INSTALL_LIBDIR=%{OAPI_INSTALL_DIR}/oneapi-compiler/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64 \
    -DCMAKE_INSTALL_DOCDIR=%{OAPI_INSTALL_DIR}/oneapi-compiler/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/doc \
    -DLLVMGenXIntrinsics_DIR="%{OAPI_GLOBAL_DIR}/include/oneapi/vci/llvm/GenXIntrinsics/" \
    -DLLVM_ENABLE_BINDINGS=OFF \
    -DOCAMLFIND=NO \
    -DLLVM_TARGETS_TO_BUILD=GenX\;X86 \
    -DLLVM_ENABLE_OCAMLDOC=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    -DLLVM_BUILD_TESTS=OFF \
    -DLLVM_CMAKE_PATH=%{_libdir}/llvm8.0
    
    ninja -j$(nproc)



# Level 4 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-oneapi-cmc.conf

echo %{OAPI_INSTALL_DIR}/oneapi-compiler/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64 > %{buildroot}/etc/ld.so.conf.d/10-oneapi-cmc.conf

%files
/etc/ld.so.conf.d/*
%{OAPI_INSTALL_DIR}/oneapi-compiler/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
