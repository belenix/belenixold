#
# spec file for package gnome-pilot
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include l10n.inc
Name:     	gnome-pilot
License:        GPL v2
Group:		Applications/Communications
Version: 	2.0.17
Release:	1
Distribution:   Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	PalmOS link utilities
Source:		http://download.gnome.org/sources/%{name}/2.0/%{name}-%{version}.tar.bz2
Source1:        %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#date:2006-03-20 owner:gman bugzilla:313203 type:bug
Patch1:         gnome-pilot-01-capplet-install.diff
#date:2006-11-15 owner:calumb bugster:6489289 bugzilla:375639 type:bug
Patch2:         gnome-pilot-02-launch-menu-item.diff
#date:2006-12-13 owner:halton type:branding
Patch3:		gnome-pilot-03-disable-gob-check.diff
#date:2006-12-18 owner:halton type:branding
Patch4:		gnome-pilot-04-usb-default.diff
URL:		http://ftp.gnome.org/pub/GNOME/sources/gnome-pilot
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/gnome-pilot
Autoreqprov:    on
Prereq:         GConf

%define pilot_link_version 0.11.8
%define scrollkeeper_version 0.3.14
%define gnome_panel_version 2.6.1

Requires:	gnome-panel >= %{gnome_panel_version}
Requires:       pilot-link >= %{pilot_link_version}
BuildRequires:	scrollkeeper >= %{scrollkeeper_version}
BuildRequires:	pilot-link-devel >= %{pilot_link_version}

%description
GNOME Pilot is a collection of programs and daemons for using 
Palm OS-based systems with GNOME, the complete user-friendly desktop 
based entirely on free software.

%package -n gnome-pilot-devel
Summary:	Pilot development header files.
Group:		Development/Libraries
Requires:	gnome-pilot = %{version}-%{release}
Requires:	pilot-link-devel >= %{pilot_link_version}

%description -n gnome-pilot-devel
GNOME Pilot is a collection of programs and daemons for using 
Palm OS-based systems with GNOME, the complete user-friendly desktop 
based entirely on free software.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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

LC_ALL=
LANG=
export LC_ALL LANG
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"				\
./configure  --prefix=%{_prefix}		\
	     --sysconfdir=%{_sysconfdir}	\
	     --mandir=%{_mandir}		\
	     --libexecdir=%{_libexecdir}	\
	     --localstatedir=/var		\
	     --disable-pilotlinktest		\
	     --with-pisock=yes			\
	     --with-hal=no 

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm $RPM_BUILD_ROOT%{_libdir}/gnome-pilot/conduits/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gnome-pilot/conduits/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="pilot.schemas"
for S in $SCHEMAS; do
	gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*
