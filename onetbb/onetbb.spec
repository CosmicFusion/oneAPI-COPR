%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir oneapi-core-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
%global OAPI_MAJOR_VERSION 20
%global OAPI_MINOR_VERSION 21
%global OAPI_PATCH_VERSION 4.0
%global OAPI_MAGIC_VERSION 327
%global OAPI_INSTALL_DIR /opt/oneapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
%global OAPI_LIBPATCH_VERSION %{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}
%global OAPI_GIT_DIR %{builddir}/OAPI-build/git
%global OAPI_GIT_TAG release/2021.4
%global OAPI_BUILD_DIR %{builddir}/OAPI-build/build
%global OAPI_PATCH_DIR %{builddir}/OAPI-build/patch

%global toolchain clang

Name:     onetbb
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI Threading Building Blocks
License:  Apache 2.0
URL:      https://oneapi.io
Source0: https://github.com/oneapi-src/oneTBB/archive/refs/tags/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}.tar.gz


Requires:      oneapi-core

Provides:      onetbb
Provides:      onetbb(x86-64)
Provides:      intel-oneapi-tbb
Provides:      intel-oneapi-tbb(x86-64)
Provides:      intel-oneapi-runtime-tbb
Provides:      intel-oneapi-runtime-tbb(x86-64)
Provides:      intel-oneapi-tbb-common
Provides:      intel-oneapi-tbb-common(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

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

%description
Intel's oneAPI Threading Building Blocks

%build

# Make basic structure
mkdir -p %{builddir}

cd %{builddir}

mkdir -p %{OAPI_GIT_DIR}

mkdir -p %{OAPI_BUILD_DIR}

mkdir -p %{OAPI_PATCH_DIR}

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}

cd %{buildroot}/%{OAPI_INSTALL_DIR}

# Level 1 : Download source

cp %{SOURCE0}

tar -xf %{SOURCE0} -C %{OAPI_GIT_DIR}

# Level 2 : Build

export CC=clang
export CXX=clang++

#cmake -Wno-dev -GNinja -S .. \
#-DCMAKE_BUILD_TYPE=Release \
#-DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}


# Level 3 : Package



%files 
%{OAPI_INSTALL_DIR}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

