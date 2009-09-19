#
# spec file for package SFEkdelibs4-experimental
#
# includes module(s): kdelibs-experimental
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc

Name:                    SFEkdelibs4-experimental
Summary:                 KDE libraries with experimental or unstable api/abi
Version:                 4.3.1
License:                 LGPLv2+
URL:                     http://www.kde.org/
Source:                  ftp://ftp.kde.org/pub/kde/unstable/4.3.65/src/kdelibs-experimental-4.3.65svn1013471.tar.bz2
%define src_dir          kdelibs-experimental-4.3.65svn1013471

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SUNWdbus
BuildRequires: SFEkdelibs4-devel
BuildRequires: SUNWdbus-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEkdelibs4-devel
Requires: SUNWdbus-devel

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

export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -floop-interchange -floop-block -ftree-loop-distribution -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -floop-interchange -floop-block -ftree-loop-distribution -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path}"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   ../%{src_dir} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
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
        -DKRB5_CONFIG=%{_bindir}/krb5-config                            \
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

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Sep 19 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
