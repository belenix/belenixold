#
# spec file for package gnome-session
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
%include l10n.inc
Name:         gnome-session
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      3
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Session Manager for the GNOME Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %option_with_sun_branding
Source1:      gnome-splash.png
%endif
Source2:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source3:                 l10n-configure.sh
%endif
Source4:      indiana-splash.jpg
Source5:      http://dlc.sun.com/osol/jds/downloads/extras/compiz/compiz-session-integration-6.4.tar.bz2
#owner:gheet date:2004-08-06 type:bug bugster:5025823
Patch1:       gnome-session-01-gnome-atom.diff
%if %option_with_sun_branding
#owner:yippi date:2004-11-04 type:branding
Patch2:       gnome-session-02-gnome-about.diff
%endif
#owner:stephen date:2006-06-29 type:feature bugster:6444179
Patch3:       gnome-session-03-wait-for-postrun.diff
#owner:erwannc date:2003-07-29 type:branding
Patch4:       gnome-session-04-busy-cursor.diff
%if %option_with_sun_branding
#owner:erwannc date:2005-05-11 type:branding
Patch5:       gnome-session-05-solaris-branding.diff
%endif
#owner:erwannc date:2008-03-27 type:branding
Patch6:      gnome-session-06-indiana-splash-hack.diff
#owner:jedy date:2008-06-23 type:feature
Patch7:      gnome-session-07-logout-dialog.diff
#owner:gheet date:2006-11-03 type:feature bugster:6393728
Patch8:     gnome-session-08-trusted-extensions.diff
#owner:gheet date:2008-08-15 type:branding
Patch9:     gnome-session-09-null-string.diff
%if %option_with_sun_branding
#owner:gheet date:2008-09-03 type:branding bugster:6743662
Patch10:     gnome-session-10-show-splash.diff
%endif
#owner:gheet date:2009-02-12 type:bug bugzilla:6538
Patch11:     gnome-session-11-null-dbus-path.diff
#owner:mattman date:2009-02-03 type:feature bugster:6767905
Patch12:     gnome-session-12-compiz-by-default.diff
#owner:gheet date:2008-03-13 type:branding bugster:6753114
Patch13:     gnome-session-13-access-save-session.diff
#owner:gheet date:2009-03-13 type:branding bugzilla:7289
Patch14:     gnome-session-14-bad-clients.diff
#owner:gheet date:2009-04-07 type:branding bugster:6753114
Patch15:     gnome-session-15-reenable-session.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf

%define libgnomeui_version 2.2.0
%define libwnck_version 2.2.1

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: libwnck >= %{libwnck_version}

%description
This package provides the basic session manager and tools for the GNOME Desktop.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif
gtar fxvj %{SOURCE5}
%patch1 -p1
%if %option_with_sun_branding
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%if %option_with_sun_branding
%patch5 -p1
cp %SOURCE1 data/gnome-splash.png
%endif
%if %option_with_indiana_branding
cp %SOURCE4 data/gnome-splash.png
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p1
%patch9 -p1
%if %option_with_sun_branding
%patch10 -p1
%endif
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

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

%ifos solaris
%define poweroff /usr/sbin/poweroff
%define reboot   /usr/sbin/reboot
%else
%define poweroff /usr/bin/poweroff
%define reboot   /usr/bin/reboot
%endif

libtoolize --force
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"		\
./configure --prefix=%{_prefix}				\
	    --libexecdir=%{_libexecdir}			\
	    --sysconfdir=%{_sysconfdir} 		\
	    --mandir=%{_mandir}				\
	    --with-halt-command=%poweroff	\
	    --with-reboot-command=%reboot
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp compiz-by-default.desktop $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp compiz-by-default $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-session.schemas"
for S in $SCHEMAS; do
	gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/gnome/default.session
%{_datadir}/gnome/default.wm
%{_datadir}/applications/
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/compiz-by-default

%changelog
* Wed Apr 08 2009 - ghee.teo@sun.com
- Added gnome-session-15-reenable-session.diff to re-enable a last minute
  changes made in the community that disable session saving.
