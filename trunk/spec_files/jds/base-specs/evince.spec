#
# spec file for package evince
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:         evince
License:      GPL
Group:        System/GUI/GNOME
# poppler should be bumped at the same time - evince depends on poppler.
# WARNING: Do NOT bump to 2.23.x version as other dependencies (e.g libgs and libspectre needed first)
Version:      2.22.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Document viewer
Source:       http://ftp.gnome.org/pub/GNOME/sources/evince/2.22/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# date:2006-06-06 type:branding owner:gman
Patch1:	      evince-01-menu-entry.diff
# date:2008-09-22 type:bug owner:dkenny bugzilla:542924 bugster:6724495
Patch2:	      evince-02-static-enum.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define gtk2_version 2.6.0
%define libgnomeui_version 2.6.0
%define dbus_version 0.33
%define poppler_version 0.4.0
%define libgnomeprintui_version 2.5.1

Requires:	gtk2 >= %{gtk2_version}
Requires:	libgnomeui >= %{libgnomeui_version}
Requires:	dbus >= %{dbus_version}
Requires:	poppler >= %{poppler_version}
Requires:       libgnomeprintui >= %{libgnomeprintui_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  dbus-devel >= %{dbus_version}
BuildRequires:  poppler-devel >= %{poppler_version}
BuildRequires:  libgnomeprintui-devel >= %{libgnomeprintui_version}

%description
Evince is a document viewer capable of displaying multiple and single page document formats like PDF and Postscript.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1

# Remove DOS line end chars. Fixes #395105.
dos2unix -ascii po/be.po po/be.po

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
export PKG_CONFIG_TOP_BUILD_DIR=${PWD}

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS 
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/libxml2" \
  ./configure \
	--prefix=%{_prefix} \
        --libexecdir=%{_libexecdir} \
	--sysconfdir=%{_sysconfdir} \
	--disable-comics		\
    --enable-thumbnailer  \
	--mandir=%{_mandir}
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.a
rm $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.la

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="evince.schemas evince-thumbnailer.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/nautilus/extensions-2.0/*.so*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/applications/*
%{_datadir}/evince/*
%{_datadir}/gnome/help/*
%{_datadir}/omf/*
%{_sysconfdir}/gconf/schemas/*

%changelog
* Mon Sep 22 2008 - darren.kenny@sun.com
- Re-introduce patch evince-02-static-enum.diff to make GEnum types be "static const".
  fixing bug#6724495 since we've reverted back to GNOME 2.22 version.
* Fri Aug 15 2008 - darren.kenny@sun.com
- Reverting back to evince 2.22 due to no libspectre or libgs.so on Solaris
  yet. When these appear I will bump evince again.
* Thu Aug 07 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Wed Jul 23 2008 - damien.carbery@sun.com
- Bump to 2.23.5. Remove upstream patch 02-static-enum.
* Mon Jul 14 2008 - darren.kenny@sun.com
- Add patch evince-03-static-enum.diff to make GEnum types be "static const".
  fixing bug#6724495, logged upstream bug#542924
* Sat Jun 21 2008 - patrick.ale@gmail.com
- Change download URI to fetch from 2.23 branch (URI correction)
* Fri Jun 20 2008 - darren.kenny@sun.com
- Remove unnecessary patch for sfw since gs is now in /usr/bin.
* Thu May 29 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90. Remove upstream patch 03-nautilus-dir.
* Fri Jan 11 2008 - damien.carbery@sun.com
- Add patch 03-nautilus-dir to determine nautilus extension dir via pkgconfig.
* Fri Dec 07 2007 - ghee.teo@sun.com
- added --disable-comics to configure option as it failed on Solaris.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.2. Remove upstream patch, 03-zero-pages-up.
* Mon Nov 19 2007 - darren.kenny@sun.com
- Add a new patch, evince-03-zero-pages-up.diff, to fix bug#6631614 
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 0.9.3.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 0.9.2.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 0.9.1.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 0.9.0.
* Thu May 10 2007 - darren.kenny@sun.com
- Add bug#6553312 ref for gs-sfw patch. 
* Thu Apr 19 2007 - laca@sun.com
- add -ascii option to dos2unix so that utf8 strings are not messed up
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 0.8.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 0.8.0.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 0.7.2.
* Wed Jan 10 2006 - damien.carbery@sun.com
- Bump to 0.7.1. Remove upstream patch, 03-lc-measurement. Add code to dos2unix
  po/be.po to fix #395105.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Add dir to CFLAGS so that libxml headers can be found.
* Wed Dec 20 2006 - damien.carbery@sun.com
- Add patch, 03-lc-measurement, to fix #387887. Patch written by Glynn.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 0.7.0.
* Tue Oct 10 2006 - damien.carbery@sun.com
- Bump to 0.6.1.
* Tue Sep 05 2006 - brian.cameron@sun.com
- Bump to 0.6.0.
* Tue Aug 08 2006 - brian.cameron@sun.com
- Bump to 0.5.5.
* Wed Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 0.5.4.
  And remove patch 03 (upstream)
* Thu Jun 15 2006 - ghee.teo@sun.com
- Fixed 6437235 stop evince from crashing on PAPI print backend.
* Fri Jun 02 2006 - glynn.foster@sun.com
- Bump to 0.5.3
* Fri Apr 28 2006 - glynn.foster@sun.com
- Add patch to install into Office submenu
  with 'Evince Document Viewer'.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 0.5.2.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 0.5.0.
* Tue Nov 08 2005 - glynn.foster@sun.com
- Show the .desktop file entry for the moment.
* Fri Sep 30 2005 - brian.cameron@sun.com
- Bump to 0.4.0
* Wed Aug 24 2005 - damien.carbery@sun.com
- Add libgnomeprintui dependency.
* Tue Aug 16 2005 - glynn.foster@sun.com
- New spec file for evince
