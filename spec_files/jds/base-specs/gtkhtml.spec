#
# spec file for package gtkhtml
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
Name:         gtkhtml
License:      GPL v2, LGPL v2
Group:        System/Libraries/GNOME
# major_version is generally a 'stable' build number i.e. has an even number.
%define major_version 3.14
Version:      3.26.1.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library for HTML support in Evolution
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.26/%{name}-%{version}.tar.bz2
Source1:      l10n-configure.sh

# date:2009-04-07 bugzilla:578213 bugster:6821920 owner:jefftsai type:bug
Patch1:       gtkhtml-01-iso-codes.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/gtkhtml
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libgnomeprint_version 2.3.0
%define libgnomeprintui_version 2.3.0
%define libgnomeui_version 2.4.0.1
%define libsoup_version 2.2.0

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       libgnomeprint >= %{libgnomeprint_version}
Requires:       libgnomeprintui >= %{libgnomeprintui_version}
Requires:       libsoup >= %{libsoup_version}

BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libgnomeprintui-devel >= %{libgnomeprintui_version}
BuildRequires:  libgnomeprint-devel >= %{libgnomeprint_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}

%description
gtkhtml is a library providing HTML support for Evolution.

%package devel
Summary:      Development Library for HTML support in Evolution
Group:        Development/Libraries/GNOME
Autoreqprov:  on
Requires:     %name = %version
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libgnomeprintui-devel >= %{libgnomeprint_version}
BuildRequires: libgnomeprint-devel >= %{libgnomeprintui_version}
BuildRequires: libsoup-devel >= %{libsoup_version}

%description devel
This package contains the development libraries for gtkhtml, a 
library providing HTML support for Evolution.

%prep
%setup -q
%patch1 -p1

%build
libtoolize --force
intltoolize --copy --force --automake

