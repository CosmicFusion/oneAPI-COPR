%undefine _auto_set_build_flags
%define _build_id_links none

%global builddir %{_builddir}/oneapi-core-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
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

Name:     oneapi-core
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI common variables and licensing	
License:  MIT
URL:      https://oneapi.io

Requires:      libc.so.6()(64bit)
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)
Requires:      libgcc_s.so.1()(64bit)
Requires:      libstdc++.so.6()(64bit)

Provides:      oneapi-core
Provides:      oneapi-core(x86-64)
Provides:      intel-oneapi-common-vars
Provides:      intel-oneapi-common-vars(x86-64)
Provides:      intel-oneapi-common-licensing
Provides:      intel-oneapi-common-licensing(x86-64)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: wget
#BuildRequires: cmake
#BuildRequires: make
#BuildRequires: gcc
#BuildRequires: gcc-c++
#BuildRequires: intel-gmmlib-devel
#BuildRequires: libva-devel
#BuildRequires: libdrm-devel
#BuildRequires: intel-igc-devel
#BuildRequires: ninja-build
#BuildRequires: libglvnd-devel
#BuildRequires: ocl-icd-devel
#BuildRequires: opencl-headers

%description
Intel's oneAPI common variables and licensing

%build

# Make basic structure
mkdir -p %{builddir}

cd %{builddir}

mkdir -p %{OAPI_GIT_DIR}

mkdir -p %{OAPI_BUILD_DIR}

mkdir -p %{OAPI_PATCH_DIR}

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}

# Level 1 : Create files

### Files from intel-oneapi-common-vars

# File N1 #

touch %{buildroot}/%{OAPI_INSTALL_DIR}/support.txt
tee > %{buildroot}/%{OAPI_INSTALL_DIR}/support.txt << EOF
For support options please see: https://software.intel.com/en-us/oneapi/support

For user forum support please see: https://software.intel.com/en-us/forum
EOF


# File N2 #

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/oneapi-core/setvars.sh -o %{buildroot}/%{OAPI_INSTALL_DIR}/setvars.sh
chmod +x %{buildroot}/%{OAPI_INSTALL_DIR}/setvars.sh

# File N3 #

wget https://raw.githubusercontent.com/CosmicFusion/oneAPI-COPR/main/oneapi-core/modulefiles-setup.sh -o %{buildroot}/%{OAPI_INSTALL_DIR}/modulefiles-setup.sh
chmod +x %{buildroot}/%{OAPI_INSTALL_DIR}/modulefiles-setup.sh

### Files from intel-oneapi-common-licensing
mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/licensing

# Level 2 : Package
mkdir -p %{buildroot}/etc/profile.d/

touch %{buildroot}/etc/profile.d/oneapi-core.sh

chmod +x %{buildroot}/etc/profile.d/oneapi-core.sh

echo 'export PATH=$PATH:/opt/oneapi:/opt/oneapi/bin' > %{buildroot}/etc/profile.d/oneapi-core.sh

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/lib64

ln -s %{OAPI_INSTALL_DIR} %{buildroot}/opt/oneapi

ln -s %{OAPI_INSTALL_DIR}/lib64 %{buildroot}/%{OAPI_INSTALL_DIR}/lib

mkdir -p %{buildroot}/etc/ld.so.conf.d

touch %{buildroot}/etc/ld.so.conf.d/10-oneapi-core.conf

echo /opt/oneapi/lib > %{buildroot}/etc/ld.so.conf.d/10-oneapi-core.conf

echo /opt/oneapi/lib64 >> %{buildroot}/etc/ld.so.conf.d/10-oneapi-core.conf

%files 
/etc/ld.so.conf.d/10-oneapi-core.conf
/etc/profile.d/oneapi-core.sh
%{OAPI_INSTALL_DIR}
/opt/oneapi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

