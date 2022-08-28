%undefine _auto_set_build_flags
%define _build_id_links none
%define _unpackaged_files_terminate_build 0

%global builddir %{_builddir}/onevpl-samples-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}-%{OAPI_LIBPATCH_VERSION}%{?dist}
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
%global OAPI_GIT_TAG3 main
%global OAPI_BUILD_DIR %{builddir}/OAPI-build/build
%global OAPI_PATCH_DIR %{builddir}/OAPI-build/patch
%global OAPI_GIT_URL https://github.com/oneapi-src/oneVPL
%global OAPI_GIT_URL2 https://github.com/oneapi-src/oneVPL-cpu
%global OAPI_GIT_URL3 https://github.com/oneapi-src/oneVPL-intel-gpu
%global toolchain clang

Name:     onevpl-samples
Version:  %{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}
Release:  %{OAPI_LIBPATCH_VERSION}%{?dist}
Summary:  Intel's oneAPI Video Processing Library Samples
License:  MIT
URL:      https://oneapi.io


Requires:      onevpl

Provides:      onevpl-samples
Provides:      onevpl-samples(x86-64)

Obsoletes:  	oneVPL-samples

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: git
BuildRequires: wget
BuildRequires: oneapi-core
BuildRequires: oneitt-devel
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

%description
Intel's oneAPI Video Processing Library Samples

%build

# Make basic structure
mkdir -p %{builddir}

cd %{builddir}

mkdir -p %{OAPI_GIT_DIR}

mkdir -p %{OAPI_BUILD_DIR}

mkdir -p %{OAPI_PATCH_DIR}

mkdir -p %{buildroot}/%{OAPI_INSTALL_DIR}



# Stage 1 : onevpl-cpu

# Level 1 : Download source

cd %{_sourcedir}

git clone -b %{OAPI_GIT_TAG} %{OAPI_GIT_URL}

git clone -b %{OAPI_GIT_TAG} %{OAPI_GIT_URL2}

cd %{builddir}

mv %{_sourcedir}/oneVPL %{OAPI_GIT_DIR}/oneVPL-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

mv %{_sourcedir}/oneVPL-cpu %{OAPI_GIT_DIR}/oneVPL-cpu-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}

# Level 2 : Build

cd %{OAPI_BUILD_DIR}
export CC=clang
export CXX=clang++
 
 
 cmake -Wno-dev -GNinja -S %{OAPI_GIT_DIR}/oneVPL-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION} \
-DCMAKE_BUILD_TYPE=Release -DENABLE_WAYLAND=ON \
-DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION} \
-DCMAKE_INSTALL_LIBDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64 \
-DONEAPI_INSTALL_ENVDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/env \
-DONEAPI_INSTALL_MODFILEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/modulefiles \
-DONEAPI_INSTALL_LICENSEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/licensing \
-DONEAPI_INSTALL_PYTHONDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/python/lib \
-DONEAPI_INSTALL_EXAMPLEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/examples \
-DCMAKE_INSTALL_DOCDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/doc


ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

# Level 4 : Clean

rm -r %{OAPI_BUILD_DIR}

mkdir -p %{OAPI_BUILD_DIR}


#

# Stage 2 : onevpl-gpu-intel

# Level 1 : Download source

cd %{_sourcedir}

git clone -b %{OAPI_GIT_TAG3} %{OAPI_GIT_URL3}


cd %{builddir}

mv %{_sourcedir}/oneVPL-intel-gpu %{OAPI_GIT_DIR}/oneVPL-intel-gpu-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION}


# Level 2 : Build

cd %{OAPI_BUILD_DIR}
export CC=clang
export CXX=clang++

cmake -Wno-dev -GNinja -S %{OAPI_GIT_DIR}/oneVPL-intel-gpu-%{OAPI_MAJOR_VERSION}.%{OAPI_MINOR_VERSION}.%{OAPI_PATCH_VERSION} \
-DCMAKE_BUILD_TYPE=Release  \
-DCMAKE_INSTALL_PREFIX=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION} \
-DCMAKE_INSTALL_LIBDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/lib/intel64 \
-DONEAPI_INSTALL_ENVDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/env \
-DONEAPI_INSTALL_MODFILEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/modulefiles \
-DONEAPI_INSTALL_LICENSEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/licensing \
-DONEAPI_INSTALL_PYTHONDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/python/lib \
-DONEAPI_INSTALL_EXAMPLEDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/examples \
-DCMAKE_INSTALL_DOCDIR=%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/share/doc \
-DENABLE_ITT=ON \
-DCMAKE_ITT_HOME=/opt/intel/oneapi/oneitt/git

ninja -j$(nproc)

# Level 3 : Package

DESTDIR="%{buildroot}" ninja -j$(nproc) install

%files 
%{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/*

%post
mkdir -p %{OAPI_INSTALL_DIR}/bin || echo "binary path exists."
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/decvpp_tool %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/sample_decode %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/sample_encode %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/sample_multi_transcode %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/sample_vpp %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/system_analyzer %{OAPI_INSTALL_DIR}/bin/
ln -s %{OAPI_INSTALL_DIR}/onevpl/%{OAPI_MAJOR_VERSION}%{OAPI_MINOR_VERSION}%{OAPI_PATCH_VERSION}/bin/vpl-inspect %{OAPI_INSTALL_DIR}/bin/
/sbin/ldconfig

%postun
rm -r %{OAPI_INSTALL_DIR}/bin/decvpp_tool || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/sample_decode || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/sample_encode || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/sample_multi_transcode || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/sample_vpp || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/system_analyzer || echo "binary not present"
rm -r %{OAPI_INSTALL_DIR}/bin/vpl-inspect || echo "binary not present"
/sbin/ldconfig
