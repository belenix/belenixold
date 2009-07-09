#
# spec file for package libwnck
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:         libwnck
License:      GPL
Group:        System/Libraries/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Window Navigator Construction Kit Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libwnck/2.26/libwnck-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:niall date:2006-10-11 type:feature
Patch1:       libwnck-01-trusted-extensions.diff
Patch2:       libwnck-02-gdk-include.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.2.4
%define startup_notification_version 0.5

Requires: gtk2 >= %{gtk2_version}
Requires: startup-notification >= %{startup_notification_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:  startup-notification-devel >= %{startup_notification_version}

%description
The Window Navigator Construction Kit is a library which can be used
to control windows on your desktop, including API for writing 
Task Lists, Workspace Switchers and Window Lists.

%package devel
Summary:      Window Navigator Construction Kit Development Library
Group:        Development/Libraries/GNOME
Autoreqprov:  on
Requires: %name = %{version}
Requires: gtk2-devel >= %{gtk2_version}

%description devel
The Window Navigator Construction Kit is a library which can be used
to control windows on your desktop, including API for writing 
Task Lists, Workspace Switchers and Window Lists.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1

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
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

gtkdocize
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"				\
./configure --prefix=%{_prefix}			\
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_libdir}/libwnck*.so.*
%{_datadir}/locale/*/*/*

%files devel
%{_libdir}/libwnck*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Add patch 02-gtkdoc-rebase.diff to fix GTKDOC_REBASE issue.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.5.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Wed Aug 20 2008 - brian.cameron@sun.com
- Remove patch libwnck-02-no-x11-dependency.diff since it is no longer needed
  now that the x11.pc file is in our builds.
* Thu Aug 07 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Fri May 16 2008 - stephen.browne@sun.com
- remove conditional build of tx patch
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.  Remove upstream patch, 03-fixcrash.
* Tue Mar 11 2008 - brian.cameron@sun.com
- Add patch to fix crashing bug 517750 (bugzilla)/6658883 (bugster)
* Mon Mar 10 2008 - brian.cameron@sun.com
- Bump to 2.22.0
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Wed Nov 14 2007 - damien.carbery@sun.com
- Bump to 2.21.2.1.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Remove upstream patch, 02-group-windows.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Remove upstream patch, 03-x11-keysym.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Thu Jun 21 2007 - damien.carbery@sun.com
- Add upstream patch, 03-x11-keysym, to fix build problem of missing header.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4. Disable TX patch, waiting for rework. 
* Thu Jun 07 2007 - damien.carbery@sun.com
- Bump to 2.19.3.1.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Fri Nov 10 2006 - niall.power@sun.com
- Re-enable ported trusted-extensions patch.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed Jun 22 2006 - niall.power@sun.com
- libwnck-01-trusted-extensions.diff: add
  support for Solaris Trusted Extensions.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Wed Jan 18 2006 - brian.cameron@sun.com
- Added calls to glib-gettextize and intltoolize to avoid going into an
  infinite loop when building.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Thu Dec 22 2005 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri Jun 24 2005 - balamurali.viswanathan@wipro.com
- Add patch pkgconfig.diff that adds the required libs explictly
* Fri May 10 2005 - glynn.foster@sun.com
- Bump to 2.10
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libwnck-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libwnck-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libwnck-l10n-po-1.0.tar.bz2
* Tue Mar 23 2004 - glynn.foster@sun.com
- Bump to 2.6.0 and remove the uninstalled, 
  potfiles and null atom patches - upstream.
* Sun Mar 21 2004 - laca@sun.com
- add patch 03 instead of adding patch 02 twice.
* Fri Mar 19 2004 - <brian.cameron@sun.com>
- add patch 2 fixing null atom names from causing coredummp on Solaris.
* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- libwnck-02-g11n-potfiles.diff
* Fri Feb 20 2004 - matt.keenan@sun.com
- Update Distro, l10n tarball
* Tue Feb 17 2004 - laca@sun.com
- Add uninstalled.pc file needed for the Solaris builds
* Fri Oct 10 2003 - <laca@sun.com>
- update to 2.4.0.1
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Fri May 30 2003 - markmc@sun.com
- Backport fitt's law patch for gnome-panel 2.3.x.
* Tue May 13 2003 - matt.keenan@sun.com
- initial Sun release.
