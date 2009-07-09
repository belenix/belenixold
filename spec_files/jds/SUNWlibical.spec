#
# spec file for package SUNWlibical.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#

%include Solaris.inc

Name:                   SUNWlibical
License:                LGPL v2.1
Group:                  System/Libraries
Summary:                Libical is an Open Source implementation of the IETF's iCalendar Calendaring and Scheduling protocols
Version:                0.43
URL:                    http://sourceforge.net/projects/freeassociation/
Distribution:           Java Desktop System
Vendor:                 Sun Microsystems, Inc.
Source:                 http://downloads.sourceforge.net/freeassociation/libical-%{version}.tar.gz
Source1:		%{name}-manpages-0.1.tar.gz
#owner:fujiwara date:2008-12-12 type:bug bugster:6783979 bugid:2417984
Patch1:                 libical-01-g11n-strstriplt-utf8.diff
SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:         %{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWperl584core
BuildRequires:          SUNWperl584usr
BuildRequires:          SFEcmake 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n libical-%{version}
%patch1 -p1

cd %{_builddir}/libical-%version
gzcat %SOURCE1 | tar xf -


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
export LDFLAGS="%_ldflags"
export LD_LIBRARY_PATH="%_pkg_config_path"
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=%{build_type} \
		-DBUILD_SHARED_LIBS=On -DICAL_ERRORS_ARE_FATAL=false \
		-DLIB_INSTALL_DIR=%{_libdir} ..
make

%ifarch amd64 sparcv9
mkdir ../build-%{_arch64} && cd ../build-%{_arch64}
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags"
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
%ifarch amd64 sparcv9
cd ../build-%{_arch64}
make install DESTDIR=$RPM_BUILD_ROOT
%endif

cd %{_builddir}/libical-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc(bzip2) THANKS
%doc(bzip2) COPYING
%doc(bzip2) LICENSE
%doc(bzip2) README
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, other) %{_docdir}
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
* Tue Jan 15 2009 - jedy.wang@sun.com
- Set default dir/file attribute for base pkg to correct invalid owner issue.
* Tue Jan 13 2009 - jedy.wang@sun.com
- Bump to 0.43.
* Sun Jan 11 2009 - dave.lin@sun.com
- Change to depend on SUNWcmake instead of SFEcmake.
* Mon Jan 05 2009 - jedy.wang@sun.com
- Add manpage.
* Fri Dec 12 2008 - takao.fujiwara@sun.com
- Add g11n-strstriplt-utf8.diff to work strstrip with UTF-8.
* Thu Nov  27 2008 - jedy.wang@sun.com
- Bump to 0.42.
- Add %attr to _datadir and _docdir to fix build.
* Tue Nov  13 2008 - jedy.wang@sun.com
- Move from sfe to spec-files.
* Tue Nov  11 2008 - jedy.wang@sun.com
- Bump to 0.4.1.
* Thu Oct  30 2008 - jedy.wang@sun.com
- Bump to 0.4.0.
- Use cmake to build.
- Add patch 01-build.diff.
* Mon Jan  21 2008 - moinak.ghosh@sun.com
- Initial spec.
