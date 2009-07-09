#
# spec file for package gdm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:         gdm
License:      GPL v2, LGPL v2, Public Domain
Group:        System/GUI/GNOME
#### DO NOT BUMP MODULE TO 2.21.x to 2.24.x AS IT IS BEING REWRITTEN AND IS
#### NOT YET READY FOR SOLARIS
Version:      2.20.10
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The GNOME 2.x Display Manager
Source:       http://ftp.gnome.org/pub/GNOME/sources/gdm/2.20/gdm-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
%if %option_with_sun_branding
#owner:yippi date:2004-11-24 type:branding
Patch1:	      gdm-01-sun-branding.diff
%endif
%if %option_with_indiana_branding
#owner:yippi date:2007-10-05 type:branding
Patch1:	      gdm-01-indiana-branding.diff
%endif
#owner:yippi date:2007-08-02 type:feature bugster:3163 bugzilla:457871,536387
Patch2:       gdm-02-showlocale.diff
#owner:yippi date:2008-04-30 type:branding
Patch3:       gdm-03-disable-cde.diff
#owner:fujiwara date:2008-04-10 type:feature bugster:5052540,6733528 bugzilla:547549
Patch4:       gdm-04-im-config.diff
# This patch is to disable VT checking, remove it after bugster #6480003 fixed. 
#owner:halton date:2008-12-04 type:branding
Patch5:       gdm-05-disable-vt.diff
#owner:yippi date:2008-12-16 type:branding
Patch6:       gdm-06-xfree-xinerama.diff
#owner:yippi date:2009-02-24 type:feature bugster:6789400
# GOK needs to launch via D-Bus since it uses GConf.
Patch7:       gdm-07-gok.diff
#owner:fujiwara date:2009-03-04 type:bug bugster:6809375
Patch8:       gdm-08-g11n-add-ka-es.diff
URL:          www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}
Autoreqprov:  on
Prereq:       /usr/sbin/groupadd
Prereq:       /usr/sbin/useradd
Prereq:       /sbin/nologin
Prereq:       sed
Prereq:       coreutils

%define pango_version 1.4.0
%define gtk2_version 2.4.0
%define libglade_version 2.3.6
%define libgnomeui_version 2.6.0
%define libgnomecanvas_version 2.6.0
%define librsvg_version 2.5.0
%define libxml2_version 2.6.7
%define scrollkeeper_version 0.3.14
%define pam_version 0.77
%define gail_version 1.6.3
%define XFree86_version 4.3.99
%define usermode_version 1.68
%define openssl_version 0.9.7d

%define dsp_mgr_file /etc/sysconfig/displaymanager
%define xdm_rc_file /etc/init.d/xdm