* Fri Mar 20 2009 - matt.keenan@sun.com
- Bump compiz-session-integration tarball to 6.4 fix #7370
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - ghee.teo@sun.com
- Added two new patches to allow gnome-session-save and click to save session
- gnome-session-13-access-save-session.diff (This patch is upstremable)
- gnome-session-14-bad-clients.diff (This is a distro specific patch for now)
* Wed Mar 11 2009 - matt.keenan@sun.com
- Bump compiz-session-integration tarball to 6.3 fix #7287
* Mon Mar 09 2009 - ghee.teo@sun.com
- Uprev tarball to 2.25.92 and reordered all patches sequentially.
* Fri Feb 27 2009 - matt.keenan@sun.com
- Bump compiz-session-integration tarball to 6.2 fix #6967
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
- Reworked patch 10-trusted-extensions.diff.
- Removed upstreamed patch 17-exit-avoid-restart.diff.
- Removed upstreamed patch 11-menu-entry.diff.
* Thu Feb 12 2009 - takao.fujiwara@sun.com
- Remove patch Xsession-dtstart.diff and Xsession.diff.
  Now gnome-session is invoked directly and loads /etc/X11/xinit/xinitrc.d
* Wed Feb 11 2009 - matt.keenan@sun.com
- Integrate compiz-session-integration tarball for compiz-by-default
* Tue Feb 03 2009 - matt.keenan@sun.com
- Add 18-compiz-by-default.diff to enable compiz by default
* Mon Jan 26 2009 - matt.keenan@sun.com
- Bump to 2.25.5
- Remove upstreamed patch 14-autostart.diff
- Remove upstreamed patch 16-stop-ice-negotiation.diff
* Fri Jan 23 2009 - brian.cameron@sun.com
- Add patch gnome-session-17-exit-no-restart.diff to ensure that programs do
  not restart when gnome-session is killed.  This makes the new GDM rewrite
  work much better.
* Mon Jan 19 2009 - ghee.teo@sun.com
- Bump to 2.25.3
- Added gnome-session-16-stop-ice-negotiation as code has not released as tarball yet.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Nov 05 2008 - jedy.wang@sun.com
- Change the owner of 09-logout-dialog.diff to jedy.
* Mon Oct 20 2008 - ghee.teo@sun.com
- Added gnome-session-15-hide-preference-options.diff #6761428 created by MattK.
* Thu Oct 09 2008 - halton.huo@sun.com
- Add patch autostart.diff to fix bugster #6756344, bugzilla #555369
* Mon Sep 29 2008 - ghee.teo@sun.com
- Bump to 2.24.0 - reworked gnome-session-10-trusted-extensions.diff
* Thu Sep 11 2008 - jedy.wang@sun.com
- Do not apply show-splash for OpenSolaris.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92, rework gnome-session-07-compiz-integration.diff
* Thu Sep 04 2008 - ghee.teo@sun.com
- Removed 13-desktop-id.diff which has been implemented differently upstream.
  gnome-session-14-restart-app.diff which was taken from upstream..
* Wed Sep 03 2008 - ghee.teo@sun.com
- Added gnome-session-15-show-splash.diff, a brnading patch to enable splash.
  Also corrected indiana splash screen location.
* Mon Sep 01 2008 - ghee.teo@sun.com
- Added gnome-session-14-restart-app.diff. A patch taken from trunk which 
  should be removed when the trunk code is released as tarball.
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Fri Aug 15 2008 - ghee.teo@un.com
- Added patch gnome-session-15-null-string.diff. This is a Solaris thing.
  Hopefully though when PSARC/2008/403 is integrated, we will not need patches like this.
* Thu Aug 14 2008 - ghee.teo@sun.com
- Added patch gnome-session-13-gconf-schema.diff which stop metacity
  from starting up due to typo in gconf key. It is in trunk. so have not
  bug id for it.
