#
# spec file for package gnome-power-manager
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#

%include l10n.inc
Name:           gnome-power-manager
License:        GPL
Group:		X11/Applications
#### DO NOT BUMP MODULE TO 2.24.x to 2.25.x AS IT DEPENDS ON DEVICEKIT-POWER
#### NOT YET READY FOR SOLARIS
Version:        2.24.4
Release:        2
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:	GNOME Power Manager
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-power-manager/2.24/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:        l10n-configure.sh
Source2:        %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
# date:2008-02-14 owner:jedy type:feature
Patch1:        gnome-power-manager-01-build.diff
# date:2008-06-06 owner:jedy type:feature
Patch2:        gnome-power-manager-02-icon_plicy.diff
# date:2008-02-14 owner:jedy type:feature
Patch3:        gnome-power-manager-03-disable-sleep-configration.diff
# date:2008-04-06 owner:jedy type:feature
Patch4:        gnome-power-manager-04-authorization.diff
# date:2008-06-06 owner:jedy type:feature
Patch5:        gnome-power-manager-05-disable-suspend-button.diff
# date:2008-02-14 bugzilla:507391 owner:jedy type:bug
Patch6:        gnome-power-manager-06-interactive-dialog.diff
# date:2008-02-14 owner:jedy type:feature
Patch7:        gnome-power-manager-07-screensaver.diff
# date:2008-09-19 bugster:6750001 owner:jedy type:feature
Patch8:        gnome-power-manager-08-cpufreq.diff
# date:2008-09-11 owner:jedy type:branding
Patch9:        gnome-power-manager-09-menu-entry.diff
# date:2009-03-02 owner:jedy type:branding
Patch10:       gnome-power-manager-10-no-console-kit.diff
# date:2009-03-24 doo:7356 owner:jedy type:bug
Patch11:       gnome-power-manager-11-no-dpms-sync.diff
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-keyring-devel >= 0.8
BuildRequires:	gnome-panel-devel >= 2.18.0
BuildRequires:	gtk+2-devel >= 1:2.10.10
BuildRequires:	hal-devel >= 0.5.7.1
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libglade2-devel >= 2.6.0
BuildRequires:	libgnomeui-devel >= 2.18.0
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libtool
BuildRequires:	libwnck-devel >= 2.18.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
Requires:	GConf2
Requires:	gtk+2
Requires:	hicolor-icon-theme
Requires:	scrollkeeper
Requires:	gnome-session >= 2.18.0
Requires:	notification-daemon >= 0.3.5
Obsoletes:	gnome-power
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uses of GNOME Power Manager infrastructure
- A dialogue that warns the user when on UPS power, that automatically
  begins a kind shutdown when the power gets critically low.
- An icon that allows a user to dim the LCD screen with a slider, and
  does do automatically when going from mains to battery power on a
  laptop.
- An icon, that when an additional battery is inserted, updates it's
  display to show two batteries and recalculates how much time
  remaining. Would work for wireless mouse and keyboards, UPS's and
  PDA's.
- A daemon that does a clean shutdown when the battery is critically
  low or does a soft-suspend when you close the lid on your laptop (or
  press the "suspend" button on your PC).
- Tell Totem to use a codec that does low quality processing to
  conserve battery power.
- Postpone indexing of databases (e.g. up2date) or other heavy
  operations until on mains power.
- Presentation programs / movie players don't want the screensaver
  starting or screen blanking.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p1
%patch10 -p1
%patch11 -p1

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

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
intltoolize --force
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I .

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
	    --enable-policykit			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
            --disable-scrollkeeper
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
	
%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install gnome-power-manager.schemas
%preun
%gconf_schema_uninstall gnome-power-manager.schemas

%postun
%scrollkeeper_update_postun

