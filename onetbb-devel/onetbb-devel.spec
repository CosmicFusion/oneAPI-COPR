%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/onetbb-devel-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
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
%global OAPI_GIT_URL https://github.com/oneapi-src/oneTBB


%global toolchain clang

Name:     onetbb-devel
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI Threading Building Blocks Development Package
License:  Apache 2.0
URL:      https://oneapi.io


Requires:      onetbb

Provides:      onetbb-devel
Provides:      onetbb-devel(x86-64)
Provides:      intel-oneapi-tbb-devel
Provides:      intel-oneapi-tbb-devel(x86-64)
Provides:      intel-oneapi-tbb-common-devel
Provides:      intel-oneapi-tbb-common-devel(x86-64)

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
Intel's oneAPI Threading Building Blocks Development Package

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
-DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}

ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib

mv %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib64 %{buildroot}/%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64

mkdir -p %{buildroot}/usr/lib64/pkgconfig

ln -s %{OAPI_INSTALL_DIR}/lib64/pkgconfig/tbb.pc %{buildroot}/usr/lib64/pkgconfig/tbb.pc

%files 
/usr/lib64/pkgconfig/tbb.pc
%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/pkgconfig/tbb.pc
%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/*
%{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/cmake/TBB

%post
mkdir -p %{OAPI_INSTALL_DIR}/include/oneapi || echo "include path exists."
ln -s %{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/oneapi/tbb* %{OAPI_INSTALL_DIR}/include/oneapi/
ln -s %{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/tbb %{OAPI_INSTALL_DIR}/include/
mkdir -p %{OAPI_INSTALL_DIR}/lib64/pkgconfig || echo "pkgconfig exists."
ln -s %{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/pkgconfig/tbb.pc %{OAPI_INSTALL_DIR}/lib64/pkgconfig/
mkdir -p %{OAPI_INSTALL_DIR}/lib64/cmake/TBB || echo "cmake path exists."
ln -s %{OAPI_INSTALL_DIR}/onetbb/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/cmake/TBB/* %{OAPI_INSTALL_DIR}/lib64/cmake/TBB/
/sbin/ldconfig

%postun
rm -r %{OAPI_INSTALL_DIR}/include/oneapi/tbb* || echo "oneapi include path not present."
rm -r %{OAPI_INSTALL_DIR}/include/tbb || echo "tbb include path not present."
rm -r %{OAPI_INSTALL_DIR}/lib64/pkgconfig/tbb.pc || echo "TBB pkgconfig not found."
rm -r %{OAPI_INSTALL_DIR}/lib64/cmake/TBB || echo "cmake not found."
/sbin/ldconfig