* Wed Aug 13 2008 - erwann@sun.com
- Bumped to 2.23.6
- ported my patches included Ghee's one and commented out the others.
* Mon Aug 04 2008 - brian.cameron@sun.com
- Bump to 2.23.5.
* Wed Jul 23 2008 - matt.keenan@sun.com
- Remove man5 from %files, default.session.5 removed from gnome-session
* Mon Jul 14 2008 - jedy.wang@sun.com
- Add 12-desktop.diff.
* Wed Jul 02 2008 - niall.power@sun.com
- Collapse patch numbers. Remove logout-effect.diff
* Mon Jun 23 2008 - simon.zheng@sun.com
- Add 15-logout-dialog.diff. Use gpm dbus interface to 
  reboot/shutdown due to ConsoleKit is unavailable.
* Thu Jun 19 2008 - brian.cameron@sun.com
- Re-enable gnome-session-03-gnome-about.diff patch.  Add new patch
  gnome-session-14-fixcrash.diff to fix crashing issue when gnome-session
  starts.  Bugzilla bug #539187.
* Thu Jun 19 2008 - niall.power@sun.com
  -10-disable-ssh.diff: Dropped since ssh is supported in gnome-session
  now.
* Thu Jun 19 2008 - niall.power@sun.com
- Bump to 2.23.4 community tarball.
  Dropped patches: 
  -06-gnome-volcheck... No longer ship gnome-volcheck
  -09-find-dbus-daemon  Launches dbus-launch now instead of dbus-daemon
  Commented out patches that don't apply to new sources.
* Thu Jun 12 2008 - takao.fujiwara@sun.com
- Add po-logout to avoid UI freeze.
* Fri Jun 06 2008 - simon.zheng@sun.com
- Remove 13-logout-shutdown-dialog.diff and 14-
* Sat May 31 2008 - brian.cameron@sun.com
- Add patch so that the "Switch User" button does not show up on
  Solaris.  Fixes bugzilla:535892.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed May 07 2008 - simon.zheng@sun.com
- Add patch 13-logout-shutdown-dialog.
* Fri Apr 11 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Fri Mar 07 2008 - damien.carbery@sun.com
- Bump to 2.21.93.
* Fri Feb 29 2008 - brian.cameron@sun.com
- When building with DT (CDE login), then make sure the gnome.desktop 
  file calls /usr/dt/bin/Xsession.jds rather than gnome-session.
* Fri Feb 29 2008 - jeff.cai@sun.com
- Bump to 2.21.92. Add patch 10-disable-ssh to revert patch #503278. This
  removes the gnome-session dependency on gnome-keyring.
* Thu Feb 28 2008 - damien.carbery@sun.com
- Revert to 2.21.91 because 2.21.92 requires a new version of gnome-keyring,
  which breaks.
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Remove upstream patch 10-gsd-header-dir.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Feb 05 2008 - damien.carbery@sun.com
- Add patch 10-gsd-header-dir to work with change in gnome-settings-daemon.
  Bugzilla 511820.
* Tue Jan 29 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2007 - brian.cameron@sun.com
- Remove patch gnome-session-09-fixdbus.diff.  No longer needed
  now that we use D-Bus 1.1.3.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Jan 08 2007 - brian.cameron@sun.com
- Add patch 9 and 10 to allow gnome-session to launch D-Bus.
* Tue Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.20.3.
* Fri Oct 19 2007 - laca@sun.com
- only display gnome-about on 1st login if --with-sun-branding is used
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Fri Oct 12 2007 - laca@sun.com
- always apply the tjds patch even if --with-tjds is not used, otherwise
  some patches that follow it fail and it doesn't hurt anyway
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Tue Jul 17 2007 - ghee.teo@sun.com
- Remove gnome-session-04-purge-warn-delay.diff
  after sun patch day review.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.4. Remove upstream patch, 08-fixtime.
* Wed Jun 06 2007 - irene.huang@sun.com
- %if %with_hal then do not apply patch7, volcheck.diff
  so that this patch will not be applied when HAL is enabled. Also modify
  the source path so that the source can be found.
