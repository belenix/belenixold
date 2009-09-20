#
# spec file for package SFEkdemultimedia4
#
# includes module(s): kdemultimedia
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdemultimedia
%define python_version   2.6
Name:                    SFEkdemultimedia4
Summary:                 Multimedia applications for KDE 4
Version:                 4.3.1
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdemultimedia-%{version}.tar.bz2
Patch1:                  kdemultimedia4-01-plat_sun.c.diff
Patch2:                  kdemultimedia4-02-paranoia.diff
Patch3:                  kdemultimedia4-03-libkcompactdisc_cmakelists.diff
Patch4:                  kdemultimedia4-04-wmlib_audio_sun.c.diff
Patch5:                  kdemultimedia4-05-mixer.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFElibcdio
Requires:      SFEkdebase4-workspace
Requires:      SUNWflac
Requires:      SUNWlibtheora
Requires:      SFElibtunepimp
Requires:      SUNWmusicbrainz
Requires:      SUNWogg-vorbis
Requires:      SFEtaglib
Requires:      SFElibxcb
Requires:      SUNWgnome-audio
Requires:      SFEakode
Requires:      SFExine-lib
BuildRequires: SFElibcdio-devel
BuildRequires: SFEkdebase4-workspace-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SUNWflac-devel
BuildRequires: SUNWlibtheora-devel
BuildRequires: SUNWmusicbrainz-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SFEtaglib-devel
BuildRequires: SFElibxcb-devel
BuildRequires: SFElibtunepimp-encumbered
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SFElame-devel
BuildRequires: SFEakode-devel
BuildRequires: SFEakode-encumbered
BuildRequires: SFExine-lib-devel
BuildRequires: SFExine-lib-encumbered
Conflicts:     SFEkdemultimedia3
Conflicts:     SFEkdemultimedia3-root
BuildConflicts: SFEkdemultimedia3-devel

%description
This package contains multimedia applications for KDE 4.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFElibcdio-devel
Requires: SFEkdebase4-workspace-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SUNWflac-devel
Requires: SUNWlibtheora-devel
Requires: SFElibmusicbrainz3-devel
Requires: SUNWogg-vorbis-devel
Requires: SFEtaglib-devel
Requires: SFElibxcb-devel
Requires: SUNWgnome-audio-devel
Requires: SFEakode-devel
Requires: SFExine-lib-devel
Conflicts: SFEkdemultimedia3-devel

%package encumbered
Summary:                 Encumbered codecs for %{name}
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFElame
Requires: SFExine-lib-encumbered
Requires: SFEakode-encumbered
Conflicts:     SFEkdemultimedia3-encumbered

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdemultimedia3-doc

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
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

mkdir -p kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"

cmake  --trace ../%{src_dir}-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
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
%{_libdir}/kde4/libaudiocd_encoder_vorbis.so
%{_libdir}/kde4/kcm_cddb.so
%{_libdir}/kde4/kio_audiocd.so
%{_libdir}/kde4/libaudiocd_encoder_flac.so
%{_libdir}/kde4/libaudiocd_encoder_wav.so
%{_libdir}/kde4/kcm_audiocd.so
%{_libdir}/kde4/dragonpart.so
%{_libdir}/kde4/videopreview.so

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*

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
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files encumbered
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/libaudiocd_encoder_lame.so

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Sep 20 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Changes for upreving to KDE 4.3.1
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial version.
