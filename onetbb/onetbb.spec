%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/onetbb-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
%global OAPI_MAJOR_VERSION g
%global OAPI_MINOR_VERSION i
%global OAPI_PATCH_VERSION t
%global OAPI_MAGIC_VERSION none
%global OAPI_INSTALL_DIR /opt/oneapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
#%global OAPI_LIBPATCH_VERSION %{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}
%global OAPI_LIBPATCH_VERSION latest
%global OAPI_GIT_DIR %{builddir}/OAPI-build/git
%global OAPI_GIT_TAG master
%global OAPI_BUILD_DIR %{builddir}/OAPI-build/build
%global OAPI_PATCH_DIR %{builddir}/OAPI-build/patch
%global OAPI_GIT_URL https://github.com/oneapi-src/oneTBB


%global toolchain clang

Name:     onetbb
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI Threading Building Blocks
License:  Apache 2.0
URL:      https://oneapi.io


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

BuildRequires: git
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

# Level 1 : Download source

cd %{_sourcedir}

git clone -b %{OAPI_GIT_TAG} %{OAPI_GIT_URL}

cd %{builddir}

mv %{_sourcedir}/oneTBB %{OAPI_GIT_DIR}/oneTBB-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

# Level 2 : Build

export CC=clang
export CXX=clang++

cmake -Wno-dev -GNinja -S %{OAPI_GIT_DIR}/oneTBB-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION} \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}/onetbb

ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/lib

mv %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/lib64 %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/lib/intel64

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/env

cd %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/env

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/onetbb/env/vars.sh

chmod +x ./vars.sh

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/licensing

cd %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/licensing

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/onetbb/licensing/license.txt

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/onetbb/licensing/license_installer.txt

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/onetbb/licensing/third-party-programs.txt

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/sys_check

cd %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/sys_check

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/onetbb/sys_check/sys_check.sh

chmod +x ./sys_check.sh

#

mkdir -p %{buildroot}/etc/profile.d

ln -s %{OAPI_INSTALL_DIR}/onetbb/env/vars.sh  %{buildroot}/etc/profile.d/onetbb-vars.sh

mkdir -p %{buildroot}/usr/lib64/pkgconfig

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/pkgconfig/tbb.pc %{buildroot}/usr/lib64/pkgconfig/tbb.pc

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbb.so %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbb.so.12 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbb.so.12.7 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbbind_2_5.so %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbbind_2_5.so.3 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbbind_2_5.so.3.7 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc.so %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc.so.2 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc.so.2.7 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc_proxy.so %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc_proxy.so.2 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/libtbbmalloc_proxy.so.2.7 %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/pkgconfig

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/pkgconfig/tbb.pc %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/pkgconfig

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/cmake/TBB

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/cmake/TBB/TBBConfig.cmake %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/cmake/TBB

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/cmake/TBB/TBBConfigVersion.cmake %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/cmake/TBB

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/cmake/TBB/TBBTargets.cmake %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/cmake/TBB

ln -s %{OAPI_INSTALL_DIR}/onetbb/lib/intel64/cmake/TBB/TBBTargets-release.cmake %{buildroot}/%{OAPI_INSTALL_DIR}/lib64/cmake/TBB

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/env

ln -s %{OAPI_INSTALL_DIR}/onetbb/env %{buildroot}/%{OAPI_INSTALL_DIR}/env/onetbb


#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/licensing

ln -s %{OAPI_INSTALL_DIR}/onetbb/licensing %{buildroot}/%{OAPI_INSTALL_DIR}/licensing/onetbb

#

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/sys_check

ln -s %{OAPI_INSTALL_DIR}/onetbb/sys_check %{buildroot}/%{OAPI_INSTALL_DIR}/sys_check/onetbb

%files 
/etc/profile.d/onetbb-vars.sh
/usr/lib64/pkgconfig/tbb.pc
%{OAPI_INSTALL_DIR}/onetbb/lib/intel64/*
%{OAPI_INSTALL_DIR}/lib64/*
%{OAPI_INSTALL_DIR}/env/onetbb
%{OAPI_INSTALL_DIR}/licensing/onetbb
%{OAPI_INSTALL_DIR}/sys_check/onetbb

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
