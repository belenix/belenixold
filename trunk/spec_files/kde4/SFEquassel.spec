#
# spec file for package SFEquassel
#
# includes module(s): quassel
#
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc

%define src_dir          quassel
Name:                    SFEquassel
Summary:                 Quassel IRC is a modern, cross-platform, distributed IRC client.
Version:                 0.4.1
License:                 GPL
Source:                  http://quassel-irc.org/pub/quassel-0.4.1.tar.bz2
URL:                     http://quassel-irc.org/

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEphonon
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SFEphonon-devel


%description
Quassel IRC is a modern, cross-platform, distributed IRC client,
meaning that one (or multiple) client(s) can attach to and detach
from a central core -- much like the popular combination of screen
and a text-based IRC client such as WeeChat, but graphical.

%prep
%setup -q -c -n %name-%version

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
OPATH=${PATH}

#%ifarch amd64 sparcv9
#cd %{src_dir}-%{version}-64
#export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
#export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
#export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
#export PATH="%{qt4_bin_path64}:${OPATH}"
#export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
#
#cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
#        -DCMAKE_BUILD_TYPE=Release                                      \
#        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
#        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
#        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
#        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
#        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
#        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
#        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
#        -DBUILD_SHARED_LIBS=On                                          \
#        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1
#
#make VERBOSE=1
#cd ..
#%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L/lib -R/lib"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBIN_INSTALL_DIR=%{_bindir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

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

cd %{src_dir}-%{version}
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..
export PATH="${OPATH}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/quassel*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*

%changelog
* Sun Jul 05 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