bash -x %SOURCE1 --enable-copyright

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --with-bonobo-editor \
    --sysconfdir=%{_sysconfdir}

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
%{_libdir}/bonobo/servers/*.server
%{_libdir}/gtkhtml/*.so
%{_datadir}/gtkhtml-%{major_version}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr (-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libgtkhtml-%{major_version}/*

%changelog
* Wed Apr 15 2009 - dave.lin@sun.com
- Bump to 3.26.1.1
* Tue Apr 14 2009 - jedy.wang@sun.com
- Bump t 3.26.1.
* Tue Apr 07 2009 - jeff.cai@sun.com
- Add patch -01-iso-codes to fix bugzilla #578213
* Tue Mar 17 2009 - jeff.cai@sun.com
- Bump to 3.26.0
* Tue Mar 03 2009 - jeff.cai@sun.com
- Bump to 3.25.92
* Tue Feb 17 2009 - jeff.cai@sun.com
- Bump to 3.25.91
* Wed Feb 04 2009 - jeff.cai@sun.com
- Bump to 3.25.90
* Wed Jan 20 2009 - jeff.cai@sun.com
- Bump to 3.25.5
- Remove -01-g11n-i18n-ui.diff, 567130 upstreamed.
* Mon Jan 12 2009 - takao.fujiwara@sun.com
- Add patch g11n-i18n-ui.diff to fix message i18n.
* Wed Jan 07 2009 - jeff.cai@sun.com
- Bump to 3.25.4
* Tue Dec 16 2008 - dave.lin@sun.com
- Bump to 3.25.3
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 3.25.2
* Wed Nov 04 2008 - jeff.cai@sun.com
- Bump to 3.25.1
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Tue Oct 29 2008 - jeff.cai@sun.com
- Bump to 3.24.1
- Remove upstream patch 01-g11n-textdomain
* Fri Oct 03 2008 - takao.fujiwara@sun.com
- Add gtkhtml-01-g11n-textdomain.diff to enable bindtextdomain.
* Tue Sep 22 2008 - jeff.cai@sun.com
- Bump to 3.24.0
* Tue Sep 09 2008 - jeff.cai@sun.com
- Bump to 3.23.92
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 3.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 3.23.90
* Wed Aug 04 2008 - jeff.cai@sun.com
- Bump to 3.23.6.

* Wed Jul 23 2008 - jeff.cai@sun.com
- Bump to 3.23.5.
- Removed upstream patch -01-spell-checker
- Removed upstream patch -02-gtk-type

* Wed Jun 18 2008 - jeff.cai@sun.com
- Add patch -01-spell-checker, fix #538703.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 3.23.4.

* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 3.23.3.

* Thu May 29 2008 - damien.carbery@sun.com
- Add --with-bonobo-editor to build the html-editor component.

* Wed May 28 2008 - jeff.cai@sun.com
- Bump to 3.23.2. Remove upstream patch, 01-g11n-backward-searching.

* Tue May 27 2008 - jeff.cai@sun.com
- Bump to 3.18.2.

* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 3.18.1.

* Sun Mar 23 2008 - takao.fujiwara@sun.com
- Add gtkhtml-01-g11n-backward-searching-head.diff not to crash in the
  backward searching with multibyte chars. Fixes 6571095

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 3.18.0.

* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 3.17.92.

* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 3.17.91.

* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 3.17.90.1.

* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 3.17.90.

* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 3.17.5.

* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 3.17.4.

* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 3.17.3.

* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 3.17.2.

* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 3.17.1.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 3.16.1.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 3.16.0.

* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 3.15.92.

* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 3.15.91.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 3.15.90.

* Tue Aug 07 2007 - jeff.cai@sun.com
- Remove patch -01-search.diff

* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 3.15.6.1.

* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 3.15.6.

* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 3.15.5.

* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 3.15.4.

* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 3.15.2.

* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 3.15.2.

* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 3.15.1. Remove upstream patch, 01-backward-finding.

* Mon Apr 30 2007 - simon.zheng@sun.com
- Update the comment on gtkhtml-01-backward-finding.diff.

* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 3.14.1.

* Wed Apr 11 2007 - simon.zheng@sun.com
- To fix the replacement issue of bug #6518702, 
  rework the patch gtkhtml-01-backward-finding.diff 

* Tue Mar 13 2007 - simon.zheng@sun.com
- Bump major_version to 3.14.

* Tue Mar 13 2007 - simon.zheng@sun.com
- Bump to 3.14.0.

* Tue Feb 28 2007 - simon.zheng@sun.com
- Bump to 3.13.92.

* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 3.13.91.

* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 3.13.6.

* Tue Jan 09 2007 - jeff.cai@sun.com
- Bump to 3.13.5.

* Tue Dec 19 2006 - jeff.cai@sun.com
- Bump to 3.13.4.

* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 3.13.3.
* Tue Nov 28 2006 - jeff.cai@sun.com
- Bump to 3.13.2.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 3.12.2.
* Mon Nov 13 2006 - simon.zheng@sun.com
- Add a patch for bugster 6448891.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 3.12.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 3.12.0.
* Tue Aug 22 2006 - jeff.cai@sun.com
- Bump to 3.11.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 3.11.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 3.11.90.1.
* Fri Jul 20 2006 - jeff.cai@sun.com
- Bump to 3.11.4.
* Tue May 30 2006 - halton.huo@sun.com
- Bump to 3.10.2.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 3.10.1.
* Tue Apr 04 2006 - halton.huo@sun.com
- Remove .a/.la files in linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Alter "remove *.a/*.la files part" to SUNWevolution-libs.spec
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 3.10.0.
* Tue Feb 28 2006 - halton.huo@sun.com
- Bump to 3.9.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 3.9.91.
* Fri Feb  3 2006 - damien.carbery@sun.com
- Bump to 3.9.90.1.
* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 3.9.90.
* Thu Jan 19 2006 - halton.huo@sun.com
- Bump to 3.9.5.
* Wed Jan 04 2006 - halton.huo@sun.com
- Bump to 3.9.4.
* Wed Dec 21 2005 - halton.huo@sun.com
- Correct Source filed.
* Tue Dec 19 2005 - damien.carbery@sun.com
- Bump to 3.9.3.
* Thu Dec 01 2005 - damien.carbery@sun.com
- Call intltoolize, needed to process intltool-*.in.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 3.8.2.
* Mon Oct 10 2005 - halton.huo@sun.com
- Bump to 3.8.1.
* Wed Sep  7 2005 - halton.huo@sun.com
- Bump to 3.8.0.
* Wed Aug 31 2005 - halton.huo@sun.com
- Remove Patch1 since it is already there.
* Wed Aug 31 2005 - glynn.foster@sun.com
- Bump 3.7.7.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump 3.7.6.
* Tue Jul 12 2005 - damien.carbery@sun.com
- Add patch to build on Solaris (remove 'return' from void function).
  Bugzilla #309785. Remove when tarball bumped.
* Tue May 17 2005 - glynn.foster@sun.com
- Bump to 3.6.2
* Tue Nov 23 2004 - glynn.foster@sun.com
- Bump to 3.2.3
* Thu Jun 17 2004 - niall.power@sun.com
- rpm4'ified
* Tue Jun 08 2004 - glynn.foster@sun.com
- Bump to 3.1.16
* Fri May 21 2004 - glynn.foster@sun.com
- Bump to 3.1.14
* Tue Apr 20 2004 - glynn.foster@sun.com
- Bump to 3.1.12
* Mon Apr 19 2004 - glynn.foster@sun.com
- Initial spec file for gtkhtml 3.1.x
