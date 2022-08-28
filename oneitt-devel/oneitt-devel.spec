%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/oneitt-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
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
%global OAPI_GIT_URL https://github.com/intel/ittapi


%global toolchain clang

Name:     oneitt-devel
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's Instrumentation and Tracing Technology (ITT) and Just-In-Time (JIT) API
License:  GPLv2
URL:      https://oneapi.io


Requires:      oneapi-core

Provides:      oneitt-devel
Provides:      oneitt-devel(x86-64)
Provides:      oneitt
Provides:      oneitt(x86-64)

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
BuildRequires: python

%description
Intel's Instrumentation and Tracing Technology (ITT) and Just-In-Time (JIT) API

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

mv %{_sourcedir}/ittapi %{OAPI_GIT_DIR}/ittapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

# Level 2 : Build

export CC=clang
export CXX=clang++

cd %{OAPI_GIT_DIR}/ittapi-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

python buildall.py || 32 bit , unbuildable , going 64 bit only.

# Level 2 : Build

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64

mv build_linux/64/bin/libittnotify.a %{buildroot}/%{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/

mv include %{buildroot}/%{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/

%files 
%{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}

%post
mkdir -p %{OAPI_INSTALL_DIR}/lib64 || echo "library path exists."
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/libittnotify.a %{OAPI_INSTALL_DIR}/lib64/
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/libittnotify.a %{OAPI_INSTALL_DIR}/lib64/libittnotify.a
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/libittnotify.a %{OAPI_INSTALL_DIR}/lib64/ittnotify64.a
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64/libittnotify.a %{OAPI_INSTALL_DIR}/lib64/ittnotify64
mkdir -p %{OAPI_INSTALL_DIR}/include/oneapi/ || echo "include path exists."
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include %{OAPI_INSTALL_DIR}/include/oneapi/itt
ln -s %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/oneapi
/sbin/ldconfig

%postun
rm -r %{OAPI_INSTALL_DIR}/lib64/libittnotify.a || echo "itt libs not present"
rm -r %{OAPI_INSTALL_DIR}/lib64/libittnotify || echo "itt libs not present"
rm -r %{OAPI_INSTALL_DIR}/lib64/ittnotify64.a || echo "itt libs not present"
rm -r %{OAPI_INSTALL_DIR}/lib64/ittnotify64 || echo "itt libs not present"
rm -r %{OAPI_INSTALL_DIR}/include/oneapi/itt || echo "oneapi include path not present."
rm -r %{OAPI_INSTALL_DIR}/oneitt/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/include/oneapi || echo "oneapi include path not present."
/sbin/ldconfig
