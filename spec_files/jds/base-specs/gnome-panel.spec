#
# spec file for package gnome-panel
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:		gnome-panel
License:	GPL
Group:		System/GUI/GNOME
Version:	2.26.0
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	The GNOME Panel
Source:		http://ftp.gnome.org/pub/GNOME/sources/gnome-panel/2.26/gnome-panel-%{version}.tar.bz2
%if %option_with_sun_branding
Source1:	gnome-main-menu.png
%endif
Source2:	gnome-time-settings.apps
Source3:	world_map-960.png
Source4:	%{name}-po-sun-%{po_sun_version}.tar.bz2
Source5:	l10n-configure.sh
Source6:	top-panel-image.png
Source7:	bottom-panel-image.png
%if %build_l10n
Source8:                 l10n-configure.sh
%endif
%if %option_with_sun_branding
# date:2003-05-30 type:branding owner:gman
Patch1:		gnome-panel-01-default-setup.diff
%endif
%if %option_with_indiana_branding
# date:2007-10-24 type:branding owner:gman
Patch1:		gnome-panel-01-default-setup-indiana.diff
%endif
# date:2004-09-30 type:branding owner:mattman 
Patch2:		gnome-panel-02-fish-applet.diff
# date:2004-10-18 type:feature bugster:4984097 owner:mattman 
Patch3:		gnome-panel-03-concurrent-login.diff
# date:2005-02-28 type:bug bugster:4912432 owner:mattman bugzilla:447901
Patch5:		gnome-panel-05-notificationarea-tooltip.diff
# date:2005-03-14 type:bug bugster:6239962,6239963 bugzilla:170268 owner:mattman
Patch6:		gnome-panel-06-input-method-filter-keypress.diff
# date:2004-03-03 type:feature owner:mattman bugzilla:394249,394252
Patch7:		gnome-panel-07-restrict-app-launching.diff
%if %option_with_indiana_branding
Patch8:         gnome-panel-08-launch-menu-indiana.diff
%endif
%if %option_with_sun_branding
# date:2006-05-03 type:branding owner:gman
Patch8:         gnome-panel-08-launch-menu.diff
# date:2006-09-21 type:branding owner:erwannc
Patch9:        gnome-panel-09-solaris-branding.diff
%endif
# date:2006-06-30 type:feature owner:stephen
Patch10:	gnome-panel-10-trusted-extensions.diff
# date:2004-03-03 type:feature owner:mattman bugzilla:397253
Patch11:        gnome-panel-11-lockdown-applets.diff
# date:2008-02-13 type:bug owner:dcarbery bugzilla:543291
Patch12:        gnome-panel-12-double-func.diff
# date:2008-08-28 type:branding owner:jedy
Patch13:        gnome-panel-13-tooltip.diff
# date:2008-09-04 type:bug owner:mattman bugzilla:537912 bugster:6702808
Patch14:        gnome-panel-14-hide-show-weather.diff
# date:2008-09-04 type:bug owner:mattman bugster:6702799
Patch15:        gnome-panel-15-use-time-admin.diff
# date:2009-04-03 type:bug owner:mattman doo:7280 bugzilla:577831
Patch16:        gnome-panel-16-set-default-location-crash.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/gnome-panel
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       GConf

