#
# spec file for package SFEkdeedu4
#
# includes module(s): kdeedu
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define src_dir          kdeedu
%define python_version   2.6
Name:                    SFEkdeedu4
Summary:                 Educational applications for KDE 4.
Version:                 4.2.4
License:                 GPLv2
URL:                     http://www.kde.org/
Source:                  http://gd.tuwien.ac.at/pub/kde/stable/%{version}/src/kdeedu-%{version}.tar.bz2
Patch1:                  kdeedu4-01-indi_nodrivers.diff
Patch2:                  kdeedu4-02-kalziumutils.cpp.diff
Patch3:                  kdeedu4-03-kstars_vars.diff
Patch4:                  kdeedu4-04-calendarwidget.cpp.diff
Patch5:                  kdeedu4-05-constraintsolver_isinf.diff
Patch6:                  kdeedu4-06-isfinite.diff

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SFEkdebase4-workspace
Requires:      SFEboost-gpp
Requires:      SFEcfitsio
Requires:      SUNWgnome-desktop-prefs
Requires:      SFEgsl
Requires:      SFElibnova
Requires:      SFElibqalculate
Requires:      SUNWlibusb
Requires:      SUNWlxml
Requires:      SUNWlxsl
Requires:      SUNWocaml
Requires:      SUNWPython26
Requires:      SFEreadline
Requires:      SFEopenbabel
Requires:      SFEsjfonts
Requires:      SFEdrfonts
Requires:      SFEdmfonts
Requires:      SFEocaml-findlib
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdebase4-workspace-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEcfitsio-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SFEeigen
BuildRequires: SFEgmm
BuildRequires: SFEgsl-devel
BuildRequires: SFElibnova-devel
BuildRequires: SFElibqalculate-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFEreadline-devel
BuildRequires: SFEopenbabel-devel
BuildRequires: SFEocaml-findlib-devel
Conflicts:     SFEkdeedu3
BuildConflicts: SFEkdeedu3-devel

%description
Educational/Edutainment applications for KDE4 including:
* blinken: Simon Says Game
* kalzium: A periodic table of the elements
* kanagram: Anagram game
* kgeography: Learn geography
* khangman: Hangman Game
* kiten: Japanese Reference/Study Tool
* klettres: French alphabet tutor
* ktouch: Learn and practice touch typing
* kturtle: Logo Programming Environment
* kwordquiz: Flashcard and vocabulary learning
* parley: Vocabulary Trainer
* step: Interactive physical simulator


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SFEkdelibs4-devel
Requires: SFEkdebase4-workspace-devel
Requires: SFEautomoc
Requires: SFEcmake
Requires: SFEkdebase4-runtime
Conflicts: SFEkdeedu3-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkdeedu3-doc

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
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
export CFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -I%{_includedir}/python%{python_version} -D__C99FEATURES__ -D_BOOL_EXISTS"
export CXXFLAGS="-march=pentium4 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -I%{_includedir}/python%{python_version} -D__C99FEATURES__ -D_BOOL_EXISTS"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"
BOOSTPYLIB="-lpython%{python_version} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 -lboost_python-mt"

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
        -DBOOST_PYTHON_INCLUDES=%{_includedir}/boost/gcc4               \
        -DBOOST_PYTHON_LIBS="${BOOSTPYLIB}"                             \
        -DEXPERIMENTAL_PYTHON_BINDINGS=TRUE                             \
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

mv ${RPM_BUILD_ROOT}/%{_libdir}/python%{python_version}/site-packages \
   ${RPM_BUILD_ROOT}/%{_libdir}/python%{python_version}/vendor-packages
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
%dir %attr (0755, root, bin) %{_libdir}/avogadro-kalzium
%{_libdir}/avogadro-kalzium/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%{_datadir}/kde4/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*

%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.a

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial version.
