#
# spec file for package SFEdigikam
#
# includes module(s): digikam
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          digikam
%define kde_version      4.3.1
%define python_version   2.6
Name:                    SFEdigikam
Summary:                 Advanced digital photo management application
Version:                 0.10.0
License:                 GPLv2+
URL:                     http://www.kde.org/
Source:                  %{sf_download}/digikam//digikam-%{version}.tar.bz2
Patch1:                  digikam-kde4-01-geodetictools.cpp.diff

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SUNWgnome-desktop-prefs
Requires:      SFEkdebase4-runtime
Requires:      SUNWgnome-camera
Requires:      SFEkdegraphics4
Requires:      SFEjasper
Requires:      SFElensfun
Requires:      SFEkdepimlibs4
Requires:      SUNWpng
Requires:      SUNWsqlite3
Requires:      SFElibmarblewidget
BuildRequires: SFEkdelibs4-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEkdebase4-runtime
BuildRequires: SUNWgnome-camera-devel
BuildRequires: SFEkdegraphics4-devel
BuildRequires: SFEjasper-devel
BuildRequires: SFElensfun-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWsqlite3-devel
BuildRequires: SFEkdeedu4-devel

%description
digiKam is an easy to use and powerful digital photo management application,
which makes importing, organizing and manipulating digital photos a "snap".
An easy to use interface is provided to connect to your digital camera,
preview the images and download and/or delete them.

digiKam built-in image editor makes the common photo correction a simple task.
The image editor is extensible via plugins, can also make use of the KIPI image
handling plugins to extend its capabilities even further for photo
manipulations, import and export, etc. Install the kipi-plugins packages
to use them.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEkdelibs4-devel
Requires: SUNWgnome-desktop-prefs-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SFEkdebase4-runtime
Requires: SUNWgnome-camera-devel
Requires: SFEkdegraphics4-devel
Requires: SFEjasper-devel
Requires: SFElensfun-devel
Requires: SFEkdepimlibs4-devel
Requires: SUNWpng-devel
Requires: SUNWsqlite3-devel
Requires: SFEkdeedu4-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

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

mkdir -p kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -DSOLARIS -DUSE_SOLARIS"
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

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Changes to uprev to KDE4.3.1.
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
