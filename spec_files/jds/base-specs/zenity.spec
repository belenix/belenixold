#
# spec file for package zenity
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: migi
#
Name:         zenity
License:      LGPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Show graphical dialog boxes from scripts
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# date:2008-08-26 type:bug owner:mattman bugster:6741015 bugzilla:549404
Patch1:		  zenity-01-hide-text.diff
# date:2009-01-07 type:bug owner:mattman bugster:6757658 bugzilla:561131
Patch2:		  zenity-02-focus-on-map.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define gtk2_version 2.3.1
%define libgnomecanvas_version 2.4.0
%define GConf_version 2.4.0.1
%define libglade_version 2.3.1
%define popt_version 1.6.4
%define scrollkeeper_version 0.3.12

Requires:	gtk2 >= %{gtk2_version}
Requires:	libgnomecanvas >= %{libgnomecanvas_version}
Requires:	GConf >= %{GConf_version}
Requires:	libglade >= %{libglade_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  libglade-devel >= %{libglade_version}
BuildRequires:  popt-devel >= %{popt_version}
BuildRequires:  scrollkeeper >= %{scrollkeeper_version}

%description
Show graphical dialog boxes from the commandline or through scripts. Zenity is a 
predecessor to dialog.

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

libtoolize --force
intltoolize --copy --force

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS 
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--localstatedir=%{_localstatedir} \
	--disable-scrollkeeper
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/


#Remove some scrollkeeper files before packaging
rm -rf $RPM_BUILD_ROOT/%{_prefix}/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/zenity
%{_datadir}/zenity/*
%{_datadir}/gnome/help
%{_mandir}/man1/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.24.1.
* Wed Jan 07 2009 - matt.keenan@sun.com
- Add patch to fix focus-on-map bug : 6757658 / bugzilla : 561131
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Aug 26 2008 - matt.keenan@sun.com
- Add patch for minor --help-text fix for hide-entry 
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.3.1.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2005 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.3.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.1. Remove upstream 01-commandline.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 29 2006 - glynn.foster@sun.com
- Add simple commandline patch to clean things
  up a little - #353320.
* Mon Aug 21 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 31 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Sun Jul 23 2006 - laca@sun.com
- Bump to 2.15.2
* Mon Jul 10 2006 - brian.cameron@sun.com
- Bump to 2.14.2.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Mon Jan 16 2006 - damien.carbery@sun.com
- Call intltoolize to build correctly.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.3
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri Jul 01 2005 - matt.keenan@sun.com
- Add pkgconfig patch
* Wed Jun 08 2005 - matt.keenan@sun.com
- Fix build. remove scrollkeeper files before packageing
* Tue May 25 2005 - brian.cameron@sun.com
- Fix build.
* Thu May 12 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Thu Mar 31 2005 - damien.carbery@sun.com
- Updated docs tarball (zenity-docs-0.3linux) from maeve.anslow@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- fixed man page file list issue
* Fri Aug 20 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs tarball from breda.mccolgan@sun.com
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to zenity-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %SOURCE1 to install l10n messages
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to zenity-l10n-po-1.1.tar.bz2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to zenity-l10n-po-1.0.tar.bz2
* Tue Mar 23 2004 - glynn.foster@sun.com
- Bump to 2.6.0
* Wed Mar 17 2004 - laca@sun.com
- re-autotoolize to pick up fixed glib-gettext macros needed on Solaris
* Tue Mar 15 2004 - glynn.foster@sun.com
- Remove man page patch since we do this 
  with %files.
* Tue Feb 24 2004 - glynn.foster@sun.com
- Update tarball to 2.5.2
* Wed Dec 17 2003 - glynn.foster@sun.com
- Update tarball to 1.7
* Mon Oct 13 2003 - laca@sun.com
- Update tarball
* Mon Aug 11 2003 - glynn.foster@sun.com
- Update tarball
* Fri Jul 25 2003 - niall.power@sun.com
- Requires scrollkeeper for postinstall. Add a dependency
* Tue Jul 01 2003 - glynn.foster@sun.com
- Initial Sun release
