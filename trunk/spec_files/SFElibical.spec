#
# spec file for package SFEopenexr.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                   SFElibical
Summary:                Libical is an Open Source implementation of the IETF's iCalendar Calendaring and Scheduling protocols
Version:                0.43
Source:                 %{sf_download}/freeassociation/libical-%{version}.tar.gz
Patch1:                 libical-01-g11n-strstriplt-utf8.diff
SUNW_Copyright:         %{name}.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython
BuildRequires: SUNWPython-devel
Requires: SUNWperl584core
BuildRequires: SUNWperl584usr
BuildRequires: SFEswig
BuildRequires: SFEcmake

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n libical-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %debug_build
%define build_type Debug
%else
%define build_type Release
%endif

mkdir build && cd build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export LD_LIBRARY_PATH="%_pkg_config_path"
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=%{build_type} \
                -DBUILD_SHARED_LIBS=On -DICAL_ERRORS_ARE_FATAL=false \
                -DLIB_INSTALL_DIR=%{_libdir} ..
make

%ifarch amd64 sparcv9
mkdir ../build-%{_arch64} && cd ../build-%{_arch64}
export CFLAGS="%optflags64"
%if %("%_ldflags64" != "")
export LDFLAGS="%_ldflags64 -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
%else
export LDFLAGS="%_ldflags -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
%endif
export LD_LIBRARY_PATH=%{_libdir}/%{_arch64}/pkgconfig
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=%{build_type} \
                -DBUILD_SHARED_LIBS=On -DICAL_ERRORS_ARE_FATAL=false \
                -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64} ..
make
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*.*a
%ifarch amd64 sparcv9
cd ../build-%{_arch64}
make install DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat Apr 18 2009 - moinakg@gmail.com
- Bump to latest version that uses Cmake and enable 64Bit build.
* Mon Jan 21 2008 - moinak.ghosh@sun.com
- Initial spec.
