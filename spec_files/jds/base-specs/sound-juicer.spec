#
# spec file for package sound-juicer
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:         sound-juicer
License:      GPL v2, LGPL v2
Group:        System/GUI/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      CD ripping tool
Source:       http://ftp.gnome.org/pub/GNOME/sources/sound-juicer/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:yippi date:2006-06-05 type:branding
Patch1:       sound-juicer-01-menu-entry.diff
#owner:jerrytan date:2008-07-02 type:bug bugzilla:540857
Patch2:       sound-juicer-02-dev.diff
#owner:jerrytan date:2009-04-03 type:branding bug:7904
Patch3:       sound-juicer-03-start-gconf-first.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%define scrollkeeper_version 0.3.12
%define libgnomeui_version 2.2.0
%define nautilus_cd_burner_version 2.6.0
%define gstreamer_version 0.8.0
%define gnome_media_version 2.10.0
%define music_brainz_version 2.10.0

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       gstreamer >= %{gstreamer_version}
Requires:       gstreamer-plugins >= %{gstreamer_version}
Requires:	nautilus-cd-burner >= %{nautilus_cd_burner_version}
Requires:       gnome-media >= %{gnome_media_version}

BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_version}
BuildRequires:  gstreamer-plugins-devel >= %{gstreamer_version}
BuildRequires:  nautilus-cd-burner >= %{nautilus_cd_burner_version}
BuildRequires:  scrollkeeper >= %{scrollkeeper_version}
BuildRequires:  gnome-media >= %{gnome_media_version}

%description
sound-juicer is a CD ripping tool based on GTK+ and GStreamer

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS 
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--disable-scrollkeeper \
	--localstatedir=%{_localstatedir}
make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/sound-juicer
%{_datadir}/applications/sound-juicer.desktop
%{_datadir}/gnome/help/sound-juicer
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/sound-juicer/*.omf
%{_datadir}/pixmaps/*
%{_datadir}/sound-juicer

%changelog
* Tue Apr 14 2009 - brian.cameron@sun.com
- Bump to 2.26.1.
* Wed Mar 18 2009 - brian.cameron@sun.com
- Bump to 2.26.0.
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92.
* Tue Feb 17 2009 - brian.cameron@sun.com
- Bump to 2.25.3.  Remove upstream patch sound-juicer-02-add-libsocket.diff.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.1.
* Thu Sep 25 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.3, rework patches/sound-juicer-03-dev.diff.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.2
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.1.

* Thu Jul 3 2008  - jerry.tan@sun.com
- Add patch sound-juicer-03-dev.diff to fix wrong dev path error

* Thu Jun 05 2008 - damien.carbery@sun.com
- Bump to 2.23.0.

* Fri May 16 2008 - jerry.tan@sun.com
- Remove sound-juicer-02-eject-cd.diff to enable eject for cdrom.

* Wed May 14 2008 - dave.lin@sun.com
- Add patch sound-juicer-03-add-libsocket.diff to fix build error.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.

* Thu Feb 14 2008 - damien.carbery@sun.com
- Bump to 2.21.91.

* Thu Jan 31 2008 - damien.carbery@sun.com
- Bump to 2.21.3.

* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.2.

* Wed Jan 02 2008 - damien.carbery@sun.com
- Bump to 2.21.1.

* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.21.0.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1. Remove upstream patch, 02-unlock-device.

* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.3.

* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.2.

* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.1.

* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.0. Remove upstream patch, 01-fixplugin, renumber rest.

* Mon Apr 16 2007 - damien.carbery@sun.com
- Bump to 2.16.4.

* Thu Mar 15 2007 - damien.carbery@sun.com
- Bump to 2.16.3.

* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.

* Tue Oct 31 2006 - takao.fujiwara@sun.com
- Added intltoolize to read LINGAS. Fixes 6488189.

* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.

* Mon Aug 21 2006 - damien.carbery@sun.com
- Bump to 2.15.5.1.

* Sun Jul 30 2006 - damien.carbery@sun.com
- Use single thread 'make' because of build problems with multiple threads.

* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.4.

* Fri Jul 21 2006 - brian.cameron@sunc.om
- Remove patch to fix duration, since this was just hiding the
  real problem in musicbrainz.  Patch added to musicbrainz to fix
  the problem.

* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 2.15.3.

* Tue Jul 11 2006 - brian.cameron@sun.com
- Fix so duration values are correct when running in offline mode
  (where soundjuicer cannot connect to musicbrainz server).

* Wed Jun 21 2006 - brian.cameron@sun.com
- Bump to 2.14.4.

* Fri Jun 02 2006 - glynn.foster@sun.com
- Add patch for menu entry according to the UI
  spec.

* Tue May 04 2006 - brian.cameron@sun.com
- Fix plugin to the correct one for Solaris.

* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 2.14.3.

* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.2.

* Tue Apr  4 2006 - damien.carbery@sun.com
- Bump to 2.14.1.

* Tue Mar 28 2006 - brian.cameron@sun.com
- Update patch and fix compile on Solaris.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.6.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.5.

* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 2.13.4.

* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.2

* Tue Dec 20 2005 - dermot.mcclusey@sun.com
- Bump to 2.13.1

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.3.

* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 2.12.2

* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.

* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.91.

* Thu Jun 16 2005 - matt.keenan@sun.com
- Specify %files to package

* Fri Mar 13 2005 - glynn.foster@sun.com
- Bump to 2.10.1