%files
%defattr(-,root,root)
%{_libdir}/bonobo/servers/GNOME_BrightnessApplet.server
%{_libdir}/bonobo/servers/GNOME_InhibitApplet.server
%{_datadir}/gnome/autostart/gnome-power-manager.desktop
%{_datadir}/dbus-1/services/gnome-power-manager.service
%{_datadir}/gnome-2.0/ui/GNOME_BrightnessApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_InhibitApplet.xml
%{_mandir}/man1/*.1*
%{_datadir}/gnome-power-manager/*
%{_sysconfdir}/gconf/schemas/gnome-power-manager.schemas


%changelog
* Tue Mar 24 2008 - jedy.wang@sun.com
- Add 11-no-dpms-sync.diff.
* Mon Feb 11 2008 - jedy.wang@sun.com
- Bump to 2.24.4.
- Remove 10-brightness-progressbar.diff. The bug has been fixed in the
  community.
- Add 10-no-console-kit.diff to disable console kit on Solaris.
* Mon Jan 19 2008 - jedy.wang@sun.com
- Bump to 2.24.3.
- Remove patch 11-no-daemon.diff.
* Wed Dec 03 2008 - jedy.wang@sun.com
- Bump to 2.24.2.
* Fri Nov 28 2008 - jedy.wang@sun.com
- Bump to 2.24.1.
* Tue Nov 25 2008 - jedy.wang@sun.com
- Add "do not bump" comments.
* Wed Oct 29 2008 - jedy.wang@sun.com
- Update patch owner.
* Thu Oct 16 2008 - jedy.wang@sun.com
- Update patch comment.
* Tue Oct 14 2008 - jedy.wang@sun.com
- Add 11-no-daemon.diff to fix doo 2929.
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Sep 23 2008 - simon.zheng@sun.com
- Bump to 2.24.0.
* Fri Sep 19 2008 - simon.zheng@sun.com
- Rework 07-screensaver.diff to fix bugster #6750004.
- Add 10-brightness-progressbar.diff to fix bugzilla #552762.
* Tue Sep 16 2008 - simon.zheng@sun.com
- Rework 08-cpufreq.diff to configure cpufreq policy.
* Thu Sep 11 2008 - jedy.wang@sun.com
- Rename 09-disable-statis-menuitem.diff to 09-menu-entry.diff and set owner to
  jedy.
* Tue Sep 02 2008 - simon.zheng@sun.com
- Bump to 2.23.91.
- Rework 01-build.diff and 04-authorization.diff.
* Thu Aug 07 2008 - simon.zheng@sun.com
- Bump to 2.23.6. 
- Rework 01-build.diff.
- Rework 04-authorization.diff
- Rework 07-screensaver.diff.
- Removed upstream patch 09-xrandr.diff.
* Wed Aug 06 2008- simon.zheng@sun.com
- Add patch 09-xrandr.diff to fix unable to startup on Sparc Solaris.
* Wed Jul 02 2008 - simon.zheng@sun.com
- Bump to 2.23.3.
- Remove upstream 10-kstat-cpu.diff.
* Fri Jun 06 2008 - simon.zheng@sun.com
- Rework 02-gnome-power-manager-02-icon_plicy.diff.
* Wed Jun 04 2008 - simon.zheng@sun.com
- Rework 03-disable-sleep-configration.diff
- Rework 05-diable-suspend-button-configration.diff
- Rework 09-authorization.diff:
* Tue Jun 03 2008 - simon.zheng@sun.com
- Bump to 2.23.1, change intloolize and aclocal arguments.  
- Remove upstream patch 04-scripts.diff. 
- Rework 01-build.diff 
- Rework 07-screensaver.diff. 
- Disable some patches for the time being. Need further work. 
* Fri May 23 2008 - laca@sun.com
- disable gconf schema install during make install to get rid of tons
  of warning.  Also delete extra \ at the end of the make install line
* Sun May 18 2008 - simon.zheng@sun.com
- Add patch 10-kstat-cpu.diff because accuracy calculation
  needs cpu load.
* Wed May 07 2008 - simon.zheng@sun.com
- Rework patch 06-interactive-dialog.diff.
* Fri Apr 04 2008 - simon.zheng@sun.com
- Rework 14-authorization-checking.diff as 09-authorization.diff.
  Check cpu, brightness, shutdown, root, suspend, hibernate 
  libpolkit auths.
- Build with option --enable-policykit.
* Sat Mar 29 2008 - simon.zheng@sun.com
- Bump to 2.22.1. 
- Remove upstream patch 10-disable-lid-beeping.diff.
* Thu Mar 27 2008 - simon.zheng@sun.com
- Rework 07-screensaver.diff. Add keyboard and point
  grab checking and use xdg-screensaver instead of
  xscreensaver.
* Fri Mar 14 2008 - simon.zheng@sun.com
- Add 08-sync-cpufreq.diff to only allow user to change 
  cpufreq policy by hand.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Sat Mar 01 2008 - siomon.zheng@sun.com
- Rework 04-script.diff to correct script path.
* Thu Feb 21 2008 - laca@sun.com
- set CFLAGS and LDFLAGS
- add --disable-scrollkeeper configure option
* Mon Feb 18 2008 - simon.zheng@sun.com
- Bump to version 2.21.92.
- Remove upstream patch 08-debugging-crash.diff.
- Remove upstream patch 09-brightness-applet-install.diff.
- Remove upstream patch 11-beep-failure.diff.
- Remove upstream patch 12-lid-shutdown.diff.
- Remove upstream patch 13-brightness-reduction.diff.
- Rework 03-disable-sleep-configration.diff and 07-screensaver.diff. 
* Thu Feb 14 2008 - simon.zheng@sun.com
- Reorder the patches list and add bug comments.
- Add patch gnome-power-manager-07-screensaver.diff
- Disable gnome-power-manager-14-authorization-checking.diff, 
  and option "--enable-policykit". Will rework later.
* Thu Feb 14 2008 - jeff.cai@sun.com
- Move to gnome spec repository from sourceforge
* Mon Jau 28 2008 - simon.zheng@sun.com
- Add patch gnome-power-manager-17-interactive-cmd.diff to
  set gnome-sys-suspend as power button interactive policy.
* Fri Jau 25 2008 - simon.zheng@sun.com
- Enable configure option --enable-polkit.
* Mon Jau 21 2008 - simon.zheng@sun.com
- Add gnome-power-manager-16-brightness-reduction.diff to fix
  bugzilla bug #510068.
- Rework gnome-power-manager-11-authrization-checking.diff to
  add cpufreq policy auth checking.
* Mon Jau 14 2008 - simon.zheng@sun.com
- Add gnome-power-manager-14-lid-shutdown.diff.
- Add gnome-power-manager-15-inhibit-lid-beeping.diff to diable 
  beeping when lid id closed or opened.
* Mon Jau 07 2008 - simon.zheng@sun.com
- Add gnome-power-manager-13-beep.diff to bugzilla bug #507789.
* Thu Dec 20 2007 - simon.zheng@sun.com
- Rework gnome-power-manager-07-disable-sleep-configration.diff.
- Add gnome-power-manager-11-authorization-checking.diff
- Add gnome-power-manager-12-crash.diff
* Wed Dec 19 2007 - simon.zheng@sun.com
- Add gnome-power-manager-10-diable-suspend-button-configration.diff.
* Tue Dec 18 2007 - simon.zheng@sun.com
- Rework gnome-power-manager-07-disable-sleep-configration.diff.
- Rework gnome-power-manager-08-brightness-applet-install.diff.
- Add gnome-power-manager-09-scripts.diff.
* Mon Dec 17 2007 - simon.zheng@sun.com
- Bump to 2.21.1.
- Rework gnome-power-manager-01-build.diff.
- Remove gnome-power-manager-02-kstat.diff.
- Remove upstream patch gnome-power-manager-03-brightness-get-stuck.diff.
- Remove gnome-power-manager-04-display-sleep.diff.
- Remove gnome-power-manager-05-configure-power-conf.diff
- Add gnome-power-manager-07-disable-sleep-configration.diff.
- Add gnome-power-manager-08-brightness-applet-install.diff.
* Thu Dec 12 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-06-icon_plicy_and_cpufreq_show.diff,
  set gconf key "cpufreq_show" as true by default and define
  gconf key "icon_policy" as always by default.
* Fri Dec 07 2007 - simon.zheng@sun.com
- Update patch gnome-power-manager-05-configure-power-conf.diff.
* Thu Dec 06 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-05-configure-power-conf.diff
  to make autoS3, autoshutdwon, disk powermanagement, autopm
  work on Solaris.
* Wed Nov 28 2007 - simon.zheng@sun.com
- Add patch gnome-power-manager-04-display-sleep.diff, to
  make display sleeping work.
* Fri Nov 17 2007 - simon.zheng@sun.com
- Bump to version 2.20.1
- Add patch gnome-power-manager-03-brightness-get-stuck.diff.
  to fix bugzilla bug #497298,
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Add intltoolize to fix build
* Wed Sep 19 2007 - simon.zheng@sun.com
- Bump to version 2.20.0
* Tue Aug 28 2007 - jeff.cai@sun.com
- Bump to version 2.19.6.
* Tue May 15 2007 - simon.zheng@sun.com
- Bump to version 2.19.2.
* Mon May 14 2007 - simon.zheng@sun.com
- Add a patch gnome-power-manager-02-kstat.diff to 
  port cpu usage statistic to solaris.
* Tue May 08 2007 - simon.zheng@sun.com
- Bump to version 2.19.1
* Fri Apr 27 2007 - simon.zheng@sun.com
- Bump to version 2.18.2
* Tue Mar 28 2007 - simon.zheng@sun.com
- initial version for pkgbuild
