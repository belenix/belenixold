#
# spec file for package gnome-applets 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# Owner: migi
#
Name:         gnome-applets 
License:      GPL
Group:        System/GUI/GNOME 
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      GNOME Applets
Source:       http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
#owner:gman date:2005-05-11 type:branding
Patch1:       gnome-applets-01-disable-drivemount.diff
#owner:gman date:2005-05-11 type:branding
Patch2:       gnome-applets-02-non-utf8-date-title.diff
#owner:gman date:2005-05-11 type:branding
Patch3:	      gnome-applets-03-make-multiload-network-available.diff
#owner:gman date:2005-18-02 type:branding
Patch4:       gnome-applets-04-deprecate-now-applet.diff
#owner:jedy date:2007-03-07 bugzilla:397477 bugster:6621806 type:bug
Patch5:	      gnome-applets-05-battstat.diff
#owner:mattman date:2008-08-28 type:bug bugzilla:549722 bugster:6741535
Patch6:	      gnome-applets-06-accessx-crash.diff
#owner:migi date:2008-29-09 type:bug bugzilla: 554277 defect.opensolaris:3625
Patch7:       gnome-applets-07-drive-button.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/gnome-applets
Autoreqprov:  on
Prereq:       GConf

%define python_version 2.4
%define gnome_panel_version 2.4.0
%define scrollkeeper_version 0.3.12
%define libgtop_version 2.9.4
%define gail_version 1.4.0
%define gstreamer_plugins_version 0.8.9

BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: gnome-panel >= %{gnome_panel_version}
BuildRequires: libgtop-devel >= %{libgtop_version}
BuildRequires: gail >= %{gail_version}
BuildRequires: gstreamer-plugins-devel >= %{gstreamer_plugins_version}
Requires:      gnome-panel >= %{gnome_panel_version}
Requires:      libgtop >= %{libgtop_version}
Requires:      gail >= %{gail_version}
Requires:      gstreamer-plugins >= %{gstreamer_plugins_version}

Obsoletes:	gnome-address-applet <= 0.0.1

%description
GNOME Applets contains a collection of small utilities that are run within the GNOME
Panel.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

