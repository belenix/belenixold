#
# Copyright (c) 2003-2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# Owner: migi
#
%include l10n.inc
Name:         gnome-netstatus
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1 
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      The GNOME Network Monitor Applet
Source:       http://ftp.gnome.org/pub/GNOME/sources/gnome-netstatus/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
%endif
Source2:      gnome-netstatus-wireless-icons-0.2.tar.gz
%if %build_l10n
Source3:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
#owner:gman date:2005-02-03 type:branding
Patch1:       gnome-netstatus-01-restart.diff
#owner:gman date:2005-02-03 type:branding
Patch2:       gnome-netstatus-02-kstat-solaris.diff
#owner:mattman date:2007-08-24 type:bug bugster:6577129 bugzilla:469864
Patch4:       gnome-netstatus-04-default-interface.diff
#owner:dkenny date:2008-06-23 type:feature 
Patch5:       gnome-netstatus-05-wifi-info.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/gnome-netstatus
Autoreqprov:  on

%define libglade_version 2.3.6
%define gnome_panel_version 2.6.1

Requires: libglade >= %{libglade_version}
Requires: gnome-panel >= %{gnome_panel_version}

BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}

%description
This package contains an applet which provides information
about a network interface on your panel.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE3 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1

cd icons
gzip -cd %SOURCE2 | tar xvf -
cd ..

#FIXME: see below
echo > po/ne.po

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

gnome-doc-common
gnome-doc-prepare
libtoolize --force
intltoolize -f -c --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

