#
# spec file for package libgnomecanvas
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         libgnomecanvas
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Canvas Library for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgnomecanvas/2.26/libgnomecanvas-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.4.0
%define libart_lgpl_version 2.3.16
%define libglade_version 2.3.6
%define gnome_common_version 2.4.0

Requires: gtk2 >= %{gtk2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libart_lgpl-devel >= %{libart_lgpl_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: gnome-common >= %{gnome_common_version}

%description
libgnomecanvas is an engine for structured graphics that offers a rich
imaging model, high performance rendering, and a powerful, high-level
API. It offers a choice between two rendering back-ends, one based on
Xlib for extremely fast display, and another based on Libart, a 
sophisticated, antialiased, alpha-compositing engine. Applications have
a choice between the Xlib imaging model or a superset of the PostScript
imaging model, depending on the level of graphic sophistication required.


%package devel
Summary:      Canvas Development Library for GNOME
Group:        Development/Libraries/GNOME
Requires:     %name = %{version}
Requires:     gtk2-devel >= %{gtk2_version}
Requires:     libart_lgpl-devel >= %{libart_lgpl_version}
Requires:     libglade-devel >= %{libglade_version}

%description devel
libgnomecanvas is an engine for structured graphics that offers a rich
imaging model, high performance rendering, and a powerful, high-level
API. It offers a choice between two rendering back-ends, one based on
Xlib for extremely fast display, and another based on Libart, a 
sophisticated, antialiased, alpha-compositing engine. Applications have
a choice between the Xlib imaging model or a superset of the PostScript
imaging model, depending on the level of graphic sophistication required.

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
gtkdocize
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir} \
	    %{gtk_doc_option}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
                                                                                                                                                             
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/libgnomecanvas*.so.*
%{_libdir}/libglade/2.0/libcanvas*so*
%{_datadir}/locale/*/LC_MESSAGES/libgnomecanvas-2.0.mo

%files devel
%{_libdir}/libgnomecanvas*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/libgnomecanvas
%{_mandir}/man3/*

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Call gtkdocize to fix GTKDOC_REBASE issue.
* Fri Feb 13 2009 - dave.lin@sun.com
- Bump to 2.25.90
* Mon Oct 22 2007 - damien.carbery@sun.com
- Remove patch, 01-gailutil-pc, as it is no longer needed for building.
  Probably because gail is part of gtk+ now.
* Mon Oct 22 2007 - damien.carbery@sun.com
- Bump to 2.20.1.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Fri Jul 13 2007 - damien.carbery@sun.com
- Add patch 01-gailutil-pc to fix #456513. This adds libgailutil to libs line
  in the pc file so that dependant modules will link with libgailutil, which
  is now required by libgnomecanvas.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 2.19.0.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.3.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.1.
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 2.10.2
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomecanvas-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomecanvas-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgnomecanvas-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 2.6.0, removing the uninstalled pc
  patch.
* Fri Feb 20 2004 - <matt.keenan@sun.com>
- Bump to 2.5.4, l10n to 0.8
- Ported potfiles patch
* Fri Feb 06 2004 - <niall.power@sun.com>
- Add patch to create an -uninstelled.pc pkgconfig
  file
- autotoolize the build stage
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Bump to 2.5.1, and port manpages/patches.
* Mon Oct 06 2003 - <ghee.teo@sun.com>
- Updated to 2.4.0 for Quicksilver
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Tue May 13 2003 - Stephen.Browne@sun.com
- initial Sun release
