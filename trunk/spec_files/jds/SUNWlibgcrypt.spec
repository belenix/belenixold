#
# spec file for package SUNWlibgcrypt
#
# includes module(s): libgcrypt
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libgcrypt64 = libgcrypt.spec
%endif

%include base.inc
%use libgcrypt = libgcrypt.spec

Name:          SUNWlibgcrypt
Summary:       libgcrypt - cryptographic library
Version:       %{libgcrypt.version}
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibgpg-error
BuildRequires: SUNWlibgpg-error-devel

Source1:    %{name}-manpages-0.1.tar.gz

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SUNWlibgcrypt

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libgcrypt64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libgcrypt.prep -d %name-%version/%base_arch

# Expand manpages tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -


%build
%ifarch amd64 sparcv9
%libgcrypt64.build -d %name-%version/%_arch64
%endif

%libgcrypt.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libgcrypt64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}/%_arch64/hmac256
%endif

%libgcrypt.install -d %name-%version/%base_arch
rm -r $RPM_BUILD_ROOT%{_datadir}/info
rm -r $RPM_BUILD_ROOT%{_sbindir}
rm -rf $RPM_BUILD_ROOT%{_bindir}/hmac256

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/libgcrypt-%{libgcrypt.version} AUTHORS README
%doc(bzip2) -d %{base_arch}/libgcrypt-%{libgcrypt.version} ChangeLog
%doc(bzip2) -d %{base_arch}/libgcrypt-%{libgcrypt.version} COPYING COPYING.LIB
%doc(bzip2) -d %{base_arch}/libgcrypt-%{libgcrypt.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Tue Mar 03 2009 - jeff.cai@sun.com
- Not ship hmac256
* Wed Sep 16 2008 - jeff.cai@sun.com
- Add copyright.
* Thu Jul 31 2008 - jeff.cai@sun.com
- Add man pages for libgcrypt.
* Fri Jun 06 2008 - damien.carbery@sun.com
- Change 'rm -rf' to 'rm -r' so that changes to installed dirs will be noticed
  in build logs.
* Tue Mar 27 2007 - laca@sun.com
- enable 64-bit build
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Apr 06 2006 - glynn.foster@sun.com
- Move -config file to -devel.
* Tue Apr 04 2006 - halton.huo@sun.com
- Alter remove .a/.la files part into linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Remove all *.a/*.la files.
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files
* Wed Sep 07 2005 - damien.carbery@sun.com
- Add Build/Requires SUNWlibgpg-error/-devel.
* Wed Aug 31 2005 - halton.huo@sun.com
- Change SUNW_Category for open solaris
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Fri Sep 10 2004 - shirley.woo@sun.com
- Added Requires: SUNWlibcrypt for devel package
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files should be in a separate devel package
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
