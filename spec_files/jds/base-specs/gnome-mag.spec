#
# spec file for package gnome-mag
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name:         gnome-mag
License:      LGPL
Group:        System/Libraries
Version:      0.15.5
Release:      201
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME magnifier
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.15/%{name}-%{version}.tar.bz2
#owner:dcarbery date:2007-06-07 type:bug bugzilla:444137,444138
Patch1:       gnome-mag-01-x11-build-error.diff
#owner:dcarbery date:2007-08-28 type:branding
Patch2:       gnome-mag-02-no-xext-dependency.diff
URL:          http://developer.gnome.org/projects/gap/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:	      /sbin/ldconfig

%define gtk2_version 2.2.4
%define libbonobo_version 2.4.0
%define popt_version 1.6.4
%define at_spi_version 1.5.4

# Requirements
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: popt-devel >= %{popt_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      libbonobo >= %{libbonobo_version}
Requires:      at-spi >= %at_spi_version

%description
gnome-mag is a screen magnification service using Bonobo.

%prep
%setup -q
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

aclocal $ACLOCAL_FLAGS -I m4
automake
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}			\
            --sysconfdir=%{_sysconfdir}		\
	    --libdir=%{_libdir}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
            --mandir=%{_mandir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/gnome-mag-1.0/*/*
%{_libdir}/*.so*
%{_libdir}/bonobo/servers/GNOME_Magnifier.server
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gnome-mag/*
%{_datadir}/idl/gnome-mag-1.0/GNOME_Magnifier.idl
%{_datadir}/locale/*/*/*
%{_mandir}/man1/*

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 0.15.5
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 0.15.4.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 0.15.3.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 0.15.2.
* Tue Jul 08 2008 - damien.carbery@sun.com
- Call aclocal/automake to pick up modified intltool.m4.
* Mon Jun 07 2008 - Christian.Kelly@Sun.Com
- Bump to 0.15.1.
* Thu Jan 03 2007 - damien.carbery@sun.com
- Bump to 0.15.0.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 0.14.10.
* Tue Sep 11 2007 - damien.carbery@sun.com
- Bump to 0.14.9.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Add patch, 02-no-xext-dependency, to remove the xext dependency from
  configure.in. This module is not on Solaris and gnome-mag builds without it.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 0.14.8.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 0.14.7. Remove upstream patch, 02-pkg-config.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Add patch 02-pkg-config to fix #467320, reorder two lines in .pc.in file.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 0.14.6.
* Thu Jun 07 2007 - damien.carbery@sun.com
- Add patch 01-x11-build-error to fix #445140.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 0.14.5.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 0.14.4.
* Sun Mar 11 2007 - damien.carbery@sun.com
- Bump to 0.14.3.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 0.14.2. Remove upstream patch, 01-uninstalled.pc.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 0.14.1.
* Sun Dec 17 2006 - damien.carbery@sun.com
- Bump to 0.14.0.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 0.13.1.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 0.13.0.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 0.12.4.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 0.12.2
* Thu May 12 2005 - bill.haneman@sun.com
- Revved to 0.12.1, fixes #6199929.  Removed obsolete g11n patch.
* Fri Feb 04 2005 - bill.haneman@sun.com
- Revved to 0.11.14, fixes bugzilla bug #166282 which should be a P2
  bugster bug.
* Fri Jan 21 2005 - bill.haneman@sun.com
  Corrected dependencies - removed gnome-speech and gail dependencies,
  added at-spi dependency (for LoginHelper API) and popt dependency.
* Wed Jan 19 2005 - bill.haneman@sun.com
  Revved to 0.11.13, fixes for 618662, 6217152, 6205225, 6199929.
* Tue Dec 07 2004 - bill.haneman@sun.com
  Revved to 0.11.11, fixes for bugs 6192805, 6182499, 6182502.
* Fri Nov 19 2004 - damien.carbery@sun.com
- add --bindir=%{_bindir}, --libdir=%{_libdir} and --includedir=%{_includedir}
  to configure opts.
* Fri Nov 05 2004 - bill.haneman@sun.com
- Revved to 0.11.10.  Should improve bugtraq 5099413 further.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add magnifier.1 man page
* Wed Oct 06 2004 - bill.haneman@sun.com
- Removed patch, revved to 0.11.8.  Partial fix for bugtraq 5099413.
* Mon Sep 20 2004 - bill.haneman@sun.com
- Added patch gnome-mag-02-damage-fix.diff for bugtraq 5099413.
* Tue Aug 31 2004 - bill.haneman@sun.com
- Revved to 0.11.7, gives readable SourceDisplay and TargetDisplay
  params, and better debugging support for XDAMAGE.
* Tue Aug 31 2004 - bill.haneman@sun.com
- Revved to 0.11.5, to include LoginHelper support.
* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.
* Tue Aug 17 2004 - bill.haneman@sun.com
- Updated to version 0.11.4, to fix bug #5083109.
* Fri Jul 30 2004 - bill.haneman@sun.com
- Updated to version 0.11.3, which includes a fix for
  the configure path to Damage and XFixes client libs,
  which are in /usr/openwin/sfw/lib for some reason.
* Tue Jul 12 2004 - niall.power@sun.com
- fixed packaging up for rpm4
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-mag-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue May 18 2004 - <laca@sun.com>
- add patch 01 (uninstalled.pc)
* Fri May 14 2004 - <padraig.obriain@sun.com>
- Bump to 0.11.2
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-mag-l10n-po-1.1.tar.bz2
* Thu Apr 22 2004 - <padraig.obriain@sun.com>
- Bump to 0.11.1
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gnome-mag-l10n-po-1.0.tar.bz2 l10n content
* Tue Mar 23 2004 - <padraig.obriain@sun.com>
- Bump to 0.10.10
* Wed Feb 25 2004 - damien.carbery@sun.com
- Created new spec file for gnome-mag