* Tue Jun 05 2007 - brian.cameron@sun.com
- Bump to 2.19.3
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Thu Feb 01 2007 - damien.carbery@sun.com
- Remove upstream patch, 08-lXau; renumber remainder.
* Sun Jan 28 2007 - laca@sun.com
- add %if %build_tjds guard around tjds patch so we can build without trusted
  jds support
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.1.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Sat Dec 30 2006 - li.yuan@sun.com
- Add gnome-session-11-remove-filter.diff to fix bugzilla #390882. 
  Remove filter when it is not needed.
* Fri Dec 15 2006 - li.yuan@sun.com
- Add libexecdir option to configure to make gnome-session know 
  where the at-spi-registryd is.
* Sun Dec 03 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Fri Nov 03 2006 - ghee.teo@sun.com
- Fixed up gnome-session-09-trusted-extensions.diff for 2.16
* Tue Oct 31 2006 - takao.fujiwara@sun.com
- Added intltoolize to read LINGAS file. Fixes 6488189.
* Mon Oct 30 2006 - irene.huang@sun.com
- add patch gnome-session-10-gnome-volcheck-default-session.diff
  which is orignally 
  Solaris/patches/gnome-session-01-gnome-volcheck-default-session.diff
* Mon Oct 23 2006 - glynn.foster@sun.com
- Fix up fuzziness of the gnome-session patches. Merge the logout
  effect patches together, remove the non-existant a11y patch, and
  comment out the broken trusted extensions patch.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Fri Aug 25 2006 - damien.carbery@sun.com
- Add patch, 12-lXau, to link libXau in.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
- Remove upstream patch, 10-fixcrash, renumber remainder.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Fri Jul 28 2006 - brian.cameron@sun.com
- Move gnome-session-07-gnome-volcheck-default-session.diff to 
  Solaris/patches so we can only apply this if HAL package is
  installed.
* Fri Jul 28 2006 - dermot.mccluskey@sun.com
- Fix minor typo.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Mon Jul 24 2006 - padraig.obriain@sun.com
- Bump to 2.15.4.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.2.
* Fri May 05 2006 - brian.cameron@sun.com
- Add patch to fix crash when HAL is enabled, caused by printing of a NULL
  string.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Thu Mar  9 2006 - damien.carbery@sun.com
- Add patch, 10-G_DEBUG-off, to not set G_DEBUG=fatal_criticals as it exposes
  a lot of crashes in Evolution.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
- Remove unneeded glib-gettextize and intltoolize calls.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 2.13.90
* Sun Jan 22 2006 - damien.carbery@sun.com
- Call intltoolize and glib-gettextize to avoid infinite loop.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.5.
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri Aug 05 2005 - glynn.foster@sun.com
- Merge the 2 splashes into one. Remove the linux splash branding patch
  to focus on one for the moment - we can bring it back later if need
  be.
* Tue Jun 14 2005 - bill.haneman@sun.com
- Set GNOME_DISABLE_CRASH_DIALOG to '1', not 'true', for
  bug #6273175.  (Previous patch set it to 'true', which failed to work).
* Fri May 20 2005 - bill.haneman@sun.com
- Edit gnome-session-09-load-a11y-modules.diff to set 
  GNOME_DISABLE_CRASH_DIALOG when a11y is on, fix for bug #6273175.
* Wed May 11 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.0
* Wed Jan 23 2005 - arvind.samptur@wipro.com
- Edit patch gnome-session-09-load-a11y-modules.diff to set
  the GTK_MODULES env before gnome_program_init (). This way
  b-a-s will get this env and will pass it on to all the factories
  that it would spawn.
* Fri Jan 21 2005 - bill.haneman@sun.com
- Edited patch gnome-session-09-load-a11y-modules.diff to fix bug
  6202413.  We now putenv("NO_J2D_DGA=true") when a11y is enabled,
  and the env variable isnt already set.