%{_datadir}/applications/*
%{_datadir}/idl/*
%{_datadir}/mime-info/*
%{_datadir}/pixmaps/*
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/gnome-pilot/conduits/*.so
%dir %{_datadir}/gnome-pilot
%dir %{_datadir}/gnome-pilot/glade
%{_datadir}/gnome-pilot/conduits
%{_datadir}/gnome-pilot/glade/*.png
%{_datadir}/gnome-pilot/glade/*.glade
%{_datadir}/gnome-pilot/*.xml
%{_datadir}/gnome/help/*
%{_datadir}/omf/*
%{_sysconfdir}/gconf/schemas/pilot.schemas
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files -n gnome-pilot-devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so

%changelog
* Thu Jan 8 2008 - jijun.yu@sun.com
- Bump to 2.0.17.
- Remove upstream patch.

* Fri Apr 18 2008 - jijun.yu@sun.com
- Add a patch to fix bug 6690026 and 6668371.

* Mon Mar 03 2008 - jijun.yu@sun.com
- Rename the patches.

* Wed Feb 27 2008 - jijun.yu@sun.com
- Bump to 2.0.16
- Remove 4 upstream patches
- Rework 2 patches

* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.

* Wed Feb 28 2007 - jijun.yu@sun.com
- Remove upstream patch gnome-pilot-02-pilot_connect.diff

* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Thu Jan 04 2007 - jijun.yu@sun.com
- Update to new version 2.0.15

* Wed Dec 06 2006 - takao.fujiwara@sun.com
- Add gnome-pilot-08-g11n-i18n-ui.diff. bugzilla #138628

* Wed Nov 15 2006 - calum.benson@sun.com
- Patch menu item to match latest UI spec.

* Wed Oct 24 2006 - glynn.foster@sun.com
- Add patch to fix #6437924, and fix up some of the window icons so they look
  a little more consistent. This is bugzilla #364589.

* Wed Jun 28 2006 - halton.huo@sun.com.
- Add patch gnome-pilot-04-remove-nouse-libs.diff to fix #6434263.
- Add patch gnome-pilot-05-disable-gob-check.diff to remove gob build dependency.

* Tue Jun 06 2006 - halton.huo@sun.com
- Remove patch gnome-pilot-01-configure-in.diff and reorder,
  build require gob2.

* Mon Mar 20 2006 - glynn.foster@sun.com
- Install capplet in the right directory - #313203

* Tue Jan 10 2006 - halton.huo@sun.com
- Replace patches by pdasync.prc team:
  deleted: gnome-pilot-01-menu-entry.diff
           gnome-pilot-02-g11n-i18n-ui.diff
           gnome-pilot-03-automake-fix.diff
  added  : gnome-pilot-01-configure-in.diff
           gnome-pilot-02-all-in-one.diff

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Tue May 17 2005 - glynn.foster@sun.com
- Port to 2.0.13

* Fri Feb 11 2005 - dinoop.thomas@wipro.com
- Added patch to make help button in gnome-pilot settings point to 
  correct location.Fixes bug 6225082

* Mon Jan 31 2005 - ghee.teo@sun.com
- Increased the Release number by 200. The problem is that the release
  counter has been reset during  the JDS 3 release cycle but the version
  number has not changed. This causes an update problem because the version
  in JDS 2 appears to be newer than this version. Fixes 6222834.

* Wed Jan 26 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from eugene.oconnor@sun.com.

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
                                                                                
* Wed Nov 17 2004 - matt.keenan@sun.com
- #6195855, install correct man page

* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gpilot-install-file.1, gpilotd-control-applet.1 man pages

* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help files with patch

* Thu Aug 19 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from eugene.oconnor@sun.com.

* Mon Aug 16 2004 - vinay.mandyakoppal@wipro.com 
- Help invocation for the applet is implemented.  

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-pilot-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
                                                                                
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed Jun 09 2004 - damien.carbery@sun.com
- Integrated docs and associated patch from eugene.oconnor@sun.com

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-pilot-l10n-po-1.1.tar.bz2

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris

* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-pilot-l10n-po-1.0.tar.bz2

* Tue Mar 16 2004 - laca@sun.com
- add patch5 to fix build with newer versions of automake
- add --libexecdir

* Fri Mar 05 2004 - takao.fujiwara@sun.com
- Modified %files section in spec file to fix 4932068
- Changed gnome-pilot-04-trans-pilot-menu.diff to gnome-pilot-04-g11n-i18n-ui.diff

* Wed Feb 18 2004 - matt.keenan@sun.com
- Updated distro to Cinnabar, added l10n stuff
- Port patchs 03/04, and libtoolize it

* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Settings keyword from the 
  menu entry patch.

* Fri Oct 10 2003 - laszlo.kovacs@sun.com
- upgrade deps versions

* Fri Oct 03 2003 - <matt.keenan@sun.com>
- remove man pages

* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la

* Mon Aug 01 2003 - glynn.foster@sun.com
- Add some menu categorization

* Mon Jul 28 2003 - michael.twomey@sun.com
- Updated POTFILES.in

* Fri Jul 28 2003 - glynn.foster@sun.com
- Install the applet as part of the main
  package. There is no reason to have an 
  extra package for this one.

* Fri Jul 25 2003 - niall.power@sun.com
- Base package requires pilot-link

* Thu Jul 24 2003 - <matt.keenan@sun.com>
- Initial version
