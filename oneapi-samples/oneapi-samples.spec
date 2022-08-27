%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/oneapi-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
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
%global OAPI_GIT_URL https://github.com/oneapi-src/oneAPI-samples


%global toolchain clang

Name:     oneapi-samples
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  code samples for Intel oneAPI toolkits.
License:  Intel + Apache 2.0 + MIT + unlicense
URL:      https://oneapi.io


Requires:      oneapi-core

Provides:      oneapi-samples
Provides:      oneapi-samples(x86-64)

BuildRequires: git
BuildRequires: oneapi-core

%description
code samples for Intel oneAPI toolkits.

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

mv %{_sourcedir}/oneAPI-samples %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

# Level 2 : Package

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}/licensing/oneapi-samples

mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/AI-and-Analytics %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/common %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/DirectProgramming %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/Libraries %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/Publications %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/RenderingToolkit %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/Tools %{buildroot}/%{OAPI_INSTALL_DIR}/share/oneapi-samples/samples/

mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/License.txt %{buildroot}/%{OAPI_INSTALL_DIR}/licensing/oneapi-samples
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/third-party-programs.txt %{buildroot}/%{OAPI_INSTALL_DIR}/licensing/oneapi-samples
mv %{OAPI_GIT_DIR}/oneAPI-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}/CODEOWNERS  %{buildroot}/%{OAPI_INSTALL_DIR}/licensing/oneapi-samples

%files 
%{OAPI_INSTALL_DIR}/share/oneapi-samples/
%{OAPI_INSTALL_DIR}/licensing/oneapi-samples/*

