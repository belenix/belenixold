#
# spec file for package SFEsoprano
#
# includes module(s): soprano
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          soprano
Name:                    SFEsoprano
Summary:                 Qt wrapper API to different RDF storage solutions
Version:                 2.2.3
License:                 LGPLv2+
URL:                     http://soprano.sourceforge.net/
Source:                  %{sf_download}/soprano/soprano-%{version}.tar.bz2

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEredland
Requires:      SFEraptor
Requires:      SFEclucene-core
Requires:      SFErasqal
Requires:      SUNWj6rt
BuildRequires: SFEredland-devel
BuildRequires: SFEraptor-devel
BuildRequires: SFEautomoc
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
BuildRequires: SFEclucene-core-devel
BuildRequires: SFErasqal-devel
BuildRequires: SUNWj6dev


%description
Soprano (formerly known as QRDF) is a library which provides
a highly usable object-oriented C++/Qt4 framework for RDF data.
It uses different RDF storage solutions as backends through a
simple plugin system. Soprano is targetted at desktop
applications that need a RDF data storage solution. It has been
optimized for easy usage and simplicity.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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


%prep
%setup -q -c -n %name-%version
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
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib64}:%{gnu_lib64}:%{_prefix}/lib/%{_arch64}:/lib/%{_arch64}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_DESTINATION=%{_libdir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DJAVA_INCLUDE_PATH2=${JAVA_HOME}/include/solaris               \
        -DJAVA_AWT_LIBRARY:FILEPATH=${JAVA_HOME}/jre/lib/%{_arch64}/libjawt.so \
        -DJAVA_JVM_LIBRARY:FILEPATH=${JAVA_HOME}/jre/lib/%{_arch64}/server/libjvm.so \
        -DBUILD_SHARED_LIBS=On                                          \
        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path}"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DLIB_DESTINATION=%{_libdir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DJAVA_INCLUDE_PATH2=${JAVA_HOME}/include/solaris               \
        -DSOPRANO_BUILD_API_DOCS=On                                     \
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
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
for prg in sopranocmd onto2vocabularyclass sopranod
do
	mv ${RPM_BUILD_ROOT}%{_bindir}/${prg} ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
done
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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sopranocmd
%{_bindir}/onto2vocabularyclass
%{_bindir}/sopranod

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/soprano
%{_libdir}/soprano/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/soprano
%{_datadir}/soprano/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/interfaces
%{_datadir}/dbus-1/interfaces/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sopranocmd
%{_bindir}/%{_arch64}/onto2vocabularyclass
%{_bindir}/%{_arch64}/sopranod

%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/soprano
%{_libdir}/%{_arch64}/soprano/*
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
- Initial version.
