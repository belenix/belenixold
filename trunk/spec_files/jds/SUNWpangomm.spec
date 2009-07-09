#
#
# spec file for package SUNWpangomm
#
# includes module(s): pangomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc

%use pangomm = pangomm.spec

Name:                    SUNWpangomm
Summary:                 pangomm - C++ Wrapper for the pango Library
Version:                 %{pangomm.version}
Source:			 %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWsigcpp
Requires: SUNWcairomm
Requires: SUNWglibmm
BuildRequires: SUNWsigcpp-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWcairomm-devel
BuildRequires: SUNWglibmm-devel

%package devel
Summary:                 pangomm - C++ Wrapper for the pango Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWsigcpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%pangomm.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%if %cc_is_gcc
export CFLAGS=`echo ${CFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS=`echo ${CXXFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LDFLAGS} ${LDFLAGS_EXTRA}"
export CFLAGS="${CFLAGS} ${CFLAGS_EXTRA}"
%endif
%pangomm.build -d %name-%version

%install
%pangomm.install -d %name-%version
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/pangomm*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/devhelp
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Mon Mar 25 2009 - jeff.cai@sun.com
- Remove dependency on SUNWgtkmm
* Tue Mar 24 2009 - dave.lin@sun.com
- Add dependency on SUNWgtkmm(CR#6821116).
* Fri Aug 22 2008 - dave.lin@sun.com
- Fixed /usr/share attribute issue.
* Mon Aug 18 2008 - chris.wang@sun.com
- add manpage
* Fri Aug 01 2008 - christian.kelly@sun.com
- set copyright to gtkmm.copyright, Chris Wang will update later.
* Thu Jul 24 2008 - chris.wang@sun.com
- create