* Thu Jan 14 2005 - ghee.teo@sun.com
- Reduce the purge_delay and warn_delay to 30seconds which essentially
  revert back the bugzilla#94754. This patch is to partially fix bq2 
  #4978659. The Mozilla team has fixed the mozilla side of the problem by
  5068301, however, reducing this timeouts will benefit other badly broken
  session apps. 
* Mon Jan 10 2005 - kieran.colfer@sun.com
- changing date on previous changelog entry - was causing rpmbuild
  to fail with "%changelog not in descending chronological order" :-)
* Mon Jan 03 2005 - arvind.samptur@wipro.com
- Now that gnome-settings-daemon starts per display, the
  patch gnome-session-07-sunray-screensaver.diff should not
  be required. Corresponding g-s-d patch is
  control-center-27-settings-daemon-per-display.diff
* Thu Nov 12 2004 - alvaro.lopez@sun.com
- Added patch #12.  It fixes #5099423
* Thu Nov 10 2004 - alvaro.lopez@sun.com
- Source header fixed.
* Wed Nov 10 2004 - leena.gunda@wipro.com
- Added patch gnome-session-11-gnome-volcheck-default-session.diff
  to start gnome-volcheck for Solaris.
* Thu Nov 04 2004 - brian.cameron@sun.com
- Added patch 10 so that gnome-about launches on first-time login. 
* Fri Oct 29 2004 - laca@sun.com
- Add gnome-session-remove.1 man page to %files
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gnome-session-remove.1 man page
* Thu Oct 28 2004 - muktha.narayan@wipro.com
- Load the a11y libraries by setting the GTK_MODULES env variable.
  Fixes issues addressed in bug #5097456.
* Sat Sep 11 2004 - laca@sun.com
- Move Solaris specific LDFLAGS to the Solaris spec file
* Fri Sep 10 2004 - damien.carbery@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Fri Aug 13 2004 - ghee.teo@sun.com
- Forward ported sun-patches/gnome-session/560-4780014-s.diff 
  as gnome-session-07-sunray-screensaver.diff. This is a security fix but
  really only affects Sunray.
* Tue Aug 10 2004 - matt.keenan@sun.com
- Bug:5084286, forward ported patch from mercury for logout effect.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-session-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 09 2004 - ghee.teo@sun.com
- do not compile patch1 on Solaris as it is a linux only patch.
  so use ifos linux to compile in
  gnome-session-01-magicdev-default-session.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-session-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - <matt.keenan@sun.com>
- Bump to 2.6.1.
* Tue Apr 06 2004 - arvind.samptur@wipro.com
- Add patch to create an atom for legacy X apps to determine
  if they are running currently under GNOME
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-session-l10n-po-1.0.tar.bz2
* Tue Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 2.6.0. Remove man page and logout effect. Seems like
  a not hugely useful branding patch that it might be good to 
  remove. 
* Tue Feb 24 2004 - <glynn.foster@sun.com>
- Bump to 2.5.90
* Fri Dec 15 2003 - <glynn.foster@sun.com>
- Bump to 2.5.2
* Wed Aug 06 2003 - <glynn.foster@sun.com>
- Remove splash icons for non-important apps
* Wed Jul 30 2003 - <markmc@sun.com>
- Add magicdev correctly
* Mon Jul 21 2003 - <markmc@sun.com>
- Make it use the consolehelper versions of reboot and poweroff.
* Fri Jul 11 2003 - <matt.keenan@sun.com>
- Add patch for logout effect
* Thu Jul 10 2003 - <glynn.foster@sun.com>
- Add an icon to the splash widget.
* Thu Jul 10 2003 - <glynn.foster@sun.com>
- Add magicdev to the default session.
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Mon Jun 30 2003 - <markmc@sun.com>
- run autoheader so config.h contains gets HAVE_RANDR
* Mon Jun 30 2003 - <markmc@sun.com>
- add display properties restoration patch
- copy the splash screen into the build tree in
  %prep rather than manually installing it in %install
* Tue May 13 2003 - <ghee.teo@Sun.COM>
- Created new spec file for gnome-session
