#
# spec file for package SFEtelepathy-qt
#
# includes module(s): telepathy-qt
#
# 64Bit build commented for now since GStreamer is still 32Bit only.
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          telepathy-qt
Name:                    SFEtelepathy-qt
Summary:                 Telepathy-qt is a Qt4 package containing base classes for use in connection managers
Version:                 svn2109
License:                 LGPLv2
Source:                  http://www.belenix.org/binfiles/telepathy-qt-%{version}.tar.gz
URL:                     http://telepathy.freedesktop.org/wiki/TelepathyQt
Patch1:                  telepathy-qt-1-CMakeLists.txt.0.diff
Patch2:                  telepathy-qt-2-CMakeLists.txt.1.diff
Patch3:                  telepathy-qt-3-CMakeLists.txt.2.diff
Patch4:                  telepathy-qt-4-QtTelepathyCommon.pc.in.3.diff
Patch5:                  telepathy-qt-5-QtTelepathyCore.pc.in.4.diff
Patch6:                  telepathy-qt-6-QtTelepathyClient.pc.in.5.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEautomoc


%description
Telepathy-qt is a Qt4 package containing base classes for use in
connection managers, and proxy classes for use in clients. It's
used in at least TapiocaQt.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SFEautomoc

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

%ifarch amd64 sparcv9
cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
%endif

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

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L/lib -R/lib"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Avoid stripping of binaries.
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
