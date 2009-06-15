#
# spec file for package SFEakonadi
#
# includes module(s): akonadi
#
#
%include Solaris.inc
%include base.inc

%define src_dir          akonadi
Name:                    SFEakonadi
Summary:                 PIM data storage server
Version:                 1.1.2
License:                 LGPLv2+
URL:                     http://pim.kde.org/akonadi/
Source:                  http://download.akonadi-project.org/akonadi-%{version}.tar.bz2
Patch1:                  akonadi-01-mysql_conf.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SUNWgnome-vfs
Requires:      SFEboost-gpp
Requires:      SUNWmysql5r
Requires:      SUNWmysql5u
BuildRequires: SFEautomoc
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SUNWgnome-vfs
BuildRequires: SFEboost-gpp-devel
BuildRequires: SUNWmysql5u


%description
Akonadi is a PIM layer, which provides an asynchronous API to access all kind
of PIM data (e.g. mails, contacts, events, todos etc.).

It consists of several processes (generally called the Akonadi server) and a
library (called client library) which encapsulates the communication
between the client and the server.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEautomoc
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SUNWgnome-vfs
Requires: SFEboost-gpp-devel
Requires: SUNWmysql5u


%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
cd ..

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
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
OPATH=${PATH}

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc} -I%{_includedir}/boost/gcc4"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc} -I%{_includedir}/boost/gcc4"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DLIB_DESTINATION=%{_libdir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

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
%{_bindir}/akonadi_control
%{_bindir}/akonadictl
%{_bindir}/akonadiserver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
