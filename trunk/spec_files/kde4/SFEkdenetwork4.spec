#
# spec file for package SFEkdenetwork4
#
# includes module(s): kdenetwork
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdenetwork
%define python_version   2.6
Name:                    SFEkdenetwork4
Summary:                 Core applications for the K Desktop Environment 4
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdenetwork-%{version}.tar.bz2
Patch1:                  kdenetwork4-01-system-libgadu.diff
Patch2:                  kdenetwork4-02-kopete-view-history.diff
Patch3:                  kdenetwork4-03-kopete-ymsg16.diff
Patch4:                  kdenetwork4-04-kopete-rtf.ll.diff
Patch5:                  kdenetwork4-05-connectioncontroller-bzero.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEboost-gpp
Requires:      SFEgiflib
Requires:      SUNWglib2
Requires:      SFEgmp
Requires:      SFElibgadu
Requires:      SUNWgnu-idn
Requires:      SFElibmsn
Requires:      SFElibvncserver
Requires:      SUNWlxml
Requires:      SUNWlxsl
Requires:      SFEmeanwhile
Requires:      SFEopenldap
Requires:      SUNWslpu
Requires:      SFEortp
Requires:      SUNWpcre
Requires:      SFEqca
Requires:      SFEkdebase4-workspace
Requires:      SFEqimageblitz
Requires:      SFEsoprano
Requires:      SUNWspeex
Requires:      SUNWsqlite3
Requires:      SFEjasper
Requires:      SUNWavahi-bridge-dsd
Requires:      SUNWgnome-im-client
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEgiflib
BuildRequires: SUNWglib2-devel
BuildRequires: SFEgmp-devel
BuildRequires: SFElibgadu-devel
BuildRequires: SFElibmsn-devel
BuildRequires: SFElibvncserver-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SFEmeanwhile-devel
BuildRequires: SFEopenldap-devel
BuildRequires: SFEortp-devel
BuildRequires: SUNWpcre
BuildRequires: SFEqca-devel
BuildRequires: SFEkdebase4-workspace-devel
BuildRequires: SFEqimageblitz-devel
BuildRequires: SFEsoprano-devel
BuildRequires: SUNWsqlite3-devel
BuildRequires: SFEjasper-devel
BuildRequires: SUNWavahi-bridge-dsd-devel
BuildRequires: SUNWgnome-im-client-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
Conflicts:     SFEkdenetwork3
BuildConflicts: SFEkdenetwork3-devel

%description
Networking applications, including:
* kget: downloader manager
* kopete: chat client
* kppp: dialer and front end for pppd
* krdc: a client for Desktop Sharing and other VNC servers
* krfb: Desktop Sharing server, allow others to access your desktop via VNC

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEkdelibs4-devel
Requires: SFEkdepimlibs4-devel
Requires: SFEboost-gpp-devel
Requires: SFEgiflib
Requires: SUNWglib2-devel
Requires: SFEgmp-devel
Requires: SFElibgadu-devel
Requires: SFElibmsn-devel
Requires: SFElibvncserver-devel
Requires: SUNWlxml-devel
Requires: SUNWlxsl-devel
Requires: SFEmeanwhile-devel
Requires: SFEopenldap-devel
Requires: SFEortp-devel
Requires: SUNWpcre
Requires: SFEqca-devel
Requires: SFEkdebase4-workspace-devel
Requires: SFEqimageblitz-devel
Requires: SFEsoprano-devel
Requires: SUNWsqlite3-devel
Requires: SFEjasper-devel
Requires: SUNWavahi-bridge-dsd-devel
Requires: SUNWgnome-im-client-devel
Requires: SFEautomoc
Requires: SFEcmake
Conflicts: SFEkdenetwork3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdenetwork3-doc

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
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
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

mkdir kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export CXXFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl -lQtGui -lkdeui -lQtNetwork -lX11 -lXext -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"

cmake   ../%{src_dir}-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DDBUS_INTERFACES_INSTALL_DIR=%{_datadir}/dbus-1/interfaces     \
        -DDBUS_SERVICES_INSTALL_DIR=%{_datadir}/dbus-1/services         \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DIDN_INCLUDEDIR=%{_includedir}/idn                             \
        -DIDN_LIBRARIES=%{_libdir}/libidn.so                            \
        -DLIBMEANWHILE_INCLUDES=%{_includedir}/meanwhile                \
        -DLIBMEANWHILE_LIBRARY=%{_libdir}/libmeanwhile.so               \
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
export PATH="${OPATH}"
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Jul 02 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