%define libgnomeui_version 2.2.0
%define gnome_desktop_version 2.2.1
%define scrollkeeper_version 0.3.11
%define popt_version 1.6.4
%define gtk_doc_version 1.0
%define libwnck_version 2.2.1-2
%define libbonoboui_version 2.2.0
%define GConf_version 2.6.1
%define gnome_menus_version 2.10.0

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires: popt-devel >= %{popt_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: GConf >= %{GConf_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: intltool
BuildRequires: gnome-menus-devel >= %{gnome_menus_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      gnome-desktop >= %{gnome_desktop_version}
Requires:      libwnck >= %{libwnck_version}
Requires:      gnome-menus >= %{gnome_menus_version}

%description
This package contains the GNOME 2.0 Panel. The Panel is an easy to use and 
functional interface to manage your desktop, start programs and organize 
access to your data.

%package devel
Summary:      The GNOME Panel
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %{name} = %{version}
Requires:     GConf-devel >= %{GConf_version}
Requires:     libbonoboui-devel >= %{libbonoboui_version}

%description devel
This package contains the GNOME 2.0 Panel. The Panel is an easy to use and functional interface to manage your desktop, start programs and organize access to your data.


%prep
%setup -q
# bugster 6486542,6346647,6444413,6399297 bugzilla 404898,402399,411097
sh -x %SOURCE5 --disable-gnu-extensions

%if %option_with_sun_branding
%patch1 -p1
%endif
%if %option_with_indiana_branding
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%if %option_with_indiana_branding
%patch8 -p1
%endif
%if %option_with_sun_branding
%patch8 -p1
%patch9 -p1
%endif
%patch10 -p1
%patch11 -p1 
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

cp %SOURCE3 icons
cp %SOURCE6 icons
cp %SOURCE7 icons
%if %option_with_sun_branding
cp %SOURCE1 icons/gnome-main-menu.png
%endif

%if %build_l10n
bzcat %SOURCE4 | tar xf -
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

if ! [ -d m4 ]; then
  mkdir -p m4
fi

libtoolize --force
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE8 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --mandir=%{_mandir}	\
    --sysconfdir=%{_sysconfdir} \
    --disable-scrollkeeper \
    %{gtk_doc_option}

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
%ifos linux
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m 644 -D %SOURCE2 $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/gnome-time-settings
mv  $RPM_BUILD_ROOT%{_bindir}/gnome-time-settings $RPM_BUILD_ROOT%{_sbindir}/
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sf consolehelper gnome-time-settings)
%endif

rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

rm -rf $RPM_BUILD_ROOT/usr/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="panel-toplevel.schemas panel-object.schemas panel-global.schemas panel-general.schemas panel-compatibility.schemas clock.schemas workspace-switcher.schemas window-list.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries
gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE --load %{_sysconfdir}/gconf/schemas/panel-default-setup.entries /apps/panel/profiles/default

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/gnome-desktop-item-edit
%{_bindir}/gnome-panel
%{_bindir}/gnome-time-settings
%{_sbindir}/gnome-time-settings
%{_libexecdir}/*
%{_libdir}/libpanel-applet*.so.*
%{_libdir}/bonobo/servers
%{_datadir}/gnome-panelrc
%{_datadir}/gnome/help
%{_datadir}/gnome/panel
%{_datadir}/gnome/panel/glade
%{_datadir}/gnome-2.0/ui
%{_datadir}/gnome-time-settings/*
%{_datadir}/icons/hicolor/*
%{_datadir}/idl/*
%{_datadir}/omf/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_mandir}/man1/*
%{_sysconfdir}/security/console.apps/*
%{_sysconfdir}/gconf/schemas/*

%files devel
%defattr (-, root, root)
%{_bindir}/panel-test-applets
%{_includedir}/panel-2.0
%{_libdir}/libpanel-applet*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/panel-applet
%{_mandir}/man3/*

%changelog
* Fri Apr 03 2009 - matt.keenan@sun.com
- Fix d.o.o.:7280, add patch 16-set-default-location-crash.diff
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Wed Feb 18 2009 - matt.keenan@sun.com
- Bump to 2.25.91
* Thu Jan 29 2009 - matt.keenan@sun.com
- Bump to 2.25.5.1
- Remove 16-shutdownbutton.diff as bug fixed upstream
- Remove 17-clock-applet-location-crash.diff as bug fixed upstream
* Wed Jan 28 2009 - brian.cameron@sun.com
- Remove gnome-panel-13-add-libsocket.diff, no longer needed.
* Tue Jan 20 2009 - jedy.wang@sun.com
- Fix borken download link of gnome-panel.
* Tue Jan 13 2009 - matt.keenan@sun.com
- Bump to 2.25.3
- Remove obsolete patch gnome-panel-04-panel-applet-session-never-restart.diff
* Mon Nov 10 2008 - jedy.wang@sun.com
- Fix bugster:6769654, Clock applet crash when adding custom location.
* Fri Nov 07 2008 - matt.keenan@sun.com
- Actually apply patch 16-use-time-admin.diff, d.o.o.:4613
* Wed Nov 05 2008 - jedy.wang@sun.com
- Change the owner of  17-shutdownbutton.diff to jedy.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* The Sep 11 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Thu Sep 04 2008 - matt.keenan@sun.com
- Add patch 16-use-time-admin.diff, bugster:6702799, workaround PolicyKit
* Thu Sep 04 2008 - matt.keenan@sun.com
- Add patch 15-hide-show-weather.diff, bugzilla:537912 bugster:6702808
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 28 2008 - jedy.wang@sun.com
- Add 14-tooltip.diff
* Fri Aug 22 2008 - dave.lin@sun.com
- Bump to 2.23.90.1
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Mon Aug 18 2008 - matt.keenan@sun.com
- Remove obsolate patch 10-gnome-sys-suspend.diff
- Remove obsolate patch 12-noswitchuser.diff
- Remove obsolate patch 14-logout-keyboard-navigation.diff
- Renamed 11-trusted-extensions.diff -> 10-trusted-extensions.diff
- Renamed 13-lockdown-applets.diff -> 11-lockdown-applets.diff
- Renamed 15-double-func.diff -> 12-double-func.diff
- Renamed 19-add-libsocket.diff -> 13-add-libsocket.diff
* Mon Aug 18 2008 - matt.keenan@sun.com
- Re-appley patch 13-lockdown-applets.diff
* Wed Aug 06 2008 - matt.keenan@sun.com
- Bump to 2.23.6
- Remove gnome-panel-16-disable-lock-screen.diff : upstreamed
* Thu Jul 24 2008 - matt.keenan@sun.com
- Bump to 2.23.5
- Remove upstreaam patch-17-launcher-name-crash.diff
* Thu Jul 24 2008 - simon.zheng@sun.com
- Remove upstream patch 18-logout-shutdown-dialog.diff. 
  Already in 2.23.4. Please see bugzilla:507391.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Fri May 16 2008 - stephen.browne@sun.com
- remove conditional build of tx patch
* Wed May 14 2008 - dave.lin@sun.com
- Add patch  gnome-panel-19-add-libsocket.diff to fix build error
* Wed May 07 2008 - simon.zheng@sun.com
- Add patch 18-logout-shutdown-dialog.diff.
* Thu Apr 17 2008 - matt.keenan@sun.com
- Add patch 17-launcher-name-crash.diff fixes bugster:6690164 bugzilla:528581
* Wed Apr 16 2008 - damien.carbery@sun.com
- Bump to 2.22.1.3.
* Mon Apr 14 2008 - damien.carbery@sun.com
- Remove patch 15-fixclock - upstream code reworked to obsolete this patch.
  Renumber remainder.
* Fri Apr 11 2008 - damien.carbery@sun.com
- Bump to 2.22.1.2. Remove upstream patch 18-fixclockmap. Comment out patch15
  (15-fixclock) as clock code has been drastically changed.
* Wed Apr 09 2008 - brian.cameron@sun.com
- Add patch gnome-panel-18-fixclockmap to fix the map displayed by the
  clock applet so it is not corrupted.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Fri Mar 14 2008 - matt.keenan@sun.com
- Patch 17-disable-lock-screen CR 6675507
* Mon Mar 10 2008 - brian.cameron@sun.com
- Bump to 2.22.0
* Mon Mar 03 2008 - Michal.Pryc@Sun.Com
- Patch8 reworked for 2.21.91. CR 6668427
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Add patch 16-double-func to remove duplicate definition of
  panel_gconf_get_client().
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Thu Jan 31 2008 - brian.cameron@sun.com
- Add patch gnome-panel-15-fixclock.diff to fix crashing issue.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Mon Dec 10 2007 - matt.keenan@sun.com
- Add patch which fixes : bugster:6632252 bugzilla:342474
* Fri Nov 09 2007 - jedy.wang@sun.com
* Remove 14-support-alacarte.diff.
* Fri Nov 02 2007 - dave.lin@sun.com
- Fixed the problem with branding Patch1 definition
* Fri Oct 19 2007 - glynn.foster@sun.com
- disable Sun branding by default
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.6. Remove upstream patch, 10-clock-timezone. Renumber patch 15
  to patch 10 (gnome-sys-suspend).
* Wed Jul 11 2007 - damien.carbery@sun.com
- Reenable the TJDS patch (11-trusted-extensions). Remove the contents of the
  obsolete clock patch, but keep the file for a fix to #455921 (to avoid patch
  renaming).
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Wed Jun 20 2007 - matt.keenan@sun.com
- Re-work gnome-panel-10-clock-timezone patch again... for 2.19.4
* Tue Jun 12 2007 - matt.keenan@sun.com
- Re-work gnome-panel-10-clock-timezone patch, missing clock.h portion !!
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3. Remove upstream patches, 15-lXau and 17-name_max. Renumber
  remainder. Comment out patch10 (clock-timezone), asking owner to update.
* Fri May 18 2007 - matt.keenan@sun.com
- Re-Work gnome-panel-16-gnome-sys-suspend.diff after tarball update
* Tue May 15 2007 - damien.carbery@sun.com
- Add patch, 17-name_max, to use MAXNAMLEN on Solaris. Fixes 438637.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Fri Mar 09 2007 - takao.fujiwara@sun.com
- Add l10n-configure.sh to remove GNU extension from it.po, th.po and zh*.po
* Wed Feb 28 2007 - damien.carbery@sun.com
- Remove upstream patch, 16-keynav.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patches, 16-gok-grab-menu and 17-fixclock.
  Renumber rest.
* Thu Feb  8 2007 - damien.carbery@sun.com
- Reenable patch10 and zone_tab.sh script as they now apply correctly.
* Mon Jan 28 2007 - matt.keenan@sun.com
- Remove Patch18 - gnome-panel-16-preferences-menu.diff, seems to be upstream
* Sun Jan 28 2007 - laca@sun.com
- add %if %build_tjds guard around tjds patch so we can build without trusted
  jds support
* Thu Jan 24 2007 - damien.carbery@sun.com
- Unbump from 2.17.90 back to 2.16.2. UI spec needs to be updated before
  patches can be reworked.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90. Remove upstream patch, 16-preferences. Renumber remainder.
  Disable a few patches, asking owners to rework them.
* Tue Jan 16 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Dec 15 2006 - brian.cameron@sun.com
- Add patch gnome-panel-18-fixclock.diff to fix problem with clock 
  crashing when you click on it to see the calendar.  Problem is 
  that it was not linking against libedataserver-1.2.so.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Fri Nov 17 2006 - harry.lu@sun.com
- rework gnome-panel-14-support-alacarte.diff and enable it.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Oct 02 2006 - padraig.obriain@sun.com
- add patch 17-preferences-menu.diff for bug 6439133
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Thu Aug 30 2006 - damien.carbery@sun.com
- Remove reference to gnome-menu-stripe.png as it has been removed. Renumber
  the remaining 'Source?' items.
* Wed Aug 16 2006 - harry.lu@sun.com
- Add patch gnome-panel-15-support-alacarte.diff to fix 6460249.
* Thu Aug 10 2006 - matt.keenan@sun.com
- Reworking of lockdown patch 08, generating two patches
  08-restrict-app-launching.diff - specifically for restricting applications
  14-lockdown-applets.diff - Applet lockdown specifics that can be pushed 
  upstream
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Thu Jul 13 2006 - laca@sun.com
- remove patch ALL_LINGUAS.diff: fixed farther down the stack
* Thu Jul 13 2006 - brian.cameron@sun.com
- Add gnome-panel-14-noswitchuser.diff so that "Switch User" is not 
  an option on the Log Out menu, since this feature requires VT's to
  be supported and they aren't yet supported on Solaris.
* Thu Jul 13 2006 - laca@sun.com
- add patch ALL_LINGUAS.diff
* Wed May 03 2006 - glynn.foster@Sun.COM
- Add launch menu branding patch.
* Tue Apr 11 2006 - Cyrille.Moureaux@Sun.COM
- Added patch for application launching restriction.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 2.13.90
* Wed Jan 18 2006 - brian.cameron@sun.com
- Running glib-gettextize is a better fix than patching the Makefile to
  not go into the po directory.  This fixes infinite loop also.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Add intltoolize call. Add patch to fix infinite loop in configure.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Remove obsolete patch 03-egg-recent-poll. Renumber 12-launch-button to 03.
- Reenable patches 10 and 11 after rework.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Thu Jul 28 2005 - srirama.sharma@wipro.com
- Added gnome-panel-17-fix-logout-crash.diff to fix the panel crash 
  when recent items change. Don't unref menu in EggRecentViewGtk. 
  Also reuse the view till menu exists.
* Fri Jul 15 2005 - arvind.samptur@wipro.com
- Get Launch button to get rendered right 
* Thu Jun 30 2005 - balamurali.viswanathan@wipro.com
- Interchange patch 12 and 15 so that pkgconfig patch applies on both
  Linux and Solaris properly.
* Wed Jun 29 2005 - balamurali.viswanathan@wipro.com
- Add more libs to LDADD so that it builds with the new pkgconfig
* Wed May 25 2005 - brian.cameron@sun.com
- No longer create lib/conf.d since it is empty.
* Tue May 24 2005 - brian.cameron@sun.com
- Make patch 12 linux only since it requires patch 3 which is 
  linux only.
* Mon May 23 2005 - glynn.foster@sun.com
- Fix up a whole bunch, and reinstate the menu stripe patch.
* Fri May 13 2005 - brian.cameron@sun.com
- Bump to 2.10.
* Fri May 05 2005 - kieran.colfer@sun.com
- updating l10n po tarball to 1.15 (linux)
* Thu May 05 2005 - srirama.sharma@wipro.com
- Revised gnome-panel-06-time-settings.diff to show correct time
  in "Adjust System Date and Time" dialog. Fixes bug #6263488
* Thu May 05 2005 - arvind.samptur@wipro.com
- Revised gnome-panel-07-multi-timezones.diff to fix
  timezone button getting broked for second instance.
  Fixes #6236886
* Tue Apr 26 2005 - takao.fujiwara@sun.com
- Revised gnome-panel-38-g11n-i18n-filename.diff from community's reply
* Fri Apr 08 2005 - glynn.foster@sun.com
- Add some hicolor icons
* Mon Mar 14 2005 - takao.fujiwara@sun.com
- Removed gnome-panel-16-g11n-potfiles.diff to use l10n-configure.sh
- Removed gnome-panel-26-g11n-alllinguas.diff to use l10n-configure.sh
- Removed gnome-panel-27-g11n-potfiles.diff
- Added gnome-panel-38-g11n-i18n-filename.diff to fix 6239962 and 6239963
* Fri Mar 11 2005 - dermot.mccluskey@sun.com
- remove concurrent build from gnome-panel and this may have been
  causing intermittent intltool timestamp problems (6228015)
* Mon Feb 28 2005 - alvaro.lopez@sun.com
- Added patch gnome-panel-40-public_html.diff to bug bug #5032218:
  gnome-panel-screenshot has the uncorrect shortcut menu.
* Mon Feb 28 2005 - dinoop.thomas@wipro.com
- Added gnome-panel-39-notificationareatooltip.diff to add tooltip
  for panel notification area applet. Fixes bug #4912432.
* Sat Feb 26 2005 - dinoop.thomas@wipro.com
- Added gnome-panel-38-workspaceswitchertooltip.diff to add tooltip
  for workspace switcher applet. Fixes bug #6227329. 
* Fri Feb 11 2005 - srirama.sharma@wipro.com
- Added gnome-panel-37-resolve-vfb-magnification.diff to fix problem with
  panel properties when using VFB magnification. Fixes bug #6225051.
* Fri Feb 11 2005 - srirama.sharma@wipro.com
- Added gnome-panel-36-multihead-keyboard-shortcut.diff to see that 
  keyboard shortcuts are serviced on the proper screen on a multihead 
  machine. Fixes bug #4983400.
* Fri Feb 11 2005 - kieran.colfer@sun.com
- added gnome-panel-35-install-warning.diff to fix CR 6222796 (rpm
  gives warnings on install) 
* Fri Feb 11 2005 - muktha.narayan@wipro.com
- Added gnome-panel-34-run-dialog-atk-name.diff to set accessible name
  for the list of known applications. Fixes bug #6223576.
* Thu Feb 10 2005 - muktha.narayan@wipro.com
- Updated gnome-panel-31-theme.diff to fix the display problem
  of launch button.
* Fri Feb 04 2005 - glynn.foster@sun.com
- Fixed the run dialog to not default to trying an url if it
  doesn't have the correct prefix. Fixes #4897845.
* Tue Feb 01 2005 - dinoop.thomas@wipro.com
- Added gnome-panel-32-clock-applet-crash.diff patch to fix
  clock applet crash on clicking Edit Timezones after the applet
  is removed. Fixes bug #6222326.
* Mon Jan 31 2005 - matt.keenan@wipro.com
- #6222810 - Only install sun man pages
* Fri Jan 28 2005 - muktha.narayan@wipro.com
- Added gnome-panel-31-theme.diff to theme the panel icons.
  Fixes bug #5088581.
* Fri Jan 28 2005 - Matt.keenan@sun.com
- #6222302 - Remove fish from yelp
* Thu Jan 27 2005 - muktha.narayan@wipro.com
- Added gnome-panel-30-showdesktop-theme.diff to theme the show
  desktop icon. Fixes bug #6218867.
* Mon Jan 25 2005 - leena.gunda@wipro.com
- Modified gnome-panel-07-multi-timezones.diff to show correct time
  in the timezone selection dialog. Fixes bug #6218072
* Mon Jan 17 2005 - ghee.teo@sun.com
- Added gnome-panel-29-panel-applet-session-never-restart.diff to make sure
  that popup dialog from panel applets are not session aware, fixes bug
  6205402.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Mon Jan 03 2005 - srirama.sharma@wipro.com
- Added gnome-panel-28-delete-attached-panel.diff to allow user to delete an
  attached panel. Fixes Bug 6211650.
* Wed Dec 22 2004 - takao.fujiwara@sun.com
- Update gnome-panel-06-time-settings.diff and 
  gnome-panel-07-multi-timezones.diff to localize multi timezone. Fix bug 6210443
* Fri Nov 26 2004 - muktha.narayan@wipro.com
- Remove patch gnome-panel-28-icon-theming.diff.
* Fri Nov 12 2004 - hidetoshi.tajima@sun.com
- Created two panel-default-setup, one for linux the other for solaris
  as gnome-im-switcher is only on Linux (6193817)
- Rename patch-[03-27] to patch-[04-28]
* Tue Nov 09 2004 - muktha.narayan@wipro.com
- Added gnome-panel-27-icon-theming.diff to update panel menu icons
  with the icon theme change.
* Fri Nov 05 2004 - ciaran.mcdermott@sun.com
- Added gnome-panel-26-g11n-potfiles.diff to update POTFILES.in
* Thu Nov 03 2004 - kieran.colfer@sun.com
- added gnome-panel-25-g11n-alllinguas.diff to fix missing zh_HK 
  messages
* Fri Oct 29 2004 - leena.gunda@wipro.com
- added gnome-panel-24-applet-locked-key.diff to notify"locked" 
  key changes. Fixes bug #6181184.
* Fri Oct 29 2004 - arvind.samptur@wipro.com
- add patch in panel to get Launch menu items
  (help,this computer and find files) to have
  feedback when launched.
* Mon Oct 18 2004 - arvind.samptur@wipro.com
- add patch in panel to fix the conncurent login
  breakage between GNOME 2.0 and JDS for the panel
  configuration. Fixes #4984097
* Wed Oct 06 2004 - matt.keenan@sun.com
- re-do patch 20-l10n-online-help.diff and apply it #5108690
* Thu Sep 30 2004 - johan.steyn@sun.com
- Added patch to remove the fish applet.
  Also removed all other references to the fish applet.
* Fri Sep 10 2004 - vijaykumar.patwari@wipro.com
- Fixes the problem of panel hang, while setting gconf key value.
  Fixes bug #5083692.
* Thu Aug 26 2004 - damien.carbery@sun.com
- Integrated docs 0.6 tarball from breda.mccoglan@sun.com
- Use %ifos to apply different tarball for Linux and Solaris.
* Wed Aug 25 2004 - arvind.samptur@wipro.com
- Add gnome-panel-21-button-press.diff. Propogate
  button press event to PanelWidget
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs 0.5 tarball from breda.mccoglan@sun.com
* Thu Jul 22 2004 - padraig.obriain@sun.comn
- Added gnome-panel-19-create-menu.diff for bugzilla #138535.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-panel-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - damien.carbery@sun.com
- Integrated docs 0.4 tarball from breda.mccoglan@sun.com
 Thu Jun 10 2004 - kaushal.kumar@wipro.com
- Added gnome-panel-18-drawer-pref-help.diff to fix the drawer properties 
  help.
* Thu Jun 10 2004 - vijaykumar.patwari@wipro.com
- Fixes workspace switcher shows only one workspace.
* Tue Jun 09 2004 - glynn.foster@sun.com
- De-screwup the g11n-potfiles patches, so that now the linux only patches
  modify POTFILES.in as well. Need to be more careful with potfile hacking
  in the future.
* Sat Jun 05 2004 - damien.carbery@sun.com
- Temp comment out patch 18 as it fails and blocks building of other modules.
* Thu Jun 03 2004 - yuriy.kuznetsov@sun.com
- Added gnome-panel-18-g11n-potfiles.diff
* Tue Jun 01 2004 - yuriy.kuznetsov@sun.com
- Added gnome-panel-17-g11n-potfiles.diff
* Tue Jun 01 2004 - padraig.obriain@sun.com
- Added gnome-panel-16-accessible-name-sleep.diff for #5023382
* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Mon May 24 2004 - balamurali.viswanathan@wipro.com
- Added gnome-panel-15-screenshot-remove-sleep.diff, solves #5032203
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-panel-l10n-po-1.1.tar.bz2
* Wed May 12 2004 - laszlo.kovacs@sun.com
- change jds-help.sh to jdshelp
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1, remerge patch-02-default-setup & patch-09-lockdown
* Thu May 06 2004 - laszlo.kovacs@sun.com
- replace yelp with jds-help.sh in gnome-panel-03-menu-changes.diff and gnome-panel-09-lockdown.diff
* Thu Apr 29 2004 - glynn.foster@wipro.com
- Fix up panel menu changes, and merge the the search replace patch.
* Wed Apr 28 2004 - leena.gunda@wipro.com
- Added gnome-panel-14-check-fam-support.diff to check for FAM 
  support while updating the recent documents menu. Fixes bug 5027221.
* Tue Apr 27 2004 - kaushal.kumar@wipro.com
- Added gnome-panel-13-window-selector-tooltip.diff to provide a tooltip 
  for the Window Selector applet. Fixes bug 4912431.
* Tue Apr 27 2004 - kaushal.kumar@wipro.com
- Added gnome-panel-12-replace-search-menu-item.diff to replace 'Search' with 
  'Find Files' as per the Cinnabar specifications. Fixes bug 5035039.
* Tue Apr 27 2004 - kaushal.kumar@wipro.com
- Added gnome-panel-11-panel-menu-help.diff to fix panel context menu 
  help link.
* Tue Apr 27 2004 - arvind.samptur@wipro.com
- Added gnome-panel-10-drawer-multidepth.diff to fix problems when multi-depth
  drawers are opened
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Tue Apr 13 2004 - matt.keenan@sun.com
- Amend patch -03-menu-changes, remove the username from logout
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-panel-l10n-po-1.0.tar.bz2
* Fri Mar 26 2004 - takao.fujiwara@sun.com
- Updated gnome-panel-04-i18n-launch-button.diff to fix 5017372
* Fri Mar 26 2004 - laca@sun.com
- add --libexecdir to configure args
* Tue Mar 23 2004 - glynn.foster@sun.com
- Bump to 2.6.0, remove clock icon, add gnome-time-settings.app
  which seems to have disappeared :/
* Thu Mar 18 2004 - hidetoshi.tajima@sun.com
- Updated gnome-panel-02-default-setup.diff to add GIMLET
* Thu Mar 18 2004 - matt.keenan@sun.com
- Bump to 2.5.93, remove patch 09-remove-man
- Rename patch-14 to patch-09
* Fri Mar 05 2004 - takao.fujiwara@sun.com
- Added gnome-panel-13-g11n-i18n-ui.diff to fix 5004633
- Added gnome-panel-14-g11n-potfiles.diff
- Updated gnome-panel-02-default-setup.diff to fix 4991948
* Fri Mar 05 2004 - matt.keenan@sun.com
- Fix to lockdown patch for Menu Bars
* Wed Mar 03 2004 - matt.keenan@sun.com
- Added lockdown Patch ported from QS
* Tue Mar 02 2004 - matt.keenan@sun.com
- Bump to 2.5.91
- Re-apply patches 03 and 10
- Renabled patches 10 & 11 inside ifos check
* Sun Feb 29 2004 - laca@sun.com
- Disabled patches 10 & 11 because they break the build on Solaris
* Fri Feb 20 2004 - hidetoshi.tajima@sun.com
- Updated gnome-panel-02-default-setup.diff to add GIMLET
* Tue Feb 17 2004 - <matt.keenan@sun.com>
- Forwared ported patch 10 from QS
* Mon Feb 16 2004 - <matt.keenan@sun.com>
- Bumped to 2.5.4, re-applied all patches ....
* Fri Feb 06 2004 - <matt.keenan@sun.com>
- Updated l10n doc, and added OrigTree.pm fix
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- add patch 08 for intltool-merge and dep. on intltool
* Tue Dec 16 2003 - <glynn.foster@sun.com> 2.5.2-2
- Merge in the i18n launch button patch.
* Tue Dec 16 2003 - <glynn.foster@sun.com> 2.5.2-1
- Merge patches and update to 2.5.2
* Thu Nov 19 2003 - <glynn.foster@sun.com> 2.4.0-27
- Add patch for Browse Application on launch button
  context menu.
* Fri Nov 07 2003 - <markmc@sun.com> 2.4.0-24
- Fixed up help link in gnome-panel-preferences.
* Wed Nov 05 2003 - <glynn.foster@sun.com> 2.4.0-23
- Update default panel setup.
* Wed Nov 05 2003 - <glynn.foster@sun.com> 2.4.0-22
- Add 'Minimize' action button, and remove the Show
  Desktop stuff.
* Fri Oct 31 2003 - <glynn.foster@sun.com> 2.4.0-18
- Add 'Open Documents' to the top of the Open Recent
  menu.
* Fri Oct 31 2003 - <glynn.foster@sun.com> 2.4.0-17
- Remove the Extras menu.
* Wed Oct 08 2003 - <markmc@sun.com> 2.4.0-12
- Change the clock applet patch to unref the tree store
  and not destroy the tree view. I thought I'd done this
  as part of the changes in 2.4.0-3. Pointed out by
  Leena.
* Wed Oct 08 2003 - <markmc@sun.com> 2.4.0-11
- Add patch from George to make launchers on drawers work.
* Fri Sep 26 2003 - <laca@sun.com>
- Integrate Sun docs
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.0-5
- Add patch based on a patch from Bala to fix
  icon loading.
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.0-4
- Add patch from Arvind to fix bogus launchers
  getting added to drawers.
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.0-3
- Integrated three patches from Vijaykumar Patwari
  fixing various bugs with the clock applet timezone
  patch
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.0-2
- Install panel-compatibility.schemas
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.0-1
- Update to 2.4.0.
* Thu Aug 14 2003 - <laca@sun.com>
- use correct %{blahdir} tags instead of %{_prefix}/blah
- move lib*.so to -devel, remove *.a, *.la
* Fri Aug 08 2003 - <markmc@sun.com> 2.3.6.1-1
- Upgrade to 2.3.6.1.
* Fri Aug 08 2003 - <markmc@sun.com> 2.3.6-1
- Upgrade to 2.3.6.
* Thu Aug 07 2003 - <niall.power@sun.com> 2.3.4.1-10
- Make scrollkeeper a standard requirement 
  instead of just being a build requirement.
* Wed Aug 06 2003 - <markmc@sun.com> 2.3.4.1-9
- Fix some serious memory stomping crackrock in
  the clock applet patch.
* Tue Aug 05 2003 - <glynn.foster@sun.com>
- Add missing .desktop file.
* Wed Jul 30 2003 - <markmc@sun.com>
- Fix crashing when adding clock applet.
* Mon Jul 28 2003 - <glynn.foster@sun.com>
- Merge together clock applet patches and fix crashing
* Thu Jul 24 2003 - <glynn.foster@sun.com>
- New default panel setup.
* Thu Jul 24 2003 - <markmc@sun.com>
- update to 2.3.4.1
* Tue Jul 22 2003 - <glynn.foster@sun.com>
- Update title to reflect menu entry.
* Tue Jul 22 2003 - <glynn.foster@sun.com>
- New Action icon for context menu.
* Tue Jul 22 2003 - <glynn.foster@sun.com>
- Add a new clock icon for the applet.
* Mon Jul 21 2003 - <glynn.foster@sun.com>
- Update menu changes to include quick-start:///
  uri thing. Mostly on crack.
* Mon Jul 21 2003 - <matt.keenan@sun.com>
- clock applet show city preference patch
* Fri Jul 18 2003 - <glynn.foster@sun.com>
- Install the png, instead of copying it.
* Fri Jul 18 2003 - <glynn.foster@sun.com>
- Update menu layout, and revise fix icons patch.
* Fri Jul 18 2003 - <glynn.foster@sun.com>
- Update default setup to move workspace switcher 
  to the far right.
* Fri Jul 18 2003 - <glynn.foster@sun.com>
- Change Applications and Help icon in the menu
* Thu Jul 17 2003 - <markmc@sun.com>
- Add back the launch button.
* Thu Jul 17 2003 - <glynn.foster@sun.com>
- Add patch to change pixmap installation location
* Tue Jul 16 2003 - <markmc@sun.com>
- Add patch to fix icon warnings.
* Tue Jul 15 2003 - <markmc@sun.com>
- Move to 2.3.4.
* Mon Jul 14 2003 - <markmc@sun.com>
- Add patch to normalise the applet size to the
  values defined in the IDL.
* Mon Jul 14 2003 - <markmc@sun.com>
- Make gnome-panel-screenshot save screenshots to
  ~/.gnome-desktop instead of ~/Desktop.
* Thu Jul 10 2003 - <glynn.foster@sun.com>
- Remove the notification area from the default
  panel setup.
* Thu Jul 10 2003 - <glynn.foster@sun.com>
- Clock applet only shows time by default.
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Fri Jul 09 2003 - <markmc@sun.com>
- fix theming in menu stripe patch. 
* Fri Jul 08 2003 - <markmc@sun.com>
- removed "Adjust Date and Time" from the clock applets
  popup menu. There is no nice time adjustment tool
  on SuSE.
* Fri Jul 04 2003 - <markmc@sun.com>
- Fixed stripe patch so events over the sripe go
  to the menu item.
* Thu Jul 03 2003 - <markmc@sun.com>
- Changed the main menu icon to the launch button
* Thu Jul 03 2003 - <markmc@sun.com>
- Remove quicklounge from the default setup patch rather
  than patching the patch
* Thu Jul 03 2003 - <markmc@sun.com>
- Bump release - new version of menu stripe patch
  and merged changes into the menu layout patch.
* Thu Jul 03 2003 - <ghee.teo@sun.com>
- Remove quick lounge from panel with patch
  gnome-panel-08-remove-quick-lounge.diff
* Wed Jul 02 2003 - <markmc@sun.com>
- use the correct menu stripe image filename
* Wed Jul 02 2003 - <markmc@sun.com>
- Make the main menu icon seperate from the GNOME
  logo so we can theme them seperately
- Fixed icons in share/icons not getting installed
* Wed Jul 02 2003 - <markmc@sun.com>
- Update to gnome-panel-2.3.3.3
* Tue Jul 01 2003 - <markmc@sun.com>
- Update to gnome-panel-2.3.3.2
- Remove gnome-panel-06-fix-lock-logout-button-crashing.diff
- Remove gnome-panel-07-install-defaults.diff
- Update gnome-panel-03-menu-changes.diff, gnome-panel-02-default-setup.diff
  and gnome-panel-04-change-required-versions.diff.
- Fix gnome-panel-08-clock-applet.diff
* Thu Jun 12 2003 - <markmc@sun.com>
- add patch to install panel-default-setup.entries
- fix post-install of default entries
* Fri May 30 2003 - <markmc@sun.com>
- Move to gnome-panel-2.3.x
* Tue May 13 2003 - <ghee.teo@sun.com>
- initial release for gnome-panel
