#
# spec file for package SFElibmsn
#
# includes module(s): libmsn
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFElibmsn
Summary:                 Library for connecting to the MSN Messenger service
Version:                 4.0-beta4
URL:                     http://sourceforge.net/projects/libmsn/
Source:                  %{sf_download}/libmsn/libmsn-%{version}.tar.bz2
License:                 GPLv2

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWopenssl-libraries
BuildRequires:          SUNWopenssl-include
BuildRequires:          SFEcmake
BuildRequires:          SUNWgnome-common-devel

%description
Libmsn is a reusable, open-source, fully documented library for connecting to
the MSN Messenger service.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWopenssl-include
Requires:          SFEcmake
Requires:          SUNWgnome-common-devel


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp libmsn-%{version} libmsn-%{version}-64
%endif

%build
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
OPATH="${PATH}"

%ifarch amd64 sparcv9
cd libmsn-%{version}-64
mkdir build
cd build

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -lsocket -lnsl"
export PATH="%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib64}:%{gnu_lib64}:%{_prefix}/lib/%{_arch64}:/lib/%{_arch64}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_SUFFIX=/%{_arch64}                                        \
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make
cd ../..
%endif

cd libmsn-%{version}
mkdir build
cd build

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib -lsocket -lnsl"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make
cd ../..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libmsn-%{version}-64/build
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/msntest ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
cd ../..
%endif

cd libmsn-%{version}/build
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
cd ../..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Tue Jun 30 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
