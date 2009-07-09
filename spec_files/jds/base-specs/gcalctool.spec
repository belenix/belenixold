#
# spec file for package gcalctool
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include l10n.inc
Name:         gcalctool
License:      GPL
Group:        System/GUI/GNOME
Version:      5.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Calculator
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/5.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define glib2_version 2.6.0
%define pango_version 1.2.5
%define gtk2_version 2.6.0
%define GConf_version 1.1.9
%define libgnome_version 2.4.0
%define scrollkeeper_version 0.3.12

Requires:       libgnome >= %{libgnome_version}
Requires:  	glib2 >= %{glib2_version}
Requires:  	gtk2 >= %{gtk2_version}
Prereq:         GConf >= %{GConf_version}
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  pango-devel >= %{pango_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  libgnome-devel >= %{libgnome_version}
BuildRequires:	scrollkeeper >= %{scrollkeeper_version}

%description
This package contains a calculator for the GNOME Desktop. This calculator
has 3 different modes - Basic, Scientific and Financial.


%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif

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

intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I ./m4
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --mandir=%{_mandir} \
	--localstatedir=/var/lib \
        --disable-scrollkeeper

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm -rf $RPM_BUILD_ROOT/var/lib/scrollkeeper
#rmdir $RPM_BUILD_ROOT/var/lib
#rmdir $RPM_BUILD_ROOT/var

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS=" gcalctool.schemas "
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/gcalctool
%{_datadir}/gnome/help
%{_sysconfdir}/gconf/schemas
%{_datadir}/applications
%{_mandir}/man1/

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 5.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 5.25.92
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 5.25.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 5.25.90.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 5.25.2
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 5.24.0
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 5.23.92.
* Tue Sep 01 2008 - christian.kelly@sun.com
- Bump to 5.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 5.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 5.23.6.

* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 5.23.5.

* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 5.23.4.

* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 5.23.3.

* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 5.23.2.

* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 5.22.2.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 5.22.0.

* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 5.21.92.

* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 5.21.91.

* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 5.21.90.

* Mon Jan 14 2008 - damien.carbery@sun.com
- Bump to 5.21.5.

* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 5.21.4.

* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 5.21.3.

* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 5.21.2.

* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 5.21.1.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 5.20.2.

* Tue Oct  2 2007 - damien.carbery@sun.com
- Bump to 5.20.1.

* Fri Sep 21 2007 - brian.cameron@sun.com
- Call intltoolize and other autotools.  Otherwise the desktop
  file doesn't get build and we don't see the calculator in the
  menus.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 5.20.0.

* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 5.19.92.

* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 5.19.91.

* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of %{_prefix}/var and %{_prefix}/var/lib dirs as they are
  no longer created.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 5.19.90.

* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 5.19.6. Remove upstream patch, 01-gtk-tooltips.

* Wed Jul 25 2007 - damien.carbery@sun.com
- Add upstream patch, 01-gtk-tooltips, to build against latest gtk+.

* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 5.19.5. Remove upstream patch, 01-menu-entry.

* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 5.19.4.

* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 5.19.3.

* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 5.19.2.

* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 5.19.1.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 5.9.14.

* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 5.9.13.

* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 5.9.12.

* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 5.9.11.

* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 5.9.10.

* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 5.9.9.

* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 5.9.8. Remove upstream patch, 02-result-area.

* Mon Nov 13 2006 - patrick.wade@sun.com
- Add patch 02-result-area to fix bugster 6480076

* Fri Nov 03 2006 - damien.carbery@sun.com
- Bump to 5.8.25. Remove upstream patch, 02-arabic-decimal-point.

* Tue Oct 03 2006 - matt.keenan@sun.com
- Bugster #6473019 / bugzilla #359291
- Fix crash with arabic locale

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 5.8.24.

* Fri Aug 18 2006 - damien.carbery@sun.com
- Bump to 5.8.23.

* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 5.8.20.

* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 5.8.19.

* Web Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 5.8.17.

* Fri Jun 01 2006 - glynn.foster@sun.com
- Add menu entry patch.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 5.7.32.

* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 5.7.30.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 5.7.29.

* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 5.7.28.

* Mon Jan 23 2006 - damien.carbery@sun.com
- Bump to 5.7.27.

* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 5.7.26.

* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 5.7.23.

* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 5.7.18.

* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff

* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 5.6.31.

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 5.6.26.

* Fri Jul 01 2005 - matt.keenan@sun.com
- -02-pkgconfig patch for solaris build

* Thu May 19 2005 - laszlo.kovacs@sun.com
- ported to 5.5.42

* Wed May 18 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help patch to add pt_BR

* Tue Jan 25 2005 - glynn.foster@sun.com
- Add patch from Rich to fix #162998.

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux

* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and patch

* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR

* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents

* Thu Aug 05 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gcalctool-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
                                                                                
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Mon May 31 2004 - padraig.obriain@sun.com
- Add patch gcalctool-01-update-display.diff to fix bugzilla bug #134376

* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gcalctool-l10n-po-1.1.tar.bz2

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris

* Thu Apr 15 2004 - glynn.foster@sun.com
- Bump to 4.3.51

* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gcalctool-l10n-po-1.0.tar.bz2

* Tue Mar 16 2004 - glynn.foster@sun.com
- Remove the man page and localized doc patches
  since they're upstream and we'll pick them up 
  with the next release. Bump to 4.3.50.

* Mon Mar 01 2004 - laca@sun.com
- fix aclocal options
- s$/usr/share/man$%{_mandir}$
- s$/usr/share%{_datadir}$

* Thu Feb 23 2004 - laca@sun.com
- fix non-portable tar commands

* Mon Feb 23 2004 - matt.keenan@sun.com
- Bump to 4.3.46, re-order patches, l10n update

* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 4.3.29

* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported keyword since we're
  moving away from extras menu.

- Remove the Sun Supported keyword since we're
  moving away from extras menu.

- Remove the Sun Supported keyword since we're
  moving away from extras menu.

- Remove the Sun Supported keyword since we're
  moving away from extras menu.

* Fri Oct 10 2003 - laca@sun.com
- Update to 3.4.4

* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu entry supported category.

* Wed Jul 30 2003 - glynn.foster@sun.com
- New release. Bump version, reset release.

* Fri Jul 25 2003 - niall.power@sun.com
- Uses scrollkeeper for postinstall. Add a dependency

* Tue Jul 01 2003 - glynn.foster@sun.com
- Initial Sun release
