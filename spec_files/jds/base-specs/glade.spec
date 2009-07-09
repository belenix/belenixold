#
# spec file for package glade
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: hawklu
#
%include l10n.inc
Name:         glade
License:      GPL
Group:        System/GUI/GNOME
Version:      3.5.7
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GLADE User Interface Builder for GNOME
Source:       http://download.gnome.org/sources/%{name}3/3.5/%{name}3-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/doc
Autoreqprov:  on

%define scrollkeeper_version 0.3.14
%define libgnomeui_version 2.9.0
%define libxml2_version 2.4.1

BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libxml2 >= %{libxml2_version}
Requires: libgnomeui >= %{libgnomeui_version}

%description
Glade is a User Interface Builder for GTK+ and GNOME. This package contains GLADE  for the GTK + 2.0 and GNOME 2.0 Platform.

%package devel
Summary:      %{name} - Developer Libraries
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}

%prep
%setup -q -n %{name}3-%{version}
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

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I ./m4
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" 	\
./configure  			\
	--prefix=%{_prefix} 	\
	--bindir=%{_bindir}	\
	--libdir=%{_libdir}	\
	--includedir=%{_includedir} \
	--sysconfdir=%{_sysconfdir} \
	--disable-scrollkeeper	\
	%{gtk_doc_option}

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/applications
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/icons
%{_datadir}/omf/*
%{_datadir}/gnome/*
%{_datadir}/glade*
%{_mandir}/man1/*

%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Mar 03 2008 - halton.huo@sun.com
- Bump to 3.5.7.
* Tue May 06 2008 - damien.carbery@sun.com
- Bump to 3.4.5.
* Fri Apr 18 2008 - damien.carbery@sun.com
- Bump to 3.4.4.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 3.4.3.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 3.4.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 3.4.0.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Thu Aug 23 2007 - damien.carbery@sun.com
- Bump to 3.3.4.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 3.3.3.
* Tue Jul 24 2007 - halton.huo@sun.com
- Bump to 3.3.2.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 3.3.1.
* Wed Jun 06 2007 - halton.huo@sun.com
- Bump to 3.3.0.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 3.2.2.
* Thu May 03 2007 - halton.huo@sun.com
- Bump to 3.2.1.
- Use %gtk_doc_option in configure
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 3.2.0. Remove upstream patch, 01-Wall-remove.
* Tue Mar 06 2007 - halton.huo@sun.com
- Add --disable-scrollkeeper when run ./configure
- Update %files.
* Wed Feb 28 2007 - halton.huo@sun.com
- Bump to 3.1.5.
- Add patch 01-Wall-remove.diff to fix bugzilla #412993.
- Remove obsoleted patch 01-menu-entry.diff.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add Add l10n tarball.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.12.1.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Sep 27 2005 - matt.keenan@sun.com
- Bump to 2.10.1.
* Tue Jun 14 2005 - matt.keenan@sun.com
- Bump to 2.10.0.
* Fri Mar 11 2005 - matt.keenan@sun.com
- 6227253 : Remove glade-faq*.omf
* Fri Feb 25 2005 - kazuhiko.maekawa@sun.com
- Added dummy l10n help files to follow base bug updates
* Mon Feb 14 2005 - damien.carbery@sun.com
- Integrate docs tarball (glade-docs-0.1) from irene.ryan@sun.com.
* Fri Nov 12 2004 - laca@sun.com
- Added --libdir and --bindir to configure opts so they can be redirected
  on Solaris
* Tue Sep 14 2004 - yuriy.kuznetsov@sun.com
- Added glade-03-g11n-potfiles.diff
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to glade-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jun  7 2004 - takao.fujiwara@sun.com
- Add 'touch po/*.po' to use sun messages files
- Add glade-02-g11n-linguas.diff to add zh_TW, zh_HK.
* Fri May 21 2004 - glynn.foster@sun.com
- Add back menu entry, and rename it to Interface Editor
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to glade-l10n-po-1.1.tar.bz2
* Tue Apr 20 2004 - niall.power@sun.com
- bump to 2.6.0 release
- add main menu entry .desktop file
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding glade-l10n-po-1.0.tar.bz2 l10n content
* Fri Mar 26 2004 - brian.cameron@sun.com
- added $ACLOCAL_FLAGS to aclocal call, needed for Solaris.
* Tue Mar 16 2004 - glynn.foster@sun.com
- Remove the menu entry patch as %files does
  this for free.
* Thu Nov 14 2003 - glynn.foster@sun.com
- Bump to 2.0.1 tarball
* Thu Nov 14 2003 - glynn.foster@sun.com
- Remove the menu entry as per spec.
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported part of the menu
  patch since we're removing the Extras menu.
* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu categorization
* Tue Jul 22 2003 - michael.twomey@sun.com
- Updated POTFILES.in
* Wed Jul 09 2003 - ghee.teo@sun.com
- Initial Sun Release
