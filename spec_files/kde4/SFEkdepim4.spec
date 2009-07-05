#
# spec file for package SFEkdepim4
#
# includes module(s): kdepim
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdepim
%define python_version   2.6
Name:                    SFEkdepim4
Summary:                 PIM ((Personal Information Manager) applications for KDE4
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdepim-%{version}.tar.bz2
Patch1:                  kdepim4-01-kmail.diff
Patch2:                  kdepim4-02-kmail.diff

SUNW_BaseDir:            /
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEkdebase4-runtime
Requires:      SUNWgnome-desktop-prefs
Requires:      SFEboost-gpp
Requires:      SFEakonadi
Requires:      SUNWPython26
Requires:      SFEgnokii
Requires:      SFEgpgme
Requires:      SFElibassuan
Requires:      SFElibical
Requires:      SUNWlxsl
Requires:      SUNWpilot-link
Requires:      SUNWPython26
Requires:      SFEsoprano
Requires:      SFEqca
Requires:      SUNWzlib
BuildRequires: SFEqt4-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEkdebase4-runtime
BuildRequires: SUNWgnome-desktop-prefs
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEakonadi-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFElibical-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SUNWbison
BuildRequires: SUNWflexlex
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWpilot-link-devel
BuildRequires: SFEsoprano-devel
BuildRequires: SFEqca-devel
BuildRequires: SUNWgnome-common-devel
Conflicts:     SFEkdepim3
BuildConflicts: SFEkdepim3-devel

%description
%{summary}, including:
* akregator: feed aggregator
* kmail: email client
* knode: newsreader
* knotes: sticky notes for the desktop
* kontact: integrated PIM management
* korganizer: journal, appointments, events, todos
* kpilot: HotSync(R) software for Palm OS(R) devices

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEkdelibs4-devel
Requires: SFEkdepimlibs4-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SFEkdebase4-runtime
Requires: SUNWgnome-desktop-prefs
Requires: SFEboost-gpp-devel
Requires: SFEakonadi-devel
Requires: SUNWPython26-devel
Requires: SFElibical-devel
Requires: SUNWbison
Requires: SUNWflexlex
Requires: SUNWlxsl-devel
Requires: SUNWpilot-link-devel
Requires: SFEsoprano-devel
Requires: SFEqca-devel
Requires: SUNWgnome-common-devel
Conflicts: SFEkdepim3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdepim3-doc

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p0
%patch2 -p0
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
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"
export PYTHON="/usr/bin/python%{python_version}"

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
%dir %attr (0755, root, bin) %{_libdir}/strigi
%{_libdir}/strigi/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

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
%dir %attr (0755, root, other) %{_datadir}/akonadi
%{_datadir}/akonadi/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

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
* Sun Jul 05 2009 - moinakg<at>gmail(dot)com
- Initial version.
