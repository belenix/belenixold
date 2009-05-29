#
# spec file for package SFEdecibel
#
# includes module(s): decibel
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          decibel
Name:                    SFEdecibel
Summary:                 Decibel is a realtime communications framework, integrating services like CTI, VoIP, text based chat and instant messaging. 
Version:                 0.5.0
License:                 LGPLv2
Source:                  http://decibel.kde.org/fileadmin/downloads/decibel/releases/decibel-%{version}.tar.gz
URL:                     http://decibel.kde.org/
Patch1:                  decibel-01-registeraccount.cpp.diff
Patch2:                  decibel-2-CMakeLists.1.diff
Patch3:                  decibel-3-CMakeLists.2.diff
Patch4:                  decibel-4-CMakeLists.3.diff
Patch5:                  decibel-5-CMakeLists.4.diff
Patch7:                  decibel-7-CMakeLists.6.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEtapioca-qt
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SFEtapioca-qt-devel


%description
Decibel is a realtime communications framework, integrating services
like CTI (Computer Telephone Integration), VoIP (Voice over IP), text
based chat and instant messaging.

Desktop users find in Decibel one central place to manage all their
realtime communication settings and can easily configure and change
responses to communication requests.

By providing a simple, DBus-based API to the services like communication
accountmanagement, connection to contacts, etc. Decibel reduces the
complexity and effort of accessing realtime communication technologies
in applications. This allows for integration of realtime communication
technologies into applications that are not focused on communication.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SFEdoxygen
Requires: SFEtapioca-qt-devel

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch7 -p0
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
%endif

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 -lQtDBus %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags -lQtDBus %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L/lib -R/lib"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBIN_INSTALL_DIR=%{_bindir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd %{src_dir}-%{version}
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/decibel
%{_bindir}/decibel_logger

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/Decibel
%{_datadir}/Decibel/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/Decibel
%{_libdir}/Decibel/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/decibel
%{_bindir}/%{_arch64}/decibel_logger
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/Decibel
%{_libdir}/%{_arch64}/Decibel/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/Decibel.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/Decibel.pc
%endif

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
