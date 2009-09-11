#
# spec file for package SFEqt4-jambi
#
# includes module(s): qt4-jambi
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          qtjambi-src-gpl
Name:                    SFEqtjambi
Summary:                 QT/Jambi is a Java Framework based on QT/X11.
Version:                 4.4.3_01
License:                 GPL
URL:                     http://www.trolltech.com/
Source:                  http://get.qtsoftware.com/qtjambi/source/qtjambi-src-gpl-%{version}.tar.gz
Source2:                 SFEqtjambi.copyright
Patch1:                  qtjambi-01-qtjambi_core.h.2.diff
Patch2:                  qtjambi-02-qtjambi_core.h.3.diff
Patch3:                  qtjambi-05-java.pro.5.diff
Patch4:                  qtjambi-04-solaris-jni.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEqt4
BuildRequires: SFEqt4-devel
Requires: SFEgccruntime
BuildRequires: SFEgcc
Requires: SUNWj6rt
BuildRequires: SUNWj6dev
BuildRequires: SUNWant

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEgcc

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
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
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/gcc
unset MAKELEVEL
unset MAKEFLAGS
ARCH=""
export JAVA_HOME=%{_prefix}/java

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -D__EXTENSIONS__ -D_POSIX_PTHREAD_SEMANTICS -D_STDC_C99 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_REENTRANT -I${JAVA_HOME}/include/solaris"
export CXXFLAGS="%cxx_optflags64 -D__EXTENSIONS__ -D_POSIX_PTHREAD_SEMANTICS -D_STDC_C99 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_REENTRANT -I${JAVA_HOME}/include/solaris"
export LDFLAGS="%_ldflags64"
export QTDIR="%{_prefix}"
export QMAKESPEC="solaris-g++-64"
UNAMEP=`uname -p`

if [ "${UNAMEP}" = "sparc" ] ; then
	export ARCH="sparcv9"
else
	export ARCH="amd64"
fi

ant all
ant -f build_generator_example.xml
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -D__EXTENSIONS__ -D_POSIX_PTHREAD_SEMANTICS -D_STDC_C99 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_REENTRANT -I${JAVA_HOME}/include/solaris"
export CXXFLAGS="%cxx_optflags -D__EXTENSIONS__ -D_POSIX_PTHREAD_SEMANTICS -D_STDC_C99 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -D_REENTRANT -I${JAVA_HOME}/include/solaris"
export LDFLAGS="%_ldflags"
export QTDIR="%{_prefix}"
export QMAKESPEC="solaris-g++"

ant all
ant -f build_generator_example.xml
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd %{src_dir}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -rf ${RPM_BUILD_ROOT}/openjpeg
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/frames_to_mj2
%{_bindir}/mj2_to_frames
%{_bindir}/wrap_j2k_in_mj2
%{_bindir}/extract_j2k_from_mj2
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/frames_to_mj2
%{_bindir}/%{_arch64}/mj2_to_frames
%{_bindir}/%{_arch64}/wrap_j2k_in_mj2
%{_bindir}/%{_arch64}/extract_j2k_from_mj2
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
