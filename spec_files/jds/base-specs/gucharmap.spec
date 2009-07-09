#
# spec file for package gucharmap
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:         gucharmap
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Unicode Character Map
Source:       http://ftp.gnome.org/pub/GNOME/sources/gucharmap/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
# date:2006-06-06 owner:gman type:branding
Patch1:       gucharmap-01-menu-entry.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define glib2_version 2.4.0
%define pango_version 1.4.0
%define gtk2_version 2.4.0
%define popt_version 1.7
%define libgnomeui_version 2.6.0
%define scrollkeeper_version 0.3.14

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  pango-devel >= %{pango_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  popt-devel >= %{popt_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
Requires:       libgnomeui >= %{libgnomeui_version}

%description
This package contains a unicode character map for the GNOME Desktop.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1

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
aclocal $ACLOCAL_FLAGS -I m4
automake --add-missing
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=/var/lib \
	--disable-scrollkeeper
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/


#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/applications
%{_datadir}/icons
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_mandir}/man1/*
%{_includedir}/gucharmap/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/omf/*
%{_datadir}/gnome/help/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Feb 20 2009 - brian.cameron@sun.com
- Remove patch gucharmap-02-gthread.diff as it is no longer needed.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.24.3.  Add patch gucharmap-02-gthread.diff.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Mon Aug 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4. Call aclocal/automake to get patched intltool.m4.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Call aclocal to get patched intltool.m4.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 1.10.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 1.10.0.
* Wed Feb 28 2007 - halton.huo@sun.com
- Remove patch 02-gnome-doc-utils-ver since g-d-u is upgrade to 0.9.x.
* Fri Feb 16 2007 - damien.carbery@sun.com
- Add patch, 02-gnome-doc-utils-ver, to allow building with gnome-doc-utils
  0.8.0. gnome-doc-utils 0.9.0 doesn't build on Solaris - waiting for docbook
  updates.
* Thu Feb 15 2007 - damien.carbery@sun.com
- Bump to 1.9.0.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 1.8.0.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 1.7.0.
* Fri Jun 01 2006 - glynn.foster@sun.com
- Add menu entry for gucharmap.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.6.0.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 1.5.3.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 1.5.2.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 1.5.1
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 1.5.0.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Sep 27 2005 - glynn.foster@sun.com
- Bump to 1.4.4
* Wed May 18 2005 - glynn.foster@sun.com
- Bump to 1.4.3
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and patch
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents with patch
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated 0.3 docs tarball from breda.mccolgan@sun.com
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gucharmap-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - damien.carbery@sun.com
- Integrated 0.2 docs tarball from breda.mccolgan@sun.com
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gucharmap-l10n-po-1.1.tar.bz2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 15 2004 - glynn.foster@sun.com
- Bump to 1.4.1
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gucharmap-l10n-po-1.0.tar.bz2
* Tue Mar 16 2004 - glynn.foster@sun.com
- Bump to 1.3.2
* Tue Mar 16 2004 - glynn.foster@sun.com
- Remove online help and .desktop patches since
  they're upstream.
* Mon Feb 23 2004 - matt.keenan@sun.com
- Bump to 1.3.0
- Re-apply patch 01-menu-name-description.diff
- Remove 02-potfiles.diff
- Port patches :
	04-add_help.diff
	05-help_make.diff
	06-l10n-online-help.diff
   From QS and into one patch
	02-add-l10n-help.diff
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 1.2.0
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported keyword since we're
  removing Extras menu.
* Fri Oct 13 2003 - laca@sun.com
- Update to 1.0.0
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Fri Aug 08 2003 - glynn.foster@sun.com
- Add and remove some mnemonics
* Fri Jul 25 2003 - niall.power@sun.com
- Add libgnomeui to Requires
* Thu Jul 10 2003 - glynn.foster@sun.com
- Add a patch to add a menu description and 
  remove the 'Unicode' part of the menu name.
* Tue Jul 01 2003 - glynn.foster@sun.com
- Initial Sun release

