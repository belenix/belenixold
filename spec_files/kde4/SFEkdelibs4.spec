#
# spec file for package SFEkdelibs
#
# includes module(s): kdelibs
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc

%define src_dir          kdelibs
Name:                    SFEkdelibs4
Summary:                 Libraries for K Desktop Environment Version 4
Version:                 4.3.1
License:                 LGPLv2+
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdelibs-%{version}.tar.bz2
Patch1:                  kdelibs4-01-kpropertiesdialog.cpp.diff
Patch2:                  kdelibs4-02-kbuildsycoca.cpp.diff
Patch3:                  kdelibs4-03-kcrash.cpp.diff
Patch4:                  kdelibs4-04-install-all-css.diff
Patch5:                  kdelibs4-05-cmake.diff
Patch6:                  kdelibs4-06-kstandarddirs.diff
Patch7:                  kdelibs4-07-file_unix.diff
Patch9:                  kdelibs4-09-nepomuk-rcgen.diff
Patch10:                 kdelibs4-10-klocale.cpp.diff
Patch12:                 kdelibs4-12-kpty.diff

# New ones for 4.3.0
Patch13:                 kdelibs4-13-bookmarks.diff
Patch14:                 kdelibs4-14-CVE-2009-2702.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEphonon
Requires:      SFEstrigi
Requires:      SFEsoprano
Requires:      SFEaspell
Requires:      SUNWpcre
Requires:      SUNWgnome-spell
Requires:      SFEredland
Requires:      SFEraptor
Requires:      SFEclucene-core
Requires:      SFEgccruntime
Requires:      SFEopenexr
Requires:      SFEilmbase
Requires:      SFElzma
BuildRequires: SFEqt4-devel
BuildRequires: SFEphonon-devel
BuildRequires: SFEstrigi-devel
BuildRequires: SFEsoprano-devel
BuildRequires: SFEaspell-devel
BuildRequires: SUNWpcre
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
BuildRequires: SFEclucene-core-devel
BuildRequires: SUNWgnome-spell-devel
BuildRequires: SFEopenexr-devel
BuildRequires: SFEilmbase-devel
BuildRequires: SFElzma-devel
Conflicts:     SFEkdelibs3
Conflicts:     SFEkdelibs3-root
Conflicts:     SFEkdeaddons3
Conflicts:     SFEkdeedu3
Conflicts:     SFEkdewebdev3
Conflicts:     SFEkdesdk3
BuildConflicts: SFEkdelibs3
BuildConflicts: SFEkdelibs3-devel
BuildConflicts: SFEkdeedu3-devel
BuildConflicts: SFEkdesdk3-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEredland-devel
Requires: SFEraptor-devel
Requires: SFEclucene-core-devel
Requires: SFEautomoc
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SFEdoxygen
Requires: SFEgraphviz
Requires: SUNWgnome-spell-devel
Requires: SFEaspell-devel
Requires: SFEstrigi-devel
Requires: SFEsoprano-devel
Requires: SFEphonon-devel
Requires: SFEopenexr-devel
Requires: SFEilmbase-devel
Requires: SFElzma-devel
Conflicts: SFEkdelibs3-devel
Conflicts: SFEkdeedu3-devel
Conflicts: SFEkdesdk3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts: SFEkdesdk3-doc
Conflicts: SFEkdewebdev3-doc
Conflicts: SFEkdeaddons3-doc


%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p0
%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
cd ..

#%ifarch amd64 sparcv9
#cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
#%endif

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

#%ifarch amd64 sparcv9
#mkdir kdebld-64
#cd kdebld-64
#export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc} ${GCC_EXTRA_OPTS}"
#export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc} ${GCC_EXTRA_OPTS}"
#export LDFLAGS="%_ldflags64 -lsocket -lnsl -L/lib/%{_arch64} -R/lib/%{_arch64} %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
#export PATH="%{qt4_bin_path64}:%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
#export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
#export CMAKE_LIBRARY_PATH="%{xorg_lib64}:%{gnu_lib64}:%{_prefix}/lib/%{_arch64}:/lib/%{_arch64}"
#
#cmake   ../%{src_dir}-%{version}-64 -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
#        -DCMAKE_BUILD_TYPE=Release                                      \
#        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
#        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
#        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
#        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
#        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
#        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
#        -DDBUS_INTERFACES_INSTALL_DIR=%{_datadir}/dbus-1/interfaces     \
#        -DDBUS_SERVICES_INSTALL_DIR=%{_datadir}/dbus-1/services         \
#        -DBUILD_SHARED_LIBS=On                                          \
#        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
#        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1
#
#make VERBOSE=1
#cd ..
#%endif

mkdir -p kdebld
cd kdebld

export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -floop-interchange -floop-block -ftree-loop-distribution -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -floop-interchange -floop-block -ftree-loop-distribution -fPIC -DPIC -I%{gnu_inc} -DSOLARIS -DUSE_SOLARIS -D_OS_SOLARIS_"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path}"
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

#%ifarch amd64 sparcv9
#cd %{src_dir}-%{version}-64
#export PATH="%{qt4_bin_path64}:${OPATH}"
#
#make install DESTDIR=$RPM_BUILD_ROOT
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
#cd ..
#%endif

cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}/%{_sysconfdir}/xdg/menus/applications.menu \
   ${RPM_BUILD_ROOT}/%{_sysconfdir}/xdg/menus/kapplications.menu
cd ..
export PATH="${OPATH}"


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
%dir %attr (0755, root, bin) %{_libdir}/kde4/plugins
%{_libdir}/kde4/plugins/*
%dir %attr (0755, root, bin) %{_libdir}/kde4/libexec
%{_libdir}/kde4/libexec/filesharelist
%attr (4755, root, bin) %{_libdir}/kde4/libexec/fileshareset
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kconf_update
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kdesu_stub
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kdontchangethehostname
%attr (4755, root, bin) %{_libdir}/kde4/libexec/kgrantpty
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kio_http_cache_cleaner
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kioslave
%attr (0555, root, bin) %{_libdir}/kde4/libexec/klauncher
%attr (0555, root, bin) %{_libdir}/kde4/libexec/kmailservice
%attr (4755, root, bin) %{_libdir}/kde4/libexec/kpac_dhcp_helper
%attr (0555, root, bin) %{_libdir}/kde4/libexec/ksendbugmail
%attr (0555, root, bin) %{_libdir}/kde4/libexec/ktelnetservice
%attr (0555, root, bin) %{_libdir}/kde4/libexec/lnusertemp
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/menus
%attr (0755, root, sys) %{_sysconfdir}/xdg/menus/kapplications.menu

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*

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
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Make some executables set-uid.
* Sat Sep 19 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Changes for upreving to KDE 4.3.1
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Rebuild with Solaris build flags.
* Sun Jul 26 2009 - moinakg<at>belenix(dot)org
- Add graphite loop optimizations for performance.
* Tue Jul 07 2009 - moinakg(at)belenix<dot>org
- Add a plasmoid patch.
- Add proper pty handling for Solaris.
* Thu Jul 02 2009 - moinakg@belenix(dot)org
- Patch up a locale issue.
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
