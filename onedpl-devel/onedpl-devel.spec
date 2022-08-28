%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/onedpl-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
%global OAPI_MAJOR_VERSION g
%global OAPI_MINOR_VERSION i
%global OAPI_PATCH_VERSION t
%global OAPI_MAGIC_VERSION none
%global OAPI_INSTALL_DIR /opt/intel/oneapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
%global OAPI_GLOBAL_DIR /opt/intel/oneapi
#%global OAPI_LIBPATCH_VERSION %{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}
%global OAPI_LIBPATCH_VERSION latest
%global OAPI_GIT_DIR %{builddir}/OAPI-build/git
%global OAPI_GIT_TAG main
%global OAPI_BUILD_DIR %{builddir}/OAPI-build/build
%global OAPI_PATCH_DIR %{builddir}/OAPI-build/patch
%global OAPI_GIT_URL https://github.com/oneapi-src/oneDPL


%global toolchain clang

Name:     onedpl-devel
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI DPC++ Library 
License:  Apache 2.0
URL:      https://oneapi.io


Requires:      oneapi-core

Provides:      onedpl-devel
Provides:      onedpl-devel(x86-64)
Provides:      onedpl
Provides:      onedpl(x86-64)
Provides:      intel-oneapi-libdpstd-devel
Provides:      intel-oneapi-libdpstd-devel(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: git
BuildRequires: onetbb-devel
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
Intel's oneAPI DPC++ Library

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

mv %{_sourcedir}/oneDPL %{OAPI_GIT_DIR}/oneDPL-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

# Level 2 : Build

mkdir -p %{OAPI_BUILD_DIR}/sys-res/oneapi/lib64

ln -s %{OAPI_GLOBAL_DIR}/lib64/libtbb.so* %{OAPI_BUILD_DIR}/sys-res/oneapi/lib64/

ln -s %{OAPI_GLOBAL_DIR}/include %{OAPI_BUILD_DIR}/sys-res/oneapi/include

export CC=clang
export CXX=clang++

cmake -Wno-dev -GNinja -S %{OAPI_GIT_DIR}/oneDPL-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION} \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX=%{OAPI_BUILD_DIR}/sys-res/oneapi

ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{OAPI_BUILD_DIR}/onedpl-pkg" ninja -j$(nproc) install

mkdir -p  %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl

mv %{OAPI_BUILD_DIR}/onedpl-pkg/%{OAPI_BUILD_DIR}/sys-res/oneapi %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}

mv %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/doc/oneDPL/licensing %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/

rm -r  %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/linux

ln -s %{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include %{buildroot}/%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/linux/

%files 
%{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}

%post
mkdir -p %{OAPI_INSTALL_DIR}/include/oneapi || echo "include path exists."
ln -s %{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/oneapi/dpl %{OAPI_INSTALL_DIR}/include/oneapi/
mkdir -p %{OAPI_INSTALL_DIR}/licensing || echo "licensing path exists."
ln -s %{OAPI_INSTALL_DIR}/onedpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/licensing %{OAPI_INSTALL_DIR}/licensing/onedpl
/sbin/ldconfig

%postun
rm -r %{OAPI_INSTALL_DIR}/include/oneapi/dpl || echo "oneapi include path not present."
rm -r %{OAPI_INSTALL_DIR}/licensing/onedpl || echo "licensing not found."
/sbin/ldconfig
