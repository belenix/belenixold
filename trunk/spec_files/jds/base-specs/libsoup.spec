#
# spec file for package libsoup
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
#
Name:         libsoup
License:      LGPL v2
Group:        System/Libraries/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library for SOAP support in Evolution
Source:       http://ftp.gnome.org/pub/GNOME/sources/libsoup/2.26/libsoup-%{version}.tar.bz2

URL:          http://www.gnome.org

BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/libsoup
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk_doc_version 1.1
%define glib_version 2.4.0
%define libxml_version 2.4.0
%define gnutls_version 1.0.0

Requires:       glib2 >= %{glib_version}
Requires:       libxml2 >= %{libxml_version}
Requires:       gnutls >= %{gnutls_version}

BuildRequires:  glib2-devel >= %{glib_version}
BuildRequires:  libxml2-devel >= %{libxml_version}
BuildRequires:  gnutls-devel >= %{gnutls_version}
BuildRequires:  gtk-doc >= %{gtk_doc_version}

%description
Soup provides an queued asynchronous callback-based mechanism for sending and
servicing SOAP requests, and a WSDL (Web Service Definition Language) to C
compiler which generates client stubs and server skeletons for easily calling
and implementing SOAP methods.

%package devel
Summary:      Development Library for SOAP support in Evolution
Group:        Development/Libraries/GNOME
Autoreqprov:  on
Requires:     %name = %version
BuildRequires: glib2-devel >= %{glib_version}
BuildRequires: libxml2-devel >= %{libxml_version}

%description devel
Soup provides an queued asynchronous callback-based mechanism for sending and
servicing SOAP requests, and a WSDL (Web Service Definition Language) to C
compiler which generates client stubs and server skeletons for easily calling
and implementing SOAP methods.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-gtk-doc

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*

%files devel
%defattr (-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libsoup-2.2/*
%{_datadir}/gtk-doc/*

%changelog
* Tue Apr 14 2009 - jedy.wagn@sun.com
- Bump to 2.26.1
* Thu Apr 09 2009 - ke.wang@sun.com
- Bump to 2.26.0.9
* Tue Mar 17 2009 - ke.wang@sun.com
- Bump to 2.26.0
* Wed Feb 18 2009 - ke.wang@sun.com
- Bump to 2.25.91
* Wed Feb 18 2009 - ke.wang@sun.com
- Move dependency on libproxy to SUNWlibsoup.spec
* Tue Feb 12 2009 - ke.wang@sun.com
- Bump to 2.25.5
- Remove patch libsoup-01-empty-struct.diff
- Add dependency on libproxy
* Fri Jan 09 2009 - ke.wang@sun.com
- Bump to 2.25.4
* Wed Dec 16 2008 - dave.lin@sun.com
- Bump to 2.25.3
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Nov 07 2008 - jeff.cai@sun.com
- Bump to 2.25.1
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Tue Oct 29 2008 - jeff.cai@sun.com
- Bump to 2.24.1.
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 2.24.0.1.
* Tue Sep 23 2008 - simon.zheng@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - simon.zheng@sun.com
- Bump to 2.23.91.
* Tue Aug 05 2008 - jedy.wang@sun.com
- Bump to 2.23.6.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 2.4.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.4.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.3.4.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.3.2. Remove upstream patch 01-stdout
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.3.0.1.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.3.0.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.2.104.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.2.102.
* Mon Oct 08 2007 - damien.carbery@sun.com
- Bump to 2.2.101.
* Tue Feb 28 2007 - simon.zheng@sun.com
- Bump to 2.2.100
* Mon Jan 9 2007 - jeff.cai@sun.com
- Bump to 2.2.99.
* Mon Nov 27 2006 - jeff.cai@sun.com
- Bump to 2.2.98.
* Tue Nov 07 2006 - jeff.cai@sun.com
- Bump to 2.2.97.
* Tue Jul 25 2006 - jeff.cai@sun.com
- Bump to 2.2.96.
* Fri Jul 20 2006 - jeff.cai@sun.com
- Bump to 2.2.95.1.
* Thu Jun 08 2006 - halton.huo@sun.com
- Disable gtk-doc.
* Tue May 30 2006 - halton.huo@sun.com
- Bump to 2.2.93.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.2.92.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Alter "remove *.a/*.la files part" to SUNWevolution-libs.spec
* Sun Mar  5 2006 - damien.carbery@sun.com
- Bump to 2.2.91.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.2.7.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.2.6.1.
* Wed Aug 31 2005 - halton.huo@sun.com
- Bump to 2.2.6.
- Change gnutls_version to 1.0.0, or SSL will be disabled. 
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.2.5.
* Tue Nov 23 2004 - glynn.foster@sun.com
- Bump to 2.2.1
* Thu Jun 17 2004 - niall.power@sun.com
- rpm4´ified
* Tue Jun 08 2004 - glynn.foster@sun.com
- Bump to 2.1.11
* Fri May 21 2004 - glynn.foster@sun.com
- Bump to 2.1.10
* Mon Apr 19 2004 - glynn.foster@sun.com
- Initial spec file for libsoup 2.1.x
