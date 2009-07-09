#
# spec file for package SUNWbabl
#
# includes module(s): babl
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use babl_64 = babl.spec
%endif
%include base.inc
%use babl = babl.spec

Name:                    SUNWbabl
Summary:                 Babl is a dynamic, any to any, pixel format conversion library.
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SUNWbabl.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWw3m
%if %cc_is_gcc
Requires:                SFEgccruntime
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%babl_64.prep -d %name-%version/%_arch64
%endif
mkdir %name-%version/%{base_arch}
%babl.prep -d %name-%version/%{base_arch}
cd %{_builddir}/%name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
%ifarch amd64 sparcv9
%babl_64.build -d %name-%version/%_arch64
%endif

%babl.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%babl_64.install -d %name-%version/%_arch64
%endif

%babl.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch} babl-%{babl.version}/AUTHORS
%doc -d %{base_arch} babl-%{babl.version}/README
%doc(bzip2) -d %{base_arch} babl-%{babl.version}/ChangeLog
%doc(bzip2) -d %{base_arch} babl-%{babl.version}/COPYING
%doc(bzip2) -d %{base_arch} babl-%{babl.version}/NEWS
%doc(bzip2) -d %{base_arch} babl-%{babl.version}/COPYING.LESSER
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/babl-0.0
%{_libdir}/%{_arch64}/babl-0.0/*.so*
%endif
%dir %attr (0755, root, bin) %{_libdir}/babl-0.0
%{_libdir}/babl-0.0/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*/*
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/babl-0.0
%dir %attr (0755, root, bin) %{_includedir}/babl-0.0/babl
%{_includedir}/babl-0.0/babl/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Mar 26 2009  chris.wang@sun.com
- Correct copyright file
* Fri Feb 20 2009  chris.wang@sun.com
- Add manpage
* Tue Dec 16 2008 - chris.wang@sun.com
- Fix SparcV9 file section problem
* Fri Nov 18 2008 - chris.wang@sun.com
- Create
