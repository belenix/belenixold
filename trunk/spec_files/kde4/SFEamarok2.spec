#
# spec file for package SFEamarok2
#
# includes module(s): amarok
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          amarok
%define python_version   2.6
Name:                    SFEamarok2
Summary:                 A KDE based music player for Linux and Unix
Version:                 2.1.1
License:                 GPLv2+
URL:                     http://amarok.kde.org/
Source:                  http://download.kde.org/stable/amarok/%{version}/src/amarok-%{version}.tar.bz2
Patch1:                  amarok2-01-qtscript_not_required.diff
Patch2:                  amarok2-02-lyricwiki-website.diff
Patch3:                  amarok2-03-u_int.diff

SUNW_BaseDir:            /
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWcurl
Requires:      SFEkdelibs4
Requires:      SUNWgnome-desktop-prefs
Requires:      SFElibifp
Requires:      SFElibmp4v2
Requires:      SFElibmtp
Requires:      SFElibgpod
Requires:      SUNWlibusb
Requires:      SUNWlxml
Requires:      SFEloudmouth
Requires:      SFEsoprano
Requires:      SFEtaglib
Requires:      SFEtaglib-extras
Requires:      SUNWzlib
Requires:      SFEstrigi
Requires:      SUNWlibgcrypt
Requires:      SUNWopenssl-libraries
Requires:      SFEqtscriptbindings
Requires:      SUNWmysql51u
BuildRequires: SUNWcurl-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFElibifp-devel
BuildRequires: SFElibmp4v2-devel
BuildRequires: SFElibmtp-devel
BuildRequires: SFElibgpod-devel
BuildRequires: SFElibnjb
BuildRequires: SUNWlxml-devel
BuildRequires: SFEloudmouth-devel
BuildRequires: SFEsoprano-devel
BuildRequires: SFEtaglib-devel
BuildRequires: SFEtaglib-extras-devel
BuildRequires: SFEstrigi-devel
BuildRequires: SUNWlibgcrypt-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWmysql51u
Conflicts:     SFEamarok1

%description
Amarok is a multimedia player with:
 - fresh playlist concept, very fast to use, with drag and drop
 - plays all formats supported by the various engines
 - audio effects, like reverb and compressor
 - compatible with the .m3u and .pls formats for playlists
 - nice GUI, integrates into the KDE look, but with a unique touch

#%package encumbered
#Summary:                 %{summary} - development files
#SUNW_BaseDir:            /
#%include default-depend.inc
#Requires: %name
#Requires:      SFElibnjb
#Conflicts: SFEamarok1-encumbered

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Conflicts: SFEamarok1-l10n
%endif

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
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
export CFLAGS="-march=pentium -frtti -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
export CXXFLAGS="-march=pentium -frtti -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
export LDFLAGS="-L/usr/lib -R/usr/lib -R/usr/gnu/lib -lgnuintl -lgnuiconv -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path} -L%{_prefix}/mysql/5.1/lib/mysql -R%{_prefix}/mysql/5.1/lib/mysql"
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
        -DLIBUSB_INCLUDE_DIR:PATH=%{sfw_inc}                            \
        -DLIBUSB_LIBRARIES:FILEPATH=%{sfw_lib}/libusb.so                \
        -DMYSQL_INCLUDE_DIR:PATH=%{_prefix}/mysql/5.1/include/mysql     \
        -DMYSQL_LIBRARIES:FILEPATH=%{_prefix}/mysql/5.1/lib/mysql/libmysqlclient.so \
        -DMYSQL_EMBEDDED_LIBRARIES:FILEPATH=%{_prefix}/mysql/5.1/lib/mysql/libmysqld.so \
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

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_localedir}
%endif

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
