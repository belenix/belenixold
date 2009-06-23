#
# spec file for package SFEkdegraphics4
#
# includes module(s): kdegraphics4
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdegraphics
%define python_version   2.6
Name:                    SFEkdegraphics4
Summary:                 Graphics applications for the K Desktop Environment 4
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdegraphics-%{version}.tar.bz2
Patch1:                  kdegraphics4-01-kolourpaint.diff
Patch2:                  kdegraphics4-02-libraw_alloc.h.diff
Patch3:                  kdegraphics4-03-libraw.h.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEkdebase4-runtime
Requires:      SFEchmlib
Requires:      SUNWpcre
Requires:      SFEdjvulibre
Requires:      SFEebook-tools
Requires:      SFEexiv2
Requires:      SFEgiflib
Requires:      SFElcms
Requires:      SUNWgnome-camera
Requires:      SFEsane-backends
Requires:      SFElibspectre
Requires:      SUNWTiff
Requires:      SUNWxorg-clientlibs
Requires:      SUNWfreetype2
Requires:      SFEpoppler
Requires:      SFEqca
Requires:      SFEqimageblitz
Requires:      SFEsoprano
BuildRequires: SFEqt4-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SUNWpcre
BuildRequires: SFEdjvulibre-devel
BuildRequires: SFEebook-tools-devel
BuildRequires: SFEexiv2-devel
BuildRequires: SFElcms-devel
BuildRequires: SUNWgnome-camera-devel
BuildRequires: SFEsane-backends-devel
BuildRequires: SFElibspectre-devel
BuildRequires: SUNWTiff-devel
BuildRequires: FSWxorg-headers
BuildRequires: SFEpoppler-devel
BuildRequires: SFEqca-devel
BuildRequires: SFEqimageblitz-devel
BuildRequires: SFEsoprano-devel
Conflicts:     SFEkdegraphics3
Conflicts:     SFElibkdcraw
Conflicts:     SFElibkexiv2
Conflicts:     SFElibkipi
BuildConflicts: SFEkdegraphics3-devel
BuildConflicts: SFElibkdcraw-devel
BuildConflicts: SFElibkexiv2-devel
BuildConflicts: SFElibkipi-devel

%description
Graphics applications for the K Desktop Environment 4, including
* gwenview (an image viewer)
* kamera (digital camera support)
* kcolorchooser (a color chooser)
* kolourpaint4 (an easy-to-use paint program)
* kruler (screen ruler and color measurement tool)
* ksnapshot (screen capture utility)
* okular (a document viewer)


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
Requires: SFEchmlib
Requires: SUNWpcre
Requires: SFEdjvulibre-devel
Requires: SFEebook-tools-devel
Requires: SFEexiv2-devel
Requires: SFEgiflib
Requires: SFElcms-devel
Requires: SUNWgnome-camera-devel
Requires: SFEsane-backends-devel
Requires: SFElibspectre-devel
Requires: SUNWTiff-devel
Requires: FSWxorg-headers
Requires: SFEpoppler-devel
Requires: SFEqca-devel
Requires: SFEqimageblitz-devel
Requires: SFEsoprano-devel
Conflicts: SFEkdegraphics3-devel
Conflicts: SFElibkdcraw-devel
Conflicts: SFElibkexiv2-devel
Conflicts: SFElibkipi-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdegraphics3-doc

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

mkdir kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export CXXFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc}"
export LDFLAGS="%_ldflags -L%{_prefix}/poppler/lib -R%{_prefix}/poppler/lib -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/poppler/lib/pkgconfig:%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
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

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
