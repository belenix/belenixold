#
# spec file for package SFEpolkit-qt4
#
# includes module(s): polkit-qt4
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          polkit-qt
Name:                    SFEpolkit-qt4
Summary:                 Qt4 bindings for PolicyKit
Version:                 0.9.2
License:                 GPLv2+
URL:                     http://api.kde.org/kdesupport-api/kdesupport-apidocs/polkit-qt/html/
Source:                  ftp://gd.tuwien.ac.at/kde/stable/apps/KDE4.x/admin/polkit-qt-%{version}.tar.bz2

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEpolicykit
BuildRequires: SFEqt4-devel
BuildRequires: SFEpolicykit-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake

%description
Polkit-qt is a library that lets developers use the PolicyKit API through a nice
Qt-styled API. It is mainly a wrapper around QAction and QAbstractButton that
lets you integrate those two component easily with PolicyKit.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SFEautomoc
Requires: SUNWhea
Requires: SFEpolicykit-devel

%prep
%setup -q -c -n %name-%version

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
export JAVA_HOME=%{_prefix}/java
export QMAKESPEC=%{_datadir}/qt4/mkspecs/solaris-g++
export 
OPATH=${PATH}

mkdir -p kdebld
cd kdebld

export CFLAGS="-O3 -march=pentium3 -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export CXXFLAGS="-O3 -march=pentium3 -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export LDFLAGS="-L%{_libdir}/polkit -R%{_libdir}/polkit %_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path}"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_libdir}/polkit/pkgconfig:%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   ../%{src_dir}-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DDBUS_INTERFACES_INSTALL_DIR=%{_datadir}/dbus-1/interfaces     \
        -DDBUS_SERVICES_INSTALL_DIR=%{_datadir}/dbus-1/services         \
        -DBUILD_SHARED_LIBS=On                                          \
        -DKDE4_ENABLE_HTMLHANDBOOK=On                                   \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}
cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
cd ..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Sep 19 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
