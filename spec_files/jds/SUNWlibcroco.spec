#
# spec file for package SUNWlibcroco
#
# includes module(s): libcroco
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libcroco64 = libcroco.spec
%endif

%include base.inc
%use libcroco = libcroco.spec

Name:                    SUNWlibcroco
Summary:                 Cascading Style Sheet (CSS) parsing and manipulation toolkit
Source1:                 %{name}-manpages-0.1.tar.gz
Version:                 %{libcroco.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlxml
BuildRequires: SUNWgnome-base-libs

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-base-libs-devel
Requires: SUNWlxml-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libcroco.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%libcroco.prep -d %name-%version/%base_arch

cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
%ifarch amd64 sparcv9
%libcroco64.build -d %name-%version/%_arch64
%endif

%libcroco.build -d %name-%version/%base_arch

%install
%ifarch amd64 sparcv9
%libcroco64.install -d %name-%version/%_arch64
rm -r $RPM_BUILD_ROOT%{_bindir}/%_arch64
%endif

%libcroco.install -d %name-%version/%base_arch

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/csslint*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%doc -d %{base_arch}/libcroco-%{libcroco.version} AUTHORS README
%doc(bzip2) -d %{base_arch}/libcroco-%{libcroco.version} COPYING COPYING.LIB
%doc(bzip2) -d %{base_arch}/libcroco-%{libcroco.version} NEWS
%doc(bzip2) -d %{base_arch}/libcroco-%{libcroco.version} ChangeLog
%doc(bzip2) -d %{base_arch}/libcroco-%{libcroco.version} csslint/ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/croco-*-config
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Tue Mar 24 2009 - jeff.cai@sun.com
- Since /usr/lib/amd64/pkgconfig/libcroco-0.6.pc (SUNWlibcroco-devel) requires
  /usr/lib/amd64/pkgconfig/glib-2.0.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
- Since /usr/lib/amd64/pkgconfig/libcroco-0.6.pc (SUNWlibcroco-devel) requires
  /usr/lib/amd64/pkgconfig/libxml-2.0.pc which is found in
  SUNWlxml-devel, add the dependency
* Thu Feb 26 2009 - brian.cameron@sun.com
- Add manpages.
* Sun Sep 14 2008 - brian.cameron@sun.com
- Add new copyright files.
* Fri Aug 22 2008 - dave.lin@sun.com
- Fixed /usr/lib/amd64/pkgconfig attribute issue.
* Thu Aug 21 2008 - laca@sun.com
- add 64-bit build, needed for the 64-bit librsvg
* Wed May 07 2008 - damien.carbery@sun.com
- Remove PERL5LIB setting as it is not necessary.
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - damien.carbery@sun.com
- Change build dependency on SUNWgnome-base-libs-share. That pkg is obsolete
  with files now in the base package.
* Thu Apr 06 2006 - glynn.foster@sun.com
- Move the config binary into the -devel package.
* Fri Feb 24 2006 - shirley.woo@sun.com
- Update Summary.
* Fri Feb 24 2006 - damien.carbery@sun.com
- Update Summary.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Now use libcroco version number.
* Wed Jul 27 2005 - brian.cameron@sun.com
- Created.