#FIXME: "ne" po file seems broken, disabling for now
LINGUAS="ar az bg bn bs ca cs cy da de el en_CA en_GB es et eu fa fi fr ga gl gu hi hr hu id it ja ko lt mn ms nb nl nn no pa pl pt pt_BR ro ru rw sk sq
sr sr@Latn sv ta th tr vi uk wa xh zh_CN zh_TW"
export LINGUAS
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-scrollkeeper

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="netstatus.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%doc %{_datadir}/gnome/help/gnome-netstatus
%config %{_sysconfdir}/gconf/schemas/*.schemas
%{_libdir}/bonobo/servers/*.server
%{_libexecdir}/*
%{_datadir}/pixmaps/*
%{_datadir}/gnome-netstatus/
%{_datadir}/gnome/help/*
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/icons/hicolor/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/gnome-netstatus/*.omf

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Removed upstreamed patch 03-icon-symlink.diff.
* Fri Oct 17 2008 - takao.fujiwara@sun.com
- Updated 03-icon-symlink.diff because *-wifi-info.diff modifies
  icons/Makefile.am and *.png files are not installed. Fixes 6759654.
- Updated 06-wifi-info.diff to localize "none" and "open". Fixes 6761162.

* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.

* Mon Sep 28 2008 - darren.kenny@sun.com
- Bump to 2.12.2 remove upstream patch gnome-netstatus-06-icon-dirs.diff, and
  renumber existing patches.

* Mon Sep 15 2008 - darren.kenny@sun.com
- Fix bug#6748400, to update to use new mechanism for icons and enable support
  for nimbus icons.

* Fri Aug 22 2008 - darren.kenny@sun.com
- Add patch gnome-netstatus-06-icon-dirs.diff, taken from upstream, to fix
  location of application icons - bugzilla#435668.
- Add wireless support on Solaris - gnome-netstatus-07-wifi-info.diff
  RFE#6740396.

* Wed May 14 2008 - dave.lin@sun.com
- Add patch gnome-netstatus-05-add-ldlibs.diff to fix build error

* Fri Aug 24 2007 - matt.keenan@sun.com
- Fix #6577129 : Default to working interface

* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.12.1.

* Wed Dec 06 2006 - takao.fujiwara@sun.com
- Added intltoolize to read ALL_LINGUAS. Fixes 6499663

* Thu Nov 16 2006 - damien.carbery@sun.com
- Add patch 04-icon-symlink to make l10n image symlinks relative rather than
  absolute. Fixes WOS integration issue which prohibits absolute symlinks.
  Bugzilla 375932.

* Mon Oct 03 2005 - damien.carbery@sun.com
- Add patch to fix po/ne.po (dos2unix required). Bugzilla 316750.
  Remove javahelp-convert code as the docs are no longer used.

* Thu Sep 15 2005 - brian.cameron@sun.com
- Bump to 2.12.0

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
                                                                                
* Tue Dec 21 2004 - vinay.mandyakoppal@wipro.com
- Added gnome-netstatus-06-Shift+F10-not-working.diff to make 
  Shift+F10 work. Fixes bug#6193273.

* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR

* Tue Oct 05 2004 - matt.keenan@sun.com
- Removed patch 03-docs.diff #5108690
- Renamed patch 05-g11n-alllinguas.diff to 03-g11n-alllinguas.diff

* Fri Sep 17 2004 - ciaran.mcdermott@sun.com
- Added gnome-netstatus-05-g11n-alllinguas.diff to add zh_TW lingua

* Mon Sep 06 2004 - matt.keenan@sun.com
- Added javahelp-convert for gnome-netstatus docs

* Wed Aug 25 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.

* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents

* Fri Aug 13 2004 - damien.carbery@sun.com
- Change absolute symlinks to relative for s10 integration. Patch wos_symlinks.

* Mon Aug 09 2004 - takao.fujiwara@sun.com
- Fixed build error.

* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs tarball from breda.mccolgan@sun.com
- Added patch to omit non-C locales from help.

* Fri Jul 23 2004 - muktha.narayan@wipro.com
- Added gnome-netstatus-02-kstat-solaris.diff to use kstat
  in Solaris.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Adding gnome-netstatus-l10n-po-1.2.tar.bz2 l10n content

* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Mon Jun 14 2004 - misha@sun.com
- Removed upstream patch gnome-netstatus-01-right-click-help.diff
  Removed upstream patch gnome-netstatus-02-include-socket-h.diff
  Removed upstream patch gnome-netstatus-04-g11n-potfiles.diff
  Removed broken patch gnome-netstatus-03-wireless.diff

* Tue Jun 08 2004 - misha@sun.com
- Bump to 2.7.1
  Network interface restart patch is added.

* Mon May 23 2004 - yuriy.kuznetsov@sun.com
- Added patch gnome-netstatus-04-g11n-potfiles.diff

* Mon May 17 2004 - damien.carbery@sun.com
- Correct Requires line: iwlib -> wireless-tools.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-netstatus-l10n-po-1.1.tar.bz2

* Tue May 12 2004 - mark.carey@sun.com
- add patch #3 (wireless support linux only)

* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1

* Sun May 02 2004 - laca@sun.com
- add patch #2 (include-socket-h) to fix build on Solaris

* Fri Apr 30 2004 - muktha.narayan@wipro.com
- Modified gnome-netstatus-01-right-click-help.diff to
  include the 'Help' menu item in GNOME_NetstatusApplet.xml file,
  fix a warning and open the correct help page for preference tab.

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-netstatus-l10n-po-1.0.tar.bz2

* Wed Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 2.6.0. Remove l10n and socksio headers, upstream.
  Refactor help patch not to use egg stuff.

* Wed Mar 03 2004 - <niall.power@sun.com>
- Patch #03 to fix build on solaris.
- replace "tar jxf" with "bzcat | tar -xf -"
- run gnome-doc-common and autoheader in build
- specify libexecdir in configure args

* Fri Feb 27 2004 - <matt.keenan@sun.com>
- Fix gnome-netstatus-02-right-click-help.diff as it was not applying... should have bee tested !
- Fix gnome-netstatus-01-i18n.diff : zh_HK bug in patch.... hmmm

* Tue Feb 24 2004 - <shakti.sen@wipro.com>
- Added gnome-netstatus-02-right-click-help.diff to provide right-click help
  support for the applet as well as support for multi-head.

* Tue Feb 10 2004 - <matt.keenan@sun.com>
- Bump to 0.14, add docs/l10n, port patches 01/02

* Mon Jul 07 2003 - <markmc@sun.com>
- Move to 0.11

* Thu Jun 12 2003 - <markmc@sun.com>
- Move to 0.10

* Thu Jun 12 2003 - <markmc@sun.com>
- Initial spec file