Requires: gtk2 >= %{gtk2_version}
Requires: sun-gdm-themes
Requires: libglade >= %{libglade_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: libgnomecanvas >= %{libgnomecanvas_version}
Requires: librsvg >= %{librsvg_version}
Requires: libxml2 >= %{libxml2_version}
Requires: pam >= %{pam_version}
Requires: usermode >= %{usermode_version}
Requires: openssl >= %{openssl_version}

BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires: librsvg-devel >= %{librsvg_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: pam-devel >= %{pam_version}
BuildRequires: XFree86-devel >= %{XFree86_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: usermode >= %{usermode_version}
BuildRequires: openssl-devel >= %{openssl_version}

%description
This version of GDM, the GNOME Display manager is based on
GTK2 and suited for the GNOME Desktop Environment. GDM is a
flexible X-Window Display Manager that allows to set many
options, usable for remote login, and provides a good looking
graphical interface.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%if %option_with_sun_branding
%patch1 -p1
%endif
%if %option_with_indiana_branding
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1

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

export CFLAGS="$RPM_OPT_FLAGS"
autoheader
autoconf

ENABLE_CONSOLE_HELPER=
%ifos linux
ENABLE_CONSOLE_HELPER="--enable-console-helper"
%endif

BINDIR_CONFIG=""
CTRUN_CONFIG=""
%ifos solaris
BINDIR_CONFIG="--with-post-path=/usr/openwin/bin"
CTRUN_CONFIG="--with-ctrun"
%endif

libtoolize --force
glib-gettextize -c -f
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}/X11 \
	--localstatedir=%{_localstatedir}/lib \
	--mandir=%{_mandir} \
	--with-pam-prefix=%{_sysconfdir} \
	--libexecdir=%{_libexecdir} \
	--with-prefetch \
	--with-console-kit=no \
	--disable-scrollkeeper \
	--with-greeter-im=no \
	--enable-ipv6=yes $ENABLE_CONSOLE_HELPER $BINDIR_CONFIG $CTRUN_CONFIG
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
#
# Remove gdmflexiserver.desktop until Virtual Termainals are supported
# on Solaris.  Continue shipping gdmflexiserver-xnest.desktop since
# running GDM in a Xnest window does work.
#
%ifos solaris
rm $RPM_BUILD_ROOT%{_datadir}/gdm/applications/gdmflexiserver.desktop
%endif

%if %option_without_dt
# We really want "rm -f" since the gdm module does not install the CDE.desktop
# file unless /usr/dt/bin/Xsession exists on the system.  So the rm command
# is only useful when building without dt support when CDE is installed.
rm -f $RPM_BUILD_ROOT%{_datadir}/xsessions/CDE.desktop
%endif

# Clean up unpackaged files
#
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/lib/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r -g 50 gdm
/usr/sbin/useradd -r -o -g gdm -u 50 -s /sbin/nologin \
-c "Gnome Display Manager daemon" -d /var/lib/gdm gdm 2> /dev/null || :


%post
if [ -f %{dsp_mgr_file} ]; then
	sed -e 's/^DISPLAYMANAGER=.*/DISPLAYMANAGER="gdm"/' %{dsp_mgr_file} > /tmp/displaymanager.$$

	if [ $? -eq 0 ]; then
		mv /tmp/displaymanager.$$ %{dsp_mgr_file}
	fi
fi

if [ -f %{xdm_rc_file} ]; then
	sed -e 's#^\( *gdm.*DISPLAYMANAGER=\)\(.*\)#\1/usr/bin/gdm ;;#' %{xdm_rc_file} > /tmp/xdm.$$

	if [ $? -eq 0 ]; then
		mv /tmp/xdm.$$ %{xdm_rc_file}
		chmod 755 %{xdm_rc_file}
	fi
fi


%files
%config %attr(-,gdm,gdm) %{_sysconfdir}/X11/gdm
%config %attr(-,root,root) %{_sysconfdir}/X11/dm
%{_datadir}/locale/*/LC_MESSAGES/gdm*.mo
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/gtk-2.0/modules/*.so
%{_libexecdir}/*
%{_datadir}/gdm
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/faces/*.jpg
%{_datadir}/pixmaps/faces/*.png
%{_datadir}/icons
%{_datadir}/gnome/help/*
%{_datadir}/xsessions/*
%{_mandir}/man1/*
%{_datadir}/omf/*
%attr(-,gdm,gdm) /var/lib/gdm
%config /etc/pam.d/*
%config /etc/security/*

%changelog
* Thu Mar 19 2009 - brian.cameron@sun.com
- Bump to 2.20.10.  Remove upstream patches.
* Wed Mar 18 2009 - brian.cameron@sun.com
- Add patch gdm-14-gid.diff to fix bugster bug #6819281.
* Wed Mar 04 2009 - takao.fujiwara@sun.com
- Add gdm-13-g11n-add-ka-es.diff for new es_US.UTF-8 and ka_GE.UTF-8. #6809375
* Fri Feb 27 2009 - brian.cameron@sun.com
- Add patch gdm-12-display.diff so that the DISPLAY variable is available 
  after changing the language.  Some PAM modules need the DISPLAY variable.
  Fixes bug #6811555.
* Mon Feb 24 2009 - brian.cameron@sun.com
- Add patch gdm-10-gestures.diff to fix doo bug #6766.  Add patch
  gdm-11-gok.diff to fix bug #6789400.
* Mon Feb 09 2009 - takao.fujiwara@sun.com
- Add patch gdm-09-xinitrc-migration.diff. Scripts are moved into xinitrc.d
* Mon Jan 05 2008 - brian.cameron@sun.com
- Add patch gdm-07-audit.diff to fix bug #6734635.  Add patch
  gdm-08-createdt.diff to fix doo bug #5973.
* Tue Dec 19 2008 - brian.cameron@sun.com
- Add patch gdm-06-xfree-xinerama.diff so that GDM builds using the Xfree
  Xinerama interfaces and not the obsolete Solaris ones.  Fixes P1 bug
  #6768573.
* Wed Dec 10 2008 - brian.cameron@sun.com
- Bump to 2.20.9.  Remove upstream patches.
* Thu Dec 04 2008 - halton.huo@sun.com
- Add disable-vt.diff to disable VT, remove it after bugster #6480003 is fixed
* Fri Nov 21 2008 - brian.cameron@sun.com
- Remove patch gdm-06-dbus.spec, it is no longer needed since D-Bus autolaunch
  is working better.
* Wed Nov 12 2008 - brian.cameron@sun.com
- Add gdm-10-no-recreate-sockets.diff so that GDM avoids recreating the
  sockets directories in /tmp.  This fixes Trusted Extensions.  Refer to
  doo bug #4719.
* Thu Oct 23 2008 - brian.cameron@sun.com
- Add patch gdm-09-fbconsole-fix.diff to address doo bug #3316.
* Mon Oct 20 2008 - takao.fujiwara@sun.com
- Updated gdm-07-xsession.diff to apply CJK locale only.
* Mon Sep 22 2008 - william.walker@sun.com
- Add bug number and better comment for gdm-06-dbus.diff patch.
* Wed Sep 17 2008 - brian.cameron@sun.com
- Add patch gdm-06-dbus.diff and gdm-07-xsession.diff.
* Wed Sep 03 2008 - brian.cameron@sun.com
- Bump to 2.20.8.  Remove upstream patches.
* Wed Sep 03 2008 - takao.fujiwara@sun.com
- Updated gdm-02-showlocale.diff not to show broken locales.
* Mon Aug 25 2008 - brian.cameron@sun.com
- In discussion with the Xserver team, it was determined that the previous
  patch is inappropriate.  The fbconsole program itself will be modified
  so it does a null-operation when it shouldn't be called, so GDM shouldn't
  avoid calling it in various situations.  In this discussion it was 
  highlighted that fbconsole needs the "-n" argument when called from the
  login program to avoid a race condition with XDMCP remote sessions.  Now
  the patch adds this feature.
* Tue Aug 19 2008 - takao.fujiwara@sun.com
- Replce gdm-04-disable-im.diff with gdm-04-im-config.diff with 6733528
* Thu Aug 07 2008 - simon.zheng@sun.com
- Add 07-fbconsole.diff.
* Tue Aug 05 2008 - brian.cameron@sun.com
- Add patch to add Kazakh language, as requested by Jan Trejbal and Jan Lana
  from the Sun localization team.  This patch is upstream.  Fixes bugster bug
  #6724439.
* Tue Jul 01 2008 - brian.cameron@sun.com
- Bump to 2.20.7.  Remove upstream patches.
* Fri Jun 20 2008 - simon.zheng@sun.com
- Add patch gdm-07-suspend-auth.diff to check suspend auth before
  showing supend button on sysmenu.
- Add patch gdm-06-fixcrash.diff to avoid GDM crashing on exit.  Fixes
  bugzilla bug #517526. 
* Thu May 22 2008 - brian.cameron@sun.com
- Add patch gdm-05-atom.diff so that GDM does not create the XFree86_VT
  atom if it does not exist.
* Mon May 12 2008 - brian.cameron@sun.com
- Bump to 2.20.6.
* Thu May 01 2008 - brian.cameron@sun.com
- Add patch gdm-06-disable-cde.diff so that we mark the CDE.desktop 
  file as being hidden.  Users can re-enable it by simply removing
  the "Hidden=true" line in the /usr/share/xsessions/CDE.desktop
  file.  And fix a bug that causes desktop files marked as
  Hidden=true to show up.
* Wed Apr 30 2008 - brian.cameron@sun.com
- Add patch gdm-05-fixcrash.diff fixing bugzilla crashing bug #517526.
* Tue Apr 15 2008 - brian.cameron@sun.com
- The gdmflexiserver.desktop file moved to a different directory, so 
  remove it from the correct location.  Fixes bug #6689633.
* Thu Apr 10 2008 - takao.fujiwara@sun.com
- Add gdm-04-disable-im.diff for disable IM on greeter.
* Mon Apr 07 2008 - brian.cameron@sun.com
- Bump to 2.20.5.
* Mon Mar 10 2008 - brian.cameron@sun.com
- Bump to 2.20.4.
* Fri Feb 29 2008 - takao.fujiwara@sun.com
- Add gdm-03-locale-support.diff
* Mon Jan 07 2008 - brian.cameron@sun.com
- Bump to 2.20.3 and remove upstream patch.
* Tue Nov 27 2007 - brian.cameron@sun.com
- Remove upstream gdm-03-sockaddr-len.diff patch and added new
  gdm-03-xdmcp-close.diff patch needed for XDMCP to work properly.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.2.
* Thu Nov 08 2007 - brian.cameron@sun.com
- Add patch gdm-03-sockaddr-len.diff to fix XDMCP so it works.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Fri Oct  5 2007 - laca@sun.com
- use separate branding patches for nevada and indiana
- delete CDE.desktop when --without-dt is used
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Thu Sep 06 2007 - damien.carbery@sun.com
- Bump to 2.19.8.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.7.
* Wed Aug 15 2007 - brian.cameron@sun.com
- Bump to 2.19.6.  Remove upstream patch.
* Thu Aug 02 2007 - brian.cameron@sun.com
- Add patch gdm-02-showlocale.diff to address bugzilla bug #457871.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.5. Remove upstream patch, 02-g11n-memory-handle.
* Fri Jul 13 2007 - takao.fujiwara@sun.com
- Added gdm-02-g11n-memory-handle.diff for memory handling.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.19.4. Remove upstream patch, 02-vtsupport.
* Thu Jun 21 2007 - brian.cameron@sun.com
- Add patch for better utmpx processing and for VT support when it goes
  into Nevada.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.3. Remove upstream patch, 02-xnestperms.
* Mon Jun 11 2007 - brian.cameron@sun.com
- Add patch to fix GDM so it doesn't modify device permissions if logging
  into a xnest session.
* Mon Jun  4 2007 - brian.cameron@sun.com
- Bump to 2.19.2.  Remove upstream patch gdm-02-no-gdm-in-cde-menu.diff.
* Thu Jue  1 2007 - simon.zheng@sun.com
- Point download path to 2.19.
* Mon May 14 2007 - brian.cameron@sun.com
* Merge patch gdm-03-nossh-in-xsession.diff with gdm-01-branding.diff
  since this is really a branding change.
* Mon May 14 2007 - brian.cameron@sun.com
- Bump to 2.19.1.
* Fri May 11 2007 - brian.cameron@sun.com
- Add --with-ctrun flag since I udpated the patch to require this
  argument.  This way people who want to build GDM on Solaris without
  SVC can do so.  Also added new gdm-05-nossh-in-xsession.diff patch.
* Thu May 10 2007 - brian.cameron@sun.com
- Bump to 2.19.0
* Thu Apr 12 2007 - brian.cameron@sun.com
- Fix upstream bug where if you fail to enter the proper root password
  after asking to run "Configure GDM" from the login menu, it asks for
  the password again.  If you type it in properly, then it starts a
  session as the root user.  This patch fixes this problem.
* Tue Apr 10 2007 - brian.cameron@sun.com
- Backout patch gdm-06-languages.diff since the patch doesn't work 
  properly.  Code needs to be backported from gdm SVN head, and I'll add
  back the patch later if we decide we need this in GNOME 2.18.
* Mon Apr 09 2007 - brian.cameron@sun.com
- Bump to 2.18.1.
* Wed Mar 21 2007 - brian.cameron@sun.com
- Add gdm-10-desktop.diff to fix Catagory in gdmsetup and gdmphotosetup
  desktop file.
* Tue Mar 13 2007 - brian.cameron@sun.com
- Add gdm-07-xephyr.diff and gdm-08-nodbus.diff patches.  Both are 
  upstream.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Fri May 09 2007 - brian.cameron@sun.com
- Add patch gdm-07-fixdesktop.diff to move GDM desktop entries into
  control center.  Add patch gdm-08-fixxnest.diff to fix GDM to send
  the right fontpath to the Xsun Xnest program.  Add patch
  gdm-09-no-gdm-in-cdu-menu.diff to ensure that GDM desktop menu 
  choices only appear if using GDM.  If not using GDM these programs
  are non-functional.
* Fri Mar 02 2007 - brian.cameron@sun.com
- Bump to 2.17.8
* Wed Feb 28 2007 - brian.cameron@sun.com
- Add patch to fix bugster bug #4877721 and bugzilla bug #108820.
  This patch won't go into GDM until 2.19, but we want this patch
  to go into 2.18 for Solaris.
* Tue Feb 15 2007 - brian.cameron@sun.com
- Remove sessionexit patch due to patch review comments.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - brian.cameron@sun.com
- Bump to 2.17.7 and add sessionexit patch to fix bugster bug
  6228488.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.6.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.5. Remove upstream patch, 07-fixdialogs.
* Sun Dec 17 2006 - laca@sun.com
- delete upstream patch fixsecurity.diff
- renumber remaining patch
* Fri Dec 15 2006 - brian.cameron@sun.com
- Patch from CVS head to fix dialog boxes so that they display text.
* Thu Dec 14 2006 - damien.carbery@sun.com
- Bump to 2.17.4.
* Wed Dec 06 2006 - brian.cameron@sun.com
- Remove Linux specific gdm-01-branding-defaults-linux.diff and
  gdm-03-pam-security-setup.diff.  Add patch comments.
* Tue Dec 05 2006 - brian.cameron@sun.com
- Add patch gdm-08-fixsecurity.diff to fix a security vulnerability found
  in gdmchooser.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.3. Remove upstream patches, 07-linguas, 10-fixsessionname,
  09-gdmsetup-launch-menu-tooltip and 11-defaultdesc: Renumber remainder.
* Thu Nov 27 2006 - brian.cameron@sun.com
- Patch to fix setting the sesison name for gnome.desktop.
  Define better name for default.desktop and turn off console kit support
  since it doesn't work on Solaris yet.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Remove upstream patchs, 09-sun-branding-patch and 10-fixfocus. Renumber
  remainder.
* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Wed Nov 15 2006 - calum.benson@sun.com
- Modify tooltip to match latest UI spec.
* Tue Oct 31 2006 - brian.cameron@sun.com
- Add patch to fix focus problem, fixed in CVS head.
* Tue Oct 31 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1. Remove upstream patch, gdm-10-fixcrash.diff.
* Sat Sep 23 2006 - brian.cameron@sun.com
- Add patch to fix crashing.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.10.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.9.
* Tue Aug 01 2006 - damien.carbery@sun.com
- Bump to 2.15.8.
* Fri Jul 28 2006 - dermot.mccluskey@sun.com
- Fix minor typo.
* Wed Jul 26 2006 - brian.cameron@sun.com
- No longer set --with-at-bindir when calling configure since gok and
  gnopernicus are now in the standard /usr/bin location, not /usr/sfw/bin.
* Wed Jul 26 2006 - brian.cameron@sun.com
- Remove patches 7 and 11, merged into CVS head.  Also remove 
  gdmflexiserver.desktop from Solaris builds since we do not support
  Virtual Terminals.  Running this menu choice causes the session to
  hang on Solaris, so we shouldn't put it in the menus.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.7.
* Fri Jun 16 2006 - brian.cameron@sun.com
- Fix focus so it returns to entry field after session, language, restart,
  suspend, and shutdown dialogs are used from options button.
* Mon Jun 12 2006 - brian.cameron@sun.com
- Bumped to 2.14.9.  This fixes automatic login, which was broken, and 
  corrects a number of warnings that were causing core dumping issues.
* Wed Jun 07 2006 - brian.cameron@sun.com
- Bumped to 2.14.8.  Removed patches no longer needed.  This fixes a serious
  security issue where a user can access the gdmsetup GUI with their user 
  password if the face browser is enabled (off by default on Solaris).
* Tue Jun 06 2006 - brian.cameron@sun.com
- Added patch gdm-12-fixflexiserver.diff to fix a core dumping problem.
  Modified gdm-01-branding-defaults-solaris.diff to better integrate with
  ctrun and updated the gdm.xml SVC manifest so that core dumps do not
  cause GDM to restart.  Removed gdm-05-fix-a11y-crash.diff since it didn't
  work as a fix.
* Mon May 23 2006 - brian.cameron@sun.com
- Bump to 2.14.7.
* Fri May 19 2006 - glynn.foster@sun.com
- Don't show the login photo dialog in the menus - removed according to
  the UI spec, and the functionality should really be apart of the 
  'Personal Information' dialog.
* Fri May 12 2006 - brian.cameron@sun.com
- Added patch gdm-12-fixconfig.diff to fix a problem that prevents users
  from disabiling the failsafe session in the menu.
* Fri May 12 2006 - brian.cameron@sun.com
- Updated to 2.14.6 which has the new features included in the patch
  added in the previous comment.  Replace the patch with a much smaller
  patch that just adds the "startagain" feature.  This is much more
  maintainable.  Also added a patch to update the Lanugage display
  provided by Peter Nugent.
* Thu May 11 2006 - brian.cameron@sun.com
- Add patch to add per-display configuration needed by SunRay.
  This patch also adds the updated Cancel button, the pam-error-logo,
  and real GTK+ buttons needed by Coolstart branding.  These changes
  all copied from GDM CVS head.
* Tue May 09 2006 - brian.cameron@sun.com
- Remove two patches that have been integrated into GDM, and add the
  avoidchown patch so that building this package works if you are a
  running as non-root.
* Wed May 03 2006 - damien.carbery@sun.com
- Bump to 2.14.5.
* Wed Apr 26 2006 - damien.carbery@sun.com
- Bump to 2.14.4.
* Tue Apr 25 2006 - damien.carbery@sun.com
- Bump to 2.14.3.
* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Thu Apr 13 2006 - damien.carbery@sun.com
- Remove upstream patches, 10-libvicious-dir and 11-fixaudit.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Mon Mar 13 2006 - brian.cameron@sun.com
- Add patch 11 to fix auditing logic.  This patch can go away when the
  GDM 2.14.1 comes out.
* Fri Mar  3 2006 - damien.carbery@sun.com
- Bump to 2.13.0.10.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.0.9.
- Remove upstream patch, 11-fixcore.
* Thu Feb 16 2006 - brian.cameron@sun.com
- Add patch 11 to fix core dumping issue in gdmsetup.  This fix is in 
  CVS head so it can go away when we update to the next version of GDM.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.0.8.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.0.7.
* Thu Jan 19 2006 - brian.cameron@sun.com
- Bump to 2.13.0.6.
* Mon Jan 16 2006 - damien.carbery@sun.com
- Move sfw reference (a Solaris specific dir) to SUNWgnome-display-mgr.spec.
* Mon Jan 16 2006 - padraig.obriain@sun.com
- Bump to 2.13.0.5; dd --with-prefetch and add /usr/sfw/include to CFILES to
  find <tcpd.h>
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.0.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.0.3
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.8.0.7.
* Thu Oct 13 2005 - damien.carbery@sun.com
- Added patch, 10-libvicious-dir, to remove dir in vicious-extensions 
  Makefile.am, as it caused build to fail.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.0.8.5
* Wed Sep 21 2005 - brian.cameron@sun.com
- Bump to 2.8.0.4
* Wed Sep 07 2005 - damien.carbery@sun.com
- Remove capplets dir from %files. Contents moved in 2.8.0.3.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.8.0.3.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.8.0.1.
* Wed Aug 03 2005 - laca@sun.com
- remove upstream patch xnext-remote-session.diff
* Thu Jul 14 2005 - damien.carbery@sun.com
- Add unpackaged files to %files (pixmaps/faces and gnome/capplets).
* Wed Jul 13 2005 - brian.cameron@sun.com
- Upgraded to 2.8.0.1
* Fri Jun 10 2005 - matt.keenan@sun.com
- Re-applied patch 01 linux branding
- Added patch 04/05 to build
* Tue May 10 2005 - leena.gunda@wipro.com
- Added patch gdm-45-xnest-remote-session.diff to allow remote login
  using XDMCP chooser in nested window. Fixes bug #6245415.
* Tue Apr 19 2005 - bill.haneman@sun.com
- Reinstated xevie-enabling patch on Linux, via gdm-44-linux-xevie.diff.
* Fri Apr 1 2005 - brian.cameron@sun.com
- Add patch 43 so that we set the Xserver on Solaris to 
  /usr/X11/bin/Xserver instead of /usr/X11/bin/X as per ARQ
  request.  Also now put /usr/openwin/bin in the user default
  patch here instead of in SUNWdtlogin-integration.spec.
* Thu Mar 17 2005 - brian.cameron@sun.com
- Add patch 42 to allow configure to specify the full path to the
  a11y AT programs used in the gesture listener configuration files.
  Patch in gdm CVS head.
* Thu Mar 10 2005 - Chookij.Vanatham@Sun.COM
- Fix gdm to fork user's session with "system locale" if "Default" option
  at the language menu being selected. [CR Id: 5032088]
* Thu Mar 03 2005 - brian.cameron@sun.com
- Fix XDMCP logic so that it works when an IPv4 address requests a 
  connection and IPV6 is enabled in GDM.  Patch40 fixes this.
* Tue Mar 01 2005 - dermot.mccluskey@sun.com
- remove patch 40 (XEVIE) - break new X server
* Fri Feb 25 2005 - brian.cameron@sun.com
- Added patch 40 to turn on XEVIE on Linux by default for the
  standard server to meet a11y requirements.  Fixes bug 6226645.
* Thu Feb 24 2005 - brian.cameron@sun.com
- Added branding patch 39 to change the GNOME string to "Java Desktop
  System" in a number of places in the c-code.
* Tue Feb 22 2005 - brian.cameron@sun.com
- Backed out patch 39/40 since ARC determined that these flags should
  not be set by default after initially indicating it was okay.
* Mon Feb 14 2005 - brian.cameron@sun.com
- Added patch 39/40 to support setting the Xserver with needed 
  a11y Xserver flags.  Fixes CR 6226645. 
* Tue Feb 08 2005 - brian.cameron@sun.com
- Removed --with-post-path argument since /usr/dt/bin and
  /usr/openwin/bin are added also by the /usr/dt/config/Xinitrc.jds.
  No need to have them in the PATH twice.  Also we do not
  need to add /usr/demo/jds/bin since all the *.desktop files
  have full-paths defined.
* Mon Feb 07 2005 - brian.cameron@sun.com
- Added patch-38 to more cleanly set the default PATH.  This replaces
  patches gdm-15-default.path.diff and gdm-16-reboot-shutdown-option.diff.
  The new patch sets more sensible definitions for Halt, Reboot, Shutdown
  commands on Solaris.  Also updated gdm-18-help.diff so it forwards
  the user to the right subsection when running gdmsetup help.
* Fri Jan 21 2005 - brian.cameron@sun.com
- Now only apply patch 37 when building on Linux.  Modified patch 37 to
  include needed changes for Solaris.
* Tue Jan 18 2005 - brian.cameron@sun.com
- Added patch gdm-37-branding.diff to fix branding issue in gnome.desktop
  file.  Also updated gdm-21-fix-a11y-crash.diff patch so it works on
  JDS Linux.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Thu Dec 30 2004 - Chookij.Vanatham@Sun.COM
- #6213083 - Add note that legacy locales are NOT SUPPORTED for linux platform.
* Wed Dec 22 2004 - leena.gunda@wipro.com
- Added gdm-35-flexi-xdmcp-option.diff to make XDMCP chooser work in 
  flexiserver. Fixes bug #4992853.
* Fri Nov 26 2004 - leena.gunda@wipro.com
- Added gdm-34-xsession-use-ksh.diff to execute Xsession script using
  ksh on Solaris. Fixes stopper bug #6199960.
* Wed Nov 24 2004 - Chookij.Vanatham@Sun.COM
- #6196675 - all single byte locales removed.
* Thu Nov 18 2004 - hidetoshi.tajima@sun.com
- #5081827 - run /usr/dt/config/Xsession.jds instead of gnome-session
  for gnome session vid gdm. Solaris only.
* Wed Nov 17 2004 - matt.keenan@sun.com
- #6195855 Install correct man page
* Wed Nov 10 2004 - Chookij.Vanatham@Sun.COM
- Added gdm-31-current-locale.diff to fix bug#5100351
* Wed Nov 10 2004 - leena.gunda@wipro.com
- Remove gdm-26-start-gnome-volcheck.diff as gnome-volcheck is now
  started by gnome-session.
* Mon Nov 09 2004 - alvaro.lopez@sun.com
- Added new patch 31. It fixes #6182860: IPv6 logic is broken for New
  Login in a Nested Window, so the enable-ipv6 parameter of configure
  is "yes" again.
* Mon Nov 01 2004 - hidetoshi.tajima@sun.com
- Modify gdm-07-set-lc-messages-to-lang.diff. set LANG from RC_LANG
  in /etc/sysconfig/language when it is NULL. (CR 6188663)
* Fri Oct 29 2004 - damien.carbery@sun.com
- Add gdm-30-xorg-conf.diff to fix 6185918. configure.in checks for Xorg
  binary before looking for X (Xsun) binary.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Added gdm-binary.1.gz, gdm.1.gz, gdmXnest.1.gz, gdmXnestchooser.1.gz,
  gdmchooser.1.gz, gdmflexiserver.1.gz, gdmgreeter.1.gz, gdmlogin.1.gz,
  gdmphotosetup.1.gz, gdmsetup.1.gz, gdmthemetester.1.gz, gdm-restart.1m.gz,
  gdm-safe-restart.1m.gz, gdm-stop.1m.gz, gdmconfig.1m.gz man pages
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Fri Oct 22 2004 - alvaro.lopez@sun.com
- "Source" entry updated
* Thu Oct 21 2004 - brian.cameron@sun.com
- Removed ipv6 support (--enable-ipv6=no) since this is breaking 
  gdm's ability to "login in a nested window".  Created bug 6182860
  so that issue gets fixed.
* Wed Oct 20 2004 - leena.gunda@wipro.com
- Added patch gdm-27-alt-meta-mapping.diff to restore 'Alt' and 'Meta' 
  mappings on sparc Solaris. Fixes bug 6173594.
* Wed Oct 20 2004 - leena.gunda@wipro.com
- Added patch gdm-26-start-gnome-volcheck.diff to start gnome-volcheck
  if Xserver is local. Fixes bug #5107205.
* Fri Oct 15 2004 - brian.cameron@sun.com
- Correct GreenLine integration.  The problem with disabling core dumps
  in the GreenLine XML file is that this causes GreenLine to ignore 
  core dumps for all programs, including gdm.  Now using patch 25
  we use ctrun to specify that only programs launched from gdm's 
  Xsession script (the user's session) are run in a separate GreenLine
  contract that ignores core dumps.  This way if gdm itself core dumps,
  GreenLine will correctly default back to the console login.
* Thu Oct 14 2004 - brian.cameron@sun.com
- Added patch gdm-24-sanitize-conf.diff to clean up language in
  gdm.conf file.  Fixes bug 5097046.  
* Wed Oct 06 2004 - balamurali.viswanathan@wipro.com
- Add patch gdm-22-xserver-location.diff to set GDM_XSERVER_LOCATION 
  with the x server type. Fixes bug #6174802
* Wed Oct 06 2004 - padraig.obriain@sun.com
- Added patch gdm-21-fix-a11y-crash.diff to remove
  /var/tmp/orbit-gdm/bonobo-activation-server-ior.  Fixes bug #5103715.
* Tue Oct 05 2004 - balamurali.viswanathan@wipro.com
- Modified patch gdm-15-default-path.diff to add 
  /usr/openwin/bin to the path. Fixes bug #5106790
* Mon Oct 04 2004 - yuriy.kuznetsov@sun.com
- Added gdm-20-g11n-i18n-button.diff to fix bug#5109970
* Wed Sep 29 2004 - <hidetoshi.tajima@sun.com>
- updated gdm-03-locale-alias.diff to remove non-UTF-8
locale entries from Traditional Chinese (big5 and big5hkscs)
* Mon Sep 20 2004 - dermot.mccluskey@sun.com
- Added chmod xdm in post-install script
* Fri Sep 17 2004 - bill.haneman@sun.com
- Added patch gdm-20-gdmwm-struts.diff, to fix bugzilla
  #143634.
* Thu Sep 16 2004 - dermot.mccluskey@sun.com
- Added post install script to set gdm as displaymanager
* Wed Sep 15 2004 - archana.shah@wipro.com
- Patch added gdm-19-add-acroread-path.diff
  Fixes bug# 5087934
* Thu Aug 26 2004 - vinay.mandyakoppal@wipro.com
- Patch gdm-18-help.diff provide help link.
* Thu Aug 26 2004 - bill.haneman@sun.com
- Updated patch gdm-10-a11y-gestures.diff.
* Tue Aug 24 2004 - brian.cameron@sun.com
- Enabling ipv6.
* Tue Aug 24 2004 - glynn.foster@sun.com
- Add back icons
* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- removed some icons
* Thu Aug 19 2004 - damien.carbery@sun.com
- Integrate updated docs tarball from eugene.oconnor@sun.com.
* Fri Aug 13 2004 - bill.haneman@sun.com
- Update patch gdm-10-a11y-gestures.diff.  Fixes bug #5067111.
* Thu Jul 29 2004 - bill.haneman@sun.com
- use version 2.6.0.3 (fix for bugzilla 144920 and related GOK problem)
- remove patches gdm-08-gdmtranslate.diff and gdm-09-fix-which.diff,
  since they are included in 2.6.0.3.
* Thu Jul 22 2004 - vinay.mandyakoppal@wipro.com
- add patch to remove reboot/shutdown option on Solaris box
* Thu Jul 22 2004 - leena.gunda@wipro.com
- add patch gdm-15-default-path.diff to add /usr/dt/bin and /usr/sfw/bin
  to PATH for Solaris. 
* Wed Jul 14 2004 - niall.power@sun.com
- add patch from Johan to invoke jds registration on first login
* Thu Jul 08 2004 - arvind.samptur@wipro.com
- add patch to pass X server options instead of hardcoding 
  it in the gdm.conf.in
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 23 2004 - damien.carbery@sun.com
- Update a11y-gestures patch to add HAVE_XINPUT to acconfig.h.
  Remove xdmcp-enable patch (10) for app security reasons and move 13 to 10.
* Thu Jun 10 2004 - damien.carbery@sun.com
- Add patch 12 to add 'docs/C/figures' directory to the build.
* Mon May 31 2004 - niall.power@sun.com
- bump to 2.6.0.2
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gdm-l10n-po-1.1.tar.bz2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 08 2004 - <niall.power@sun.com>
- bumped to 2.6.0.0 and updated dependencies
* Sat Apr 03 2004 - Chookij.Vanatham@Sun.COM
- added gdm-11-g11n-truncated-username.diff to fix 4955151
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Wed Mar 31 2004 - <hidetoshi.tajima@sun.com>
- updated gdm-03-locale-alias.diff to fix 4884887
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gdm-l10n-po-1.0.tar.bz2
* Tue Mar 23 2004 - <glynn.foster@sun.com>
- Remove photo setup from %files since we didn't want it part of the 
  menus by default [$datadir/gnome/capplets/..]
* Mon Mar 22 2004 - <laca@sun.com>
- simplify %build
* Fri Mar 19 2004 - <damien.carbery@sun.com>
- Move autoheader and autoconf out of the platform specific section because
  it is common to both platforms.
* Fri Mar 19 2004 - <damien.carbery@sun.com>
- Change '\' to ';' so autoheader and autoconf run separately.
* Thu Mar 18 2004 - <brian.cameron@sun.com>
- Add patch 8 that fixes gdmtranslate so it compiles with -g, add
  patch 9 to fix scripts so that they don't call which (since which
  doesn't work on Solaris without an associated TTY), and add patch
  10 to turn on XDMCP support by default.
* Tue Mar 09 2004 - <niall.power@sun.com>
- bump to 2.5.90.2
* Mon Mar 01 2004 - <laca@sun.com>
- s$/usr/share$%{_datadir}$
* Thu Feb 26 2004 - <damien.carbery@sun.com>
- Fix small typos in description and change tar commmand to bzcat/tar.
- Remove --enable-console-helper on Solaris.
* Fri Feb 06 2004 - <matt.keenan@sun.com>
- Bump to 2.5.90.0, add docs, and ported QS patches
* Wed Jan 07 2004 - <niall.power@sun.com>
- Update to 2.4.4.7 for gnome-2.5.x
- Regenerated gdm-07-enable-tcp-by-default.diff
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the Sun Supported menu entry patch, and reorder.
* Tue Oct 14 2003 - <markmc@sun.com> 2.4.4.3-2
- Add patch from Toshi to normalize the locale environment
  variables to be the same as LANG if they are unset.
* Fri Oct 10 2003 - <niall.power@sun.com> 2.4.4.3
- Update to 2.4.4.3 for gnome-2.4
* Wed Oct 01 2003 - <michael.twomey@sun.com> 2.4.2.101-14
- Add patch from Chookij to fix bug 4901817 (ja_JP.eucJP name)
* Thu Sep 18 2003 - <markmc@sun.com> 2.4.2.101-12
- Add patch from Leena to set AlwaysRestartServer to true.
* Thu Aug 21 2003 - <markmc@sun.com> 2.4.2.101-1
- Upgrade to 2.4.2.101
* Mon Aug 18 2003 - <markmc@sun.com> 2.4.2.99-7
- Set DisallowTCP to false by default.
* Fri Aug 08 2003 - <michael.twomey@sun.com> 2.4.2.99-3
- Updated locale.alias patch with a fix for zh_HK and a tweak
  for ja_JP.sjis (now ja_JP.SJIS). Fixing bug 4899317.
- Added a dependancy on openssl-devel. My build failed because 
  it was missing. I've also added openssl for good measure.
* Thu Aug 07 2003 - <michael.twomey@sun.com> 2.4.2.99-2
- Patched /etc/X11/gdm/Xsession so ~/.xim or /etc/skel/.xim is sourced which
  ensures that XIM input methods are started.
* Fri Aug 01 2003 - <markmc@sun.com> 2.4.2.99-1
- Upgrade to 2.4.2.99.
* Fri Aug 01 2003 - <glynn.foster@sun.com>
- Add supported menu category.
* Sun Jul 27 2003 - <markmc@sun.com>
- Update to 2.4.2.98
- Remove POTFILES.in patch. Seems to be in new tarball.
* Tue Jul 22 2003 - <michael.twomey@sun.com>
- Added a patch to update the POTFILES.in.
* Mon Jul 21 2003 - <glynn.foster@sun.com>
- Changed category of gdmsetup.desktop, so it appears in 
  the system menu again.
* Mon Jul 21 2003 - <michael.twomey@sun.com>
- Added zh_HK (Hong Kong Chinese) to the available languages.
* Fri Jul 18 2003 - <michael.twomey@sun.com>
- Patched locale.alias to include more Asian locale codeset 
  variants as requested by the Asian teams.
* Thu Jul 17 2003 - <markmc@sun.com>
- Fixed up the PAM configuration files.
- Removed the sysconfig/displaymanager hack
* Thu Jul 17 2003 - <niall.power@sun.com>
- update to version 2.4.2.97, release 0
- removed patches gdm-04-setlocale.diff and
  gdm-05-potfiles_in.diff, which are integrated upstream
- Changed sysconfdir to /etc/X11 so that new common sessions
  configuration directory (/etc/X11/dm/Sessions) can be shared
  with kdm etc.
- New common sessions dir /etc/X11/dm added to %files
* Fri Jul 11 2003 - <niall.power@sun.com>
- added setlocal patch - No more Welsh :) (or Czech!)
* Tue Jul 08 2003 - <niall.power@sun.com>
- Remove .desktop capplets from %files since photo setup
  is gone.
* Mon Jul 07 2003 - <glynn.foster@sun.com>
- Remove the photo setup .desktop menu item from the
  Settings menu.
* Tue Jul 01 2003 - <glynn.foster@sun.com>
- Move the pam and branding stuff to patches, and not 
  dirty copy hacks ;)
* Tue Jul 01 2003 - <glynn.foster@sun.com>
- Make gdm now depend on sun-gdm-themes which is a new
  package, replacing the old one.
* Fri Jun 30 2003 - <glynn.foster@sun.com>
- Make gdm now depend on Sundt-gdm-theme. This may be
  crack that we shouldn't do, but until I figure out
  how things work, let's go with it. 
* Fri Jun 30 2003 - <glynn.foster@sun.com>
- New tarball, bump version and reset release. Remove
  the old greeter theme, since we probably don't want
  it installed anyway
* Fri May 02 2003 - <niall.power@sun.com>
- Initial Sun release.
