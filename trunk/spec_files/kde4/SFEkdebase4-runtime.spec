#
# spec file for package SFEkdebase4-runtime
#
# includes module(s): kdebase-runtime
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdebase-runtime
Name:                    SFEkdebase4-runtime
Summary:                 K Desktop Environment - Runtime
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdebase-runtime-%{version}.tar.bz2
Patch1:                  kdebase4-runtime-01-secure.cpp.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEqimageblitz
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEsoprano
Requires:      SFEclucene-core
Requires:      SUNWhal
Requires:      SFExine-lib
Requires:      SFElibxcb
Requires:      SFEopenexr
Requires:      SUNWzlib
Requires:      SUNWsmbar
Requires:      SUNWxwplt
Requires:      SUNWimagick
Requires:      FSWxorg-clientlibs
BuildRequires: SFEqt4-devel
BuildRequires: SFEqimageblitz-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEsoprano-devel
BuildRequires: SFEclucene-core-devel
BuildRequires: SUNWzlib
BuildRequires: SUNWsmbar
BuildRequires: SUNWhea
BuildRequires: SFEopenexr-devel
BuildRequires: SFExine-lib-devel
BuildRequires: SFElibxcb-devel
BuildRequires: SUNWimagick-devel
BuildRequires: FSWxorg-headers
Conflicts:     SFEkdebase3
BuildConflicts: SFEkdebase3-devel

%description
Core runtime for the K Desktop Environment 4.
This package is incompatible with the corresponding KDE3 package.

#%package devel
#Summary:                 %{summary} - development files
#SUNW_BaseDir:            /
#%include default-depend.inc
#Requires: %name
#Requires: SFEqt4-devel
#Requires: SFEqimageblitz-devel
#Requires: SFEkdelibs4-devel
#Requires: SFEkdepimlibs4-devel
#Requires: SFEautomoc
#Requires: SFEcmake
#Conflicts: SFEkdebase3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name


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
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

mkdir kdebld
cd kdebld

export CFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc}"
export CXXFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc}"

#
# SFW path is included for samba
#
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
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
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DSAMBA_INCLUDE_DIR:PATH=%{_prefix}/sfw/include                 \
        -DSAMBA_LIBRARIES:FILEPATH=%{_prefix}/sfw/lib/libsmbclient.so   \
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

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/index.theme


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
%{_libdir}/kde4/*.so
%dir %attr (0755, root, bin) %{_libdir}/kde4/libexec
%attr (0555, root, bin) %{_libdir}/kde4/libexec/drkonqi
%attr (6555, root, bin) %{_libdir}/kde4/libexec/kdeeject
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kdesu
%attr (6555, root, bin) %{_libdir}/kde4/libexec/kdesud
%attr (0555, root, bin) %{_libdir}/kde4/libexec/khc_docbookdig.pl
%attr (0555, root, bin) %{_libdir}/kde4/libexec/khc_htdig.pl
%attr (0555, root, bin) %{_libdir}/kde4/libexec/khc_htsearch.pl
%attr (0555, root, bin) %{_libdir}/kde4/libexec/khc_indexbuilder
%attr (0555, root, bin) %{_libdir}/kde4/libexec/khc_mansearch.pl
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kioexec
%attr (0555, root, bin) %{_libdir}/kde4/libexec/klocaldomainurifilterhelper
%attr (6555, root, bin) %{_libdir}/kde4/libexec/knetattach
%dir %attr (0755, root, bin) %{_libdir}/kde4/plugins
%{_libdir}/kde4/plugins/*
%dir %attr (0755, root, other) %{_libdir}/kconf_update_bin
%{_libdir}/kconf_update_bin/*
%dir %attr (0755, root, bin) %{_libdir}/strigi
%{_libdir}/strigi/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*
%dir %attr (0755, root, bin) %{_datadir}/sounds
%{_datadir}/sounds/*
%dir %attr (0755, root, bin) %{_datadir}/desktop-directories
%{_datadir}/desktop-directories/*

%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*
%dir %attr (0755, root, other) %{_datadir}/emoticons
%{_datadir}/emoticons/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/menus
%{_sysconfdir}/xdg/menus/*

#%files devel
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_prefix}
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*
#%dir %attr (0755, root, bin) %{_libdir}
#%dir %attr (0755, root, bin) %{_libdir}/KdepimLibs-%{version}
#%{_libdir}/KdepimLibs-%{version}/*
#%dir %attr (0755, root, bin) %{_libdir}/gpgmepp
#%{_libdir}/gpgmepp/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Jul 09 2009 - moinakg<at>belenix(dot)org
- Set some executables as setuid/gid.
- Add SocketSecurity implementation for Solaris.
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