for po in po/*.po; do
  dos2unix -ascii $po $po
done

%build
libtoolize --force
aclocal $ACLOCAL_FLAGS -I ./m4
autoheader
automake -a -c -f
autoconf

# Set LIBGWEATHER info as the gweather.pc file has been removed. The interface
# has been defined as private in the GNOME 2.22 ARC case.
export LIBGWEATHER_CFLAGS=-I%{_includedir}
export LIBGWEATHER_LIBS="-L%{_libdir} -lgweather -lm"

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --libexecdir=%{_libexecdir} \
	    --with-gstreamer=0.10       \
	    --enable-stickynotes        \
	    --disable-gswitchit         \
            --disable-scrollkeeper      \
            --enable-mixer-applet

make -j $CPUS \
        pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

# Mixer applet only built if gstreamer-plugins-devel installed

%ifos linux
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/gnome-applets/gkb-*
%endif

rm -rf $RPM_BUILD_ROOT/usr/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="battstat.schemas charpick.schemas cpufreq-applet.schemas geyes.schemas gtik.schemas gweather.schemas mini-commander-global.schemas mini-commander.schemas mixer.schemas multiload.schemas stickynotes.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done
%{_libexecdir}/gnome-applets/mc-install-default-macros

%files
%defattr (-, root, root)
%{_sysconfdir}/gconf/schemas/*.schemas
%{_sysconfdir}/sound/events/
%{_bindir}/*
%{_libdir}/bonobo/servers/*.server
%{_libdir}/pkgconfig/*.pc
%{_libexecdir}/*
%{_datadir}/gnome/help/*
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-applets/*
%{_datadir}/icons/*
%{_datadir}/locale/*/LC_MESSAGES/gnome-applets-2.0.mo
%{_datadir}/omf/*
%{_datadir}/pixmaps/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Wed Feb 18 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Mon Feb 16 2009 - Matt.Keenan@sun.com
- Bump to 2.25.90
* Fri Jan 30 2009 - Michal.Pryc@Sun.Com
- added "--enable-mixer-applet" to the configure scipt.
- patches/gnome-applets-01-disable-drivemount.diff: Reworked
- patches/gnome-applets-04-deprecate-now-applet.diff: Reworked
* Fri Dec 26 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Mon Sep 29 2008 - Michal.Pryc@Sun.Com
- Bump to 2.24.0.1
- gnome-applets-07-drive-button.diff: 
 Fix: defect.opensolaris: 3625, bugzilla: 554277
* Wed Sep 17 2008 - Michal.Pryc@Sun.com
- Bump to 2.23.92: Fixes 6747363
- Rework gnome-applets-06-accessx-crash.diff
* Sat Sep 06 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 28 2008 - matt.keenan@sun.com
- Remove patch 06-fixsticky.diff, applied upstream
- Add patch 06-accessx-crash.diff : Fixes : 6741535
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.4.

* Mon Jun 16 2008 - damien.carbery@sun.com
- Bump to 2.23.3.

* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.

* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.22.2.

* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.

* Tue Apr 08 2008 - damien.carbery@sun.com
- Set LIBGWEATHER_CFLAGS and LIBGWEATHER_LIBS because the gweather.pc file has
  been removed. The interface has been defined as private in the GNOME 2.22 ARC
  case.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.

* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.

* Thu Jan 31 2008 - brian.cameron@sun.com
- Add patch gnome-applets-06-fixsticky.diff to fix crashing issue
  with the StickyNotes applet.

* Wed Jan 16 2008 - damien.carbery@sun.com
- Bump to 2.21.4.

* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.2.

* Mon Nov 12 2007 - damien.carbery@sun.com
- Bump to 2.21.1. Remove upstream patch, 06-mixerpoll.

* Thu Oct 11 2007 - brian.cameron@sun.com
- Add patch gnome-applets-06-mixerpoll.diff so that the mixer applet polls
  for changes in the volume less frequently.  Also set python_version and call
  make install setting pyexecdir/pythondir properly so that the invest python
  code gets built and installed.  Otherwise this applet doesn't work.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.91.

* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 2.19.1.

* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.0. Remove upstream patch, 06-gtk-tooltips.

* Wed Jul 25 2007 - damien.carbery@sun.com
- Add upstream patch, 06-gtk-tooltips, to allow building against new gtk+.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Mon Mar 05 2006 - damien.carbery@sun.com
- Bump to 2.17.90.

* Mon Feb 19 2006 - damien.carbery@sun.com
- Specify pythondir in make install so that we install into vendor-packages dir
  rather than site-packages.

* Sun Feb 18 2007 - glynn.foster@sun.com
- Sucky patch to deprecate the now applet completely. Maybe we can 
  remove this in the future.

* Wed Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.17.1. Remove patch, 03-disable-keyboard-layout, because the
  libxklavier sections are no longer present. Renumber remainder.

* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.

* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.

* Fri Sep 15 2006 - brian.cameron@sun.com
- Remove stale patches.

* Thu Sep 14 2006 - brian.cameron@sun.com
- Rework gnome-applets-04-disable-keyboard-layout.diff patch so that the
  gswitchit applet is disabled with --disable-gswitchit, which is now 
  added to configure call.

* Mon Sep 04 2006 - brian.cameron@sun.com
- Add patch so that the multiload applet builds, since it needs -lXau on the
  linker call.

* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.1.

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.

* Wed Aug 23 2006 - damien.carbery@sun.com
- Reenable building of stickynotes, turned off because TomBoy is a replacement.

* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
- Remove upstream patch, 05-hidden, renumber remainder.

* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.3.

* Fri Jul 28 2006 - damien.carbery@sun.com
- Remove upstream patch, 07-multiload. dos2unix the po files.

* Fri Jul 28 2006 - brian.cameron@sun.com
- Correct patches.  

* Fri Jul 28 2006 - darren.kenny@sun.com
- Add multiload patches

* Fri Jul 28 2006 - damien.carbery@sun.com
- Bump to 2.15.2.

* Thu Jul 27 2006 - brian.cameron@sun.com
- Remove patch patches/gnome-applets-04-prefer-sdtaudiocontrol.diff since
  now gnome-volume-control is in better shape.

* Thu Jul 27 2006 - damien.carbery@sun.com
- Add patch, 06-hidden, for G_GNUC_INTERNAL changes.

* Wed Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.1.1.

* Sat Jul 15 2006 - glynn.foster@sun.com
- Add patch to remove all the keyboard layout features.

* Tue May 16 2006 - calum.benson@sun.com
- Have mixer's "open audio control" menu item run sdtaudiocontrol (if present)
  rather than gnome-volume-control, as per UI spec.

* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.

* Sun Mar 12 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 2.13.90.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.4.

* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
- Remove upstream patches, 04-trashapplet and 05-gstreamer10.
- Modified configure to use gstreamer 0.10.

* Thu Jan 19 2006 - brian.cameron@sun.com
- Add patch 05 so that it builds with GStreamer 0.10.

* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.2

* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.13.1.

* Wed Nov 30 2005 - damien.carbery@sun.com
- Remove upstream patch, gnome-applets-05-Wall.diff.

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.

* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1

* Tue Sep 20 2005 - laca@sun.com
- update -Wall.diff

* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Tue Sep 13 2005 - laca@sun.com
- use --disable-scrollkeeper so that make install doesn't try to update
  the scrollkeeper data in /var
- add patch trashapplet.diff
- add patches Wall.diff (remove -Wall CFLAGS) and fontconfig.diff
  (add -lfontconfig)

* Mon Aug 29 2005 - laca@sun.com
- remove solaris.diff (upstream) and powersaved-support-for-battstat.diff
  (broken)

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.

* Thu Jul 07 2005 - archana.shah@wipro.com
- Added patch gnome-applets-05-powersaved-support-for-battstat.diff to make use
  of libpowersave.
  Patch taken for #6237356

* Mon Jun 20 2005 - matt.keenan@sun.com
- Add requires for gstreamer-plugins for mixer-applet build

* Fri Jun 03 2005 - leena.gunda@wipro.com
- Added patch gnome-applets-22-gkb-applet-show-message.diff to popup a
  message when user adds gkb-applet to panel. Fixes bug #6245563.

* Tue May 24 2005 - brian.cameron@sun.com
- Cleanup.

* Thu May 19 2005 - brian.cameron@sun.com
- No longer call javahelp-convert-install for cdplayer, mailcheck or gkb
  since they are no longer in gnome-applets.

* Mon May 16 2005 - kazuhiko.maekawa@sun.com
- l10n help files follow base bug fix 6265900 and 6227253

* Fri May 13 2005 - brian.cameron@sun.com
- Only build with tm_gmtoff if it is available.  It's not on Solaris so this
  fixes the build.

* Fri May 13 2005 - brian.cameron@sun.com
- Add "-I ./m4" to aclocal since it is needed.

* Wed May 11 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.1

* Thu May 05 2005 - damien.carbery@sun.com
- 6265900: Change xml file in accessx-status-C.omf from accessx-status.xml to
  gnome-access-guide.xml#dtconfig-21 (as in submitted file). A hack that is
  easy to maintain.

* Mon Apr 18 2005 - damien.carbery@sun.com
- 6227253: Change xml file in gweather-C.omf from gweather.xml to
  sample_apps_info.xml (part of gnome-user-docs). Bit of a hack but a very easy
  one to maintain.

* Thu Mar 17 2005 - srirama.sharma@wipro.com
- Updated gnome-applets-19-powersaved-support-for-battstat.diff to
  make sure that the battstat applet shows proper tooltip information.
  Fixes bug #6237356. 
 
* Mon Mar 14 2005 - damien.carbery@sun.com
- Remove 'rm' of gweather omf files.

* Sat Mar 12 2005 - damien.carbery@sun.com
- Comment out patch 20 because it clashes with the new docs tarball.

* Fri Mar 11 2005 - damien.carbery@sun.com
- Integrate docs tarball (gnome-applets_docs-0.13linux) from irene.ryan@sun.com.

* Wed Feb 16 2005 - alvaro.lopez@sun.com
- Obsoletes header fixed: added version.

* Wed Feb 16 2005 - damien.carbery@sun.com
- Integrate docs tarball (gnome-applets_docs-0.12linux) from 
  maeve.anslow@sun.com.

* Fri Feb 11 2005 dinoop.thomas@wipro.com
- Added patch to include tooltip for modemlights.
  Fixes bug 4958878.
 
* Wed Feb 02 2005 glynn.foster@sun.com
- Remove drivemount.

* Tue Feb 01 2005 alvaro.lopez@sun.com
- Obsoletes gnome-address-applet 

* Fri Jan 28 2005 matt.keenan@sun.com
- #6222302 : Remove gkb from yelp for linux
- #6222336 : Remove gweather from yelp

* Mon Jan 24 2005 srirama.sharma@wipro.com
- Adding autoheader to pick up the powersaved changes.
 
* Mon Jan 24 2005 archana.shah@wipro.com
- gnome-applets-17-cdplayer-applet-work.diff: Patch removed.
  gnome-applets-17-cdplayer-play.diff: Patch added. Fixes bug#6185200
  Also fixes bugs #6215743 & #6215744

* Fri Jan 21 2005 matt.keenan@sun.com
- #6219571 : Remove gkb help from linux

* Mon Jan 17 2005 alvaro.lopez@sun.com
- Updated URL

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
                                                                                
* Fri Jan 14 2005 takao.fujiwara@sun.com
- Updated gnome-applets-04-g11n-i18n-ui.diff from community reply.
- Added gswitchit.schemas in spec file

* Thu Jan 13 2005 matt.keenan@sun.com
- #6200378, accessx status applet help

* Wed Jan 12 2005 takao.fujiwara@sun.com
- Updated gnome-applets-04-g11n-i18n-ui.diff to localize gswitchit.
  Fixing bug 6216093

* Fri Jan 07 2005 srirama.sharma@wipro.com
- Added gnome-applets-19-powersaved-support-for-battstat.diff to 
  make battstat applet work using powersave library functions.

* Thu Dec 16 2004 srirama.sharma@wipro.com
- Added gnome-applets-18-mixer-volume-control.diff  to control 
  volume properly using "+" and "-" keys. Fixes the Bug #4991121.

* Mon Dec 06 2004 vinay.mandyakoppal@wipro.com
- Added gnome-applets-17-cdplayer-applet-work.diff to make cdplayer
  applet work. Fixes bug #6185200.
 
* Fri Nov 26 2004 glynn.foster@Sun.COM
- Add workaround patch to disable gswitchit on Solaris. Fixes 
  bug #6184440 temporarily.

* Wed Nov 10 2004 Chookij.Vanatham@Sun.COM
- Added patch gnome-applets-15-non-utf8-date-title.diff to fix
  undisplayed non-utf8 date at the title. Fixes bug 6176791.

* Mon Nov 08 2004 - matt.keenan@sun.com
- #5076490, add patch 14-gkb-help.diff

* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gkb_xmmap.1, gnome-keyboard-layout.1, gswitchit-plugins-capplet.1 man pages

* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR

* Wed Oct 27 2004 damien.carbery@sun.com
- Integrate updated docs tarball from maeve.anslow@sun.com.

* Fri Oct 01 2004 bill.haneman@sun.com
- Added replacement image for accessx-status/pixmaps/sticky-meta-locked.png.

* Thu Sep 30 2004 vinay.mandyakoppal@wipro.com
- Added patch gnome-applets-12-gswitchit-help.diff to fix help
  issues. Fixes bug #5076490

* Wed Sep 29 2004 srirama.sharma@wipro.com
- Added patch gnome-applets-11-volume-control-icon.diff
  to provide a icon in gnome desktop menu. Fixes bug #5099353.

* Wed Sep 29 2004 vinay.mandyakoppal@wipro.com
- Added patch gnome-applets-10-save-password.diff to make
  "Save the password to disk" work. Fixes bug #5103157.
 
* Wed Sep 08 2004 matt.keenan@sun.com
- Bumped tarball to 2.6.2.1 for a11y bug fixes
- Removed patch gnome-applets-07-accessx-xkb-check.diff
- Removed patch gnome-applets-08-accessx-fix-crash.diff
- Removed patch gnome-applets-09-gkb-crash.diff
- Removed patch gnome-applets-11-accessx-xkb-crash.diff
- Renamed patch 10 -> 07
- Renamed patch 12 -> 08
- Renamed patch 13 -> 09

* Fri Aug 27 2004 damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.
- Removed patch 14 because the imswitcher directory has been removed because
  it is in another module - gnome-im-switcher.

* Thu Aug 26 2004 damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.
- Removed gswitchit-docs tarball as is part of gnome-applets_docs now.

* Wed Aug 25 2004 damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.

* Wed Aug 25 2004 Kazuhiko.Maekawa@sun.com
- Added l10n help contents

* Thu Aug 19 2004 damien.carbery@sun.com
- Add new gswitchit docs tarball from breda.mccolgan@sun.com.

* Tue Aug 17 2004 - balamurali.viswanathan@wipro.com
- Remove "--enable-gstreamer=no" option to the configure script. So that mixer
  applet can use sunaudio plugin.

* Mon Aug 09 2004 - balamurali.viswanathan@wipro.com
- Add "--enable-gstreamer=no" option to the configure script. So that mixer
  applet uses SUN APIs to change volume. Only for Solaris.

* Thu Aug 05 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Thu Jul 29 2004 - matt.keenan@sun.com
- Bug : 5077650, help bug

* Thu Jul 22 2004 - glynn.foster@sun.com
- Disable the wireless applet.

* Mon Jul 19 2004 - niall.power@sun.com
- merged with HEAD

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-applets-l10n-po-1.2.tar.bz2

* Thu Jul 08 2004 - dermot.mccluskey@sun.com
- undid -j $CPUS for this module

* Thu Jul 08 2004 - stephen.browne@sun.com
- Ported to rpm4/SLES9

* Wed Jul 07 2004 - leena.gunda@wipro.com
- added gnome-applets-12-accessx-xkb-crash.diff to fix bug #5067184.

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Thu Jun 24 2004 vijaykumar.patwari@wipro.com
- Associate default macros for mini commander applet.

* Wed Jun 02 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Wed Jun 02 2004 - leena.gunda@wipro.com
- Add patch gnome-applets-10-gkb-crash.diff to fix bug #5043883.

* Mon May 31 2004 - padraig.obriain@sun.com
- Add patch gnome-applets-08-accessx-fix-crash.diff bugzilla - bug #137585.

* Mon May 31 2004 - matt.keenan@sun.com
- Update to 2.6.1, remove patch-05, re-apply 01, rename 09 to 05

* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-applets-l10n-po-1.1.tar.bz2

* Mon May 10 2004 - archana.shah@wipro.com
- Added gnome-applets-09-mailcheck-pop3.diff

* Mon May 10 2004 - archana.shah@wipro.com
- Added gnome-applets-08-wireless-tooltip.diff

* Tue Apr 27 2004 - arvind.samptur@wipro.com
- Added gnome-applets-07-accessx-xkb-check.diff to fix the applet
  not to crash when XKB is not enabled on the X server

* Fri Apr 23 2004 - archana.shah@wipro.com
- Modified the tooltip for mini-commander applet.
- Patch: gnome-applets-06-mini-commander-tooltip.diff

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
- ifos the javahelp conversions of applets not available on Solaris
* Mon Apr 05 2004 - matt.keenan@sun.com
- Bump to 2.6.0
- Re-apply patch 03-g18n..
- Remove patch 05-non_portable_CFLAGS
- Rename patch 06 -> to patch 05

* Thu Apr 01 2004 - damien.donlon@sun.com
- javahelp conversion

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-applets-l10n-po-1.0.tar.bz2

* Tue Mar 16 2004 - glynn.foster@sun.com
- Updated version to 2.5.8, killed off a few patches that
  we know are going to make 2.6.0, and sanitize things a little.
* Mon Mar 15 2004 - takao.fujiwara@sun.com
- Replaced gnome-applets-01-potfiles.diff with 
  gnome-applets-01-g11n-potfiles.diff
- Replaced gnome-applets-08-gweather-i18n.diff with
  gnome-applets-08-g11n-i18n-ui.diff to fix 4980055, 4991808, 4999133
- Added gnome-applets-10-g11n-schemas.diff
* Mon Feb 23 2004 - <matt.keenan@sun.com>
- Bumped to 2.5.6
- Remerged all patches
- Brought forward NEW changes from patch
  gnome-applets-19-i18n-ui.diff, This should have been ported to HEAD by Wipro !!!
* Tue Feb 17 2004 - <laca@sun.com>
- added patch to remove non-portable CFLAGS hardcoded in a Makefile.am
* Wed Feb 04 2004 - <matt.keenan@sun.com>
  Fix prob with gnome-applets-08-gweather-i18n.diff
  Remove pixmaps/gweather/* from files list as no longer in tarball
* Tue Feb 03 2004 - <Matt.Keenan@sun.com>
  Bump to 2.5.5
  Redid Patchs :
	gnome-applets-02-stickynotes-icon.diff
	gnome-applets-06-add-l10n-docs.diff
  Forward port patches from Quicksilver
	gnome-applets-07-l10n-online-help.diff
		QS: gnome-applets-17-multiload-docs.diff
		QS: gnome-applets-18-multiload-docs2.diff
		QS: gnome-applets-22-l10n-online-help.diff
	gnome-applets-08-gweather-i18n.diff
		QS: gnome-applets-19-i18n-gweather.diff
* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Bump to 2.5.2
* Thu Oct 23 2003 - <matt.keenan@sun.com>
- #4942358 patch 09
* Tue Oct 14 2003 - <matt.keenan@sun.com>
- Upgrade Tarball to 2.4.1 for QS
* Wed Oct 01 2003 - <matt.keenan@sun.com>
- #4930230, Wireless doc install
* Wed Oct 01 2003 - <matt.keenan@sun.com>
- #4905881, Battery applet suspend command failure message
* Tue Sep 30 2003 - <matt.keenan@sun.com>
- #4913408, cd player applet stops playing
* Tue Sep 30 2003 - <matt.keenan@sun.com>
- #4922609, stock ticker location change bug
* Fri Sep 26 2003 - <laca@sun.com>
- Integrate Sun docs
* Mon Sep 08 2003 - <matt.keenan@sun.com>
- patch for bug 4911981
* Tue Aug 12 2003 - <matt.keenan@sun.com>
- Not delivering gweather/Locations
* Mon Aug 11 2003 - <matt.keenan@sun.com>
- Update new tarball 2.3.6, and re-alligned all the patches, remove one patch
* Thu Aug 07 2003 - <matt.keenan@sun.com>
- Save current keyboard layout #4887871
* Thu Aug 07 2003 - <matt.keenan@sun.com>
- Default battstat suspend computer command
* Wed Aug 06 2003 - <glynn.foster@sun.com>
- Position the file selector dialog for mini-commander
  applet nicely.
* Wed Jul 23 2003 - <glynn.foster@sun.com>
- Add consistant window icon
* Tue Jul 22 2003 - <glynn.foster@sun.com>
- Make sure geyes themes get installed
* Tue Jul 22 2003 - <glynn.foster@sun.com>
- New mixer icon
* Mon Jul 21 2003 - <glynn.foster@sun.com>
- Changed stickynotes icon for the hell of it
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Thu Jul 03 2003 - Matt.Keenan@sun.com
- Patch for accessx-applet from head
* Thu Jul 03 2003 - Matt.Keenan@sun.com
- New Tarball, gnome-applets-2.3.5
* Tue Jun 10 2003 - Matt.Keenan@sun.com
- New Tarball, gnome-applets-2.3.4, updated files and schemas for new applets.
* Thu May 15 2003 - Matt.Keenan@sun.com
- Fix installation of mixer & wirelass applets icons
* Wed May 14 2003 - Laszlo.Kovacs@Sun.COM
- Initial release
