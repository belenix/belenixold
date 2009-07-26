#
# spec file for package SFEkdegames4
#
# includes module(s): kdebase
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdegames
%define python_version   2.6
Name:                    SFEkdegames4
Summary:                 Games collection for KDE 4
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdegames-%{version}.tar.bz2
Patch1:                  kdegames4-01-ksirk-kde#187235.diff
Patch2:                  kdegames4-02-ksirk-rh#486380.diff
Patch3:                  kdegames4-03-const_names.diff
Patch4:                  kdegames4-04-jdns.diff
Patch5:                  kdegames4-05-undef_sun.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SFEkdebase4-workspace
#
# Unfortunate dependency due to the way JDS tends to do clumped packaging.
# libggz, ggz-client-libs are clumped into gnome-games package - UGH!
#
Requires:      SUNWgnome-games
Requires:      SFEqca
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdebase4-workspace-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SUNWgnome-games-devel
BuildRequires: SFEqca-devel
Conflicts:     SFEkdegames3
BuildConflicts: SFEkdegames3-devel

%description
Games for the K Desktop Environment 4.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SFEkdelibs4-devel
Requires: SFEkdebase4-workspace-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SUNWgnome-games-devel
Requires: SFEqca-devel
Conflicts: SFEkdegames3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdegames3-doc

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
export CFLAGS="-march=pentium4 -fno-omit-frame-pointer -g -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export CXXFLAGS="-march=pentium4 -fno-omit-frame-pointer -g -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
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
        -DSKIP_GGZCONFIG=1                                              \
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
%dir %attr (0755, root, sys) %{_datadir}
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
* Sun Jul 26 2009 - moinakg<at>belenix(dot)org
- Initial version.
