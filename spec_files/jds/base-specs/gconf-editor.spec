#
# spec file for package gconf-editor
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen
#
Name:         gconf-editor
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Editor/admin tool for GConf
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# date:2006-05-05 owner:gman type:branding
Patch1:       gconf-editor-01-menu-entry.diff
# date:2009-03-25 owner:stephen type:bug bugzilla:7402
Patch2:       gconf-editor-02-no-polkit.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define GConf_version 2.4.0.1

BuildRequires: GConf-devel >= %{GConf_version}
Requires: GConf >= %{GConf_version}

%description
gconf-editor allows you to browse and modify GConf configuration
sources.

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

aclocal $ACLOCAL_FLAGS
libtoolize --force
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
	    --sysconfdir=%{_sysconfdir} \
	    --datadir=%{_datadir} \
	    --disable-scrollkeeper \
	    --mandir=%{_mandir}
make -j $CPUS

%install

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/


rm -rf $RPM_BUILD_ROOT/usr/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/gconf/schemas
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/pixmaps
%{_datadir}/icons
%{_datadir}/applications
%{_mandir}/man1/*
%{_datadir}/gnome
%{_datadir}/omf/gconf-editor/*.omf

%changelog
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.24.1.
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.1.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - patrick.ale@gmail.com
- Correct download URL
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91, rework gconf-editor-01, remove /usr/share/pixmap and add
  /usr/share/gconf-editor to pkg.
* Wed Mar 12 2008 - damien.carbery@sun.com
- Remove 'mkdir m4' as the dir exists in 2.22.0 tarball.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Fri Feb 22 2008 - damien.carbery@sun.com
- Add --disable-scrollkeeper to configure because scrollkeeper-update breaks
  build.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Add 'mkdir m4' before intltoolize call so that intltool.m4 can be copied.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 12 2007 - damien.carbery@sun.com
- Remove 'mkdir m4' from %build as the directory is in the source tarball.
* Tue Sep 11 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Move aclocal call and mkdir m4 as required by intltoolize call.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.0.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Aug 14 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Fri May 05 2006 - glynn.foster@sun.com
- Remove gconf-editor from the menus.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90. Add intltoolize call.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.12.1
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Tue Aug 30 2005 - glynn.foster@sun.com
- Bump to 2.11.92
* Fri Jul 01 2005 - matt.keenan@sun.com
- Add pkgconfig patch
* Thu May 19 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Thu Jan 27 2005 - damien.carbery@sun.com
- Linux docs tarball required an updated patch which is incompatible with
  Solaris docs tarball so patch 04 added for Solaris.
* Wed Jan 26 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from eugene.oconnor@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n online help
* Thu Aug 19 2004 - glynn.foster@sun.com
- Bump to 2.6.2
* Wed Aug 18 2004 - damien.carbery@sun.com
- Integrated new docs tarball from eugene.oconnor@sun.com
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gconf-editor-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - balamurali.viswanathan@wipro.com
- Add a Help->Contents menu item. Fixes bug #5038096
* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Jun 22 2004 - conor.healy@sun.com
- Added LC_MESSAGES content to %files section
* Thu Jun 17 2004 - matt.keenan@sun.com
- Add docs tarball
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gconf-editor-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gconf-editor-l10n-po-1.0.tar.bz2
* Mon Feb 23 2004 - <stephen.browne@sun.com>
- uprevd to 2.5.4
* Tue Feb 17 2004 - <niall.power@sun.com>
- use ACLOCAL_FLAGS env during build
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.1
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the menu entry patch for adding Sun
  Supported since we're removing the extras menu
* Mon Oct 20 2003 - <stephen.browne@sun.com>
- updated to 2.4.0
* Mon Aug 11 2003 -<stephen.browne@sun.com>
- new version, reset release, remove glib2 include patch
* Fri Aug 01 2003 - <glynn.foster@sun.com>
- add some menu categorization
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Thu May 08 2003 - ghee.teo@Sun.COM
- Created new spec file for gconf-editor

