#
# spec file for package SFEkdepimlibs
#
# includes module(s): kdepimlibs
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdepimlibs
Name:                    SFEkdepimlibs4
Summary:                 Libraries for PIM data management in KDE4
Version:                 4.2.4
License:                 LGPLv2+
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdepimlibs-%{version}.tar.bz2

#
# Ugly workaround for a PyKDE4 sip issue that tries to use
# assignment with messagethreadingattribute objects.
#
Patch1:                  kdepimlibs-01-messagethreadingattribute.h.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEqimageblitz
Requires:      SFEkdelibs4
Requires:      SUNWxwplt
BuildRequires: SFEqt4-devel
BuildRequires: SFEqimageblitz-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
Conflicts:     SFEkdebase3
BuildConflicts: SFEkdebase3-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires:      SFEqt4
Requires:      SFEakonadi
Requires:      SFEgpgme
Requires:      SFEkdelibs4
Requires:      SFEboost-gpp
Requires:      SFEcyrus-sasl
Requires:      SFElibical
Requires:      SFEopenldap
Requires:      SFEphonon
BuildRequires: SFEqt4-devel
BuildRequires: SFEakonadi-devel
BuildRequires: SFEgpgme
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEcyrus-sasl
BuildRequires: SFElibical-devel
BuildRequires: SFEopenldap-devel
BuildRequires: SFEphonon-devel
Conflicts:     SFEkdepim3
BuildConflicts: SFEkdepim3-devel

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
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DLBER_LIBRARIES:FILEPATH=%{gnu_lib}/liblber.so                 \
        -DLDAP_INCLUDE_DIR:PATH=%{gnu_inc}/openldap                     \
        -DLDAP_LIBRARIES:FILEPATH=%{gnu_lib}/libldap-2.4.so             \
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


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
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

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/KdepimLibs-%{version}
%{_libdir}/KdepimLibs-%{version}/*
%dir %attr (0755, root, bin) %{_libdir}/gpgmepp
%{_libdir}/gpgmepp/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Remove dependency on self.
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
