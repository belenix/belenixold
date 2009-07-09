#
# spec file for package control-center.
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:         gnome-control-center
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The GNOME control center for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/gnome-control-center/2.26/gnome-control-center-%{version}.tar.bz2
Source1:     %{name}-po-sun-%{po_sun_version}.tar.bz2
Source2:      visual-effects-images.tar.bz2
%if %build_l10n
Source3:                 l10n-configure.sh
%endif
# date:2006-12-07 owner:dcarbery type:bug bugzilla:383356
Patch1:       control-center-01-no-libgnomekbd.diff
# date:2004-11-09 owner:dkenny type:bug bugster:6180767
Patch2:       control-center-02-keybinding-caps-lock.diff
# date:2006-11-02 owner:erwannc type:feature
Patch3:      control-center-03-full-hinting-dialog.diff
# date:2008-02-14 owner:erwannc type:feature
Patch4:      control-center-04-compiz-integration.diff
#owner:jedy date:2008-07-14 type:branding
Patch5:      control-center-05-menu-entry.diff
# date:2008-11-14 owner:dkenny type:bug bugster:6771506
Patch6:      control-center-06-use-default-dpi.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/control-center2
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       GConf

%define libgnomeui_version 2.6.0
%define esound_version 0.2.33
%define gnome_desktop_version 2.6.1
%define metacity_version 2.8.0
%define nautilus_version 2.6.1
%define fontilus_version 2.4.0
%define acme_version 2.4.2
%define desktop_file_utils_version 0.10
%define xft_version 2.1.7

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: esound-devel >= %{esound_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires: metacity >= %{metacity_version}
BuildRequires: nautilus-devel >= %{nautilus_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: automake >= 1.9
BuildRequires: evolution-data-server-devel
BuildRequires: gstreamer-plugins-devel

Requires: gst-plugins-base
Requires: libgnomeui >= %{libgnomeui_version}
Requires: esound >= %{esound_version}
Requires: gnome-desktop >= %{gnome_desktop_version}
Requires: nautilus >= %{nautilus_version}
Requires: evolution-data-server

Obsoletes:      fontilus < %{fontilus_version}
Provides:       fontilus = %{fontilus_version}
Obsoletes:	acme < %{acme_version}
Provides:	acme = %{acme_version}

%description
This package contains the new control-center for the GNOME desktop.

%package devel
Summary:       Development files for the GNOME control center for GNOME 2.6
Group:         Development/Libraries/GNOME
Requires:      %name = %version-%release

%description devel
This package contains the files need for development of GNOME control center capplets

%prep
%setup -q
cd capplets/appearance/data
bzcat %SOURCE2 | tar xf -
cd ../../..
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
gnome-doc-common
gnome-doc-prepare --force
libtoolize --force
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

%if %with_hal
export ENABLE_HAL_CONFIG="--enable-hal"
%else
export ENABLE_HAL_CONFIG="--disable-hal"
%endif

CFLAGS="$RPM_OPT_FLAGS -DDBUS_API_SUBJECT_TO_CHANGE -I/usr/X11/share/include" \
  ./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir}       \
    --libexecdir=%{_libexecdir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-scrollkeeper \
    --enable-aboutme \
    --disable-gswitchit \
    $ENABLE_HAL_CONFIG
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL       
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.a
rm $RPM_BUILD_ROOT%{_libdir}/window-manager-settings/*.la
                                                                               
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="apps_gnome_settings_daemon_default_editor.schemas apps_gnome_settings_daemon_screensaver.schemas desktop_gnome_font_rendering.schemas desktop_gnome_peripherals_keyboard_xkb.schemas apps_gnome_settings_daemon_keybindings.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_prefix}/bin/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/pixmaps/*
%{_datadir}/idl/*.idl
%{_datadir}/control-center-2.0/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%{_datadir}/gnome/vfolders/*
%{_datadir}/gnome/cursor-fonts/*
%{_datadir}/gnome/help/*
%{_datadir}/omf
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_datadir}/gnome-background-properties
%{_datadir}/gnome-default-applications
%{_libdir}/*.so.*
%{_libdir}/bonobo/servers/*
%{_libdir}/gnome-vfs-2.0/modules/*.so*
%{_libdir}/nautilus/extensions-2.0/*.so
%{_libdir}/window-manager-settings/*.so
%{_libexecdir}/gnome-settings-daemon
%{_mandir}/man1/*

%files devel
%{_includedir}/gnome-window-settings-2.0/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Jan 10 2009 - matt.keenan@sun.com
- Bump to 2.25.90.
* Tue Jan 09 2009 - darren.kenny@sun.com
- Remove upstreamed feature in patch control-center-02-custom-keybinding.diff
  Renumber remaining patches.
* Sat Dec 27 2008 - dave.lin@sun.com
- Bump to 2.25.3.
* Wed Dec 03 2008 - dave.lin@sun.com
- Remove upstreamed patch 07-xrandr-warning.diff.
* Fri Nov 14 2008 - darren.kenny@sun.com
- Add patch control-center-08-use-default-dpi.diff to fix bug#6771506 where
  the default DPI set in the schema wasn't being used.
* Mon Oct 20 2008 - takao.fujiwara@sun.com
- Updated 05-compiz-integration.diff for SUN_BRANDING. Fixes #6761162.
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.24.0.1.  Remove upstream patch control-center-07-audiotheme.diff.
* Thu Sep 25 2008 - matt.keenan@sun.com
- Add patch 08-xrandr-warning.diff, fixes #6752483 XRANDR core
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Tue Aug 20 2008 - brian.cameron@sun.com
- Add patch control-center-07-audiotheme.diff to fix crashing problem when
  building with libcanberra.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Wed Aug 06 2008 - matt.keenan@sun.com
- Bump to 2.23.6.
* Fri Jul 25 2008 - damien.carbery@sun.com
- Remove references to %nautilusdir and to
  %{_libdir}/gnome-vfs-2.0/modules/*.so and %{_nautilusdir}.
* Fri Jul 25 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Mon Jul 14 2008 - jedy.wang@sun.com
- Add 06-desktop.diff.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Wed Jun 03 2008 - darren.kenny@sun.com
- Bump to 2.23.3.
* Thu May 29 2008 - damien.carbery@sun.com
- Bump to 2.23.2. Remove upstream patch, 05-getpwnam_r, rename
  06-compiz-integration to 05.
* Thu May 29 2008 - damien.carbery@sun.com
- Bump to 2.22.2.1.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Fri May 09 2008 - brian.cameron@sun.com
- Found that the control-center-07-mediaLib.diff patch did not actually fix
  the problem.  I found the bug was actually caused by an error in the 
  metacity-08-trusted-extensions.diff patch, which I fixed.
* Tue May 06 2008 - brian.cameron@sun.com
- Add patch control-center-07-mediaLib.diff to workaround a crashing problem
  when using mediaLib interpolation type BILINEAR.  Use NEAREST until the
  problem is fixed in the mediaLib libraries.  Fixes bugster bug #6685666.
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Remove upstream patch, 06-gsd-header-dir.
* Mon Feb 04 2008 - damien.carbery@sun.com
- Add patch 06-gsd-header-dir to work with change in gnome-settings-daemon.
  Bugzilla 511820.
* Tue Jan 29 2008 - brian.cameron@sun.com
- Bump to 2.21.90.  Remove upstream patch control-center-06-nautilus-dir.diff.
* Thu Jan 24 2008 - damien.carbery@sun.com
- Remove obsolete patch 07-gsd-headers. It is obsoleted by
  gnome-settings-daemon-10-mv-src-dir.diff.
* Wed Jan 23 2008 - damien.carbery@sun.com
- Add patch 07-gsd-header to change the path to a gnome-settings-daemon header
  as the header file is not installed when called.
* Wed Jan 23 2008 - darren.kenny@sun.com
- Re-order and rework patches due to move of gnome-settings-daemon to a new
  project.
* Mon Jan 12 2008 - brian.cameron@sun.com
- Remove upstream patch control-center-12-fixcrash.diff.
* Fri Jan 11 2008 - damien.carbery@sun.com
- Add patch 13-nautilus-dir to determine nautilus extension dir via pkgconfig.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Thu Nov 29 2007 - brian.cameron@sun.com
- Add patch control-center-12-fixcrash.diff to fix a crashing
  problem when a NULL string is printed.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 31 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Thu Oct  4 2007 - laca@sun.com
- add patch control-center-11-getpwnam_r.diff
* Wed Sep 26 2007 - damien.carbery@sun.com
- Bump to 2.20.0.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Undo Jan's commit - the _POSIX_PTHREAD_SEMANTICS define came from a custom
  x11.pc which is no longer required. Also remove the 11-compilation-errors
  patch as it too is no longer needed.
* Wed Sep 19 2007 - jan.schmidt@sun.com
- Add _POSIX_PTHREAD_SEMANTICS to get the correct form of getpwuid_r.
* Tue Sep 18 2007 - darren.kenny@sun.com
- Bump to 2.20
- Removed upstream compilation fixes for 473967. Remaining patch contents are
  a Solaris specific issue w.r.t. getpwuid_r - appears to only needed for RE
  builds.
* Wed Sep 05 2007 - darren.kenny@sun.com
- Bump to 2.19.92
- Reworked all patches to match new release, and obsoleted some.
- Add new patch for compilation issues - 11-compilation-errors.
* Sun Aug 05 2007 - damien.carbery@sun.com
- Add sparc patch because build failing in gnome-about-me.c because it needs
  the 5 param version.
* Wed Apr 10 2007 - darren.kenny@sun.com
- Change patch 6 to be a feature patch.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarballs for control-center-01-solaris-printmgr.diff.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patches, 01-keybindings-close and
  16-function-macro. Renumber 15 to 01.
* Sun Jan 28 2007 - laca@sun.com
- add %if %build_tjds guard around tjds patch so we can build without trusted
  jds support
* Tue Jan 23 2007 - damien.carbery@sun.com
- Remove upstream patch, 11-menu-entry. Renumber rest.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Mon Dec 18 2006 - matt.keenan@sun.com
- Remove onsolete patch 13-evolution-about-me.diff, renumber patches
* Thu Dec 07 2006 - damien.carbery@sun.com
- Remove obsolete patch, 04-remove-xkb-layout. Rename libgnomekbd patch to 04.
* Wed Dec 06 2006 - damien.carbery@sun.com
- Add 19-function-macro to change __FUNCTION__ to G_GNUC_FUNCTION.
- Add 20-empty-struct to add a member to the empty struct.
- Add 21-no-libgnomekbd so that libgnomekbd is not required.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Tue Nov 14 2006 - padraig.obriain@sun.com
- Remove patch -keybinding-fix-edit as changes are now made in 
  -custom-keybinding patch.
* Mon Nov 13 2006 - patrick.wade@sun.com
- Add patch -sound-preview to fix bugster 6458353
* Mon Oct 23 2006 - padraig.obriain@sun.com
- Add patch -keybinding-fix-edit to fix bugster 6471348, bugzilla 363623.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 19 2006 - brian.cameron@sun.com
- Remove unneeded patch control-center-10-wall.diff 
* Fri Sep 15 2006 - darren.kenny@sun.com
- Remove the control-center-09-volume-control.diff patch since we're now using
  GStreamer correctly.
* Tue Sep 05 2006 - brian.cameron@sun.com
- Now call with --disable-libxklavier to build without
  libxklavier, and --enable-hal/disable-hal as appropriate.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Aug 28 2006 - patrick.wade@sun.com
- patch : control-center-23-sticky-timeout.diff
  Bug #6327546
* Mon Aug 28 2006 - patrick.wade@sun.com
- patch : control-center-22-unique-a11y-kbd.diff
  Bug #6463966
* Wed Aug 23 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Fri Jul 28 2006 - matt.keenan@sun.com
- patch : control-center-21-evolution-about-me.diff : e-contact.h has changed 
  from 1.6->1.8, so about-me image processing needs patching.
* Fri Jul 28 2006 - matt.keenan@sun.com
- patch : control-center-20-reserved-names.diff : bugzilla : #349079
  and 2nd Hunk of control-center-12-wall.diff : bugzilla : #347610
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Web Jul 19 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.
  Remove patch #16 (upstream) and decrement later patches.
* Sat Jul 15 2006 - glynn.foster@sun.com
- Remove all the xkb layout related patches to be
  replaced by a single patch that removes the layout
  options completely.
* Mon Jun 12 2006 - niall.power@sun.com
- Added patch22 to fix issue with negative refresh rates:
  Bug #6437221
* Fri May 05 2006 - glynn.foster@sun.com
- Move a few menu entries around.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - glynn.foster@sun.com
- Remove registration of settings daemon per display patch,
  as it's now upstream, #94049.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Tue Feb 15 2006 - glynn.foster@sun.com
- Remove no apply button patch, since it was reverted upstream.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Fri Feb  3 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
- Remove patch 23-no-es-help as #329331 fixed.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Add patch, 23-no-es-help, to fix #329331.
* Tue Jan 31 2006 - glynn.foster@sun.com
- Add no apply button patch because of braindead maintainer and bump to
  2.13.90
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.5.1.
- Remove 'mkdir m4' call - fixed in 2.13.5.1.
* Wed Jan 18 2006 - brian.cameron@sun.com
- Call glib-gettextize instead of commenting out the po directory from the
  Makefile.am subdirs.  Now build with GStreamer 0.10.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Add patch to fix 327563 (void function returning value), 22-void-return.diff
- Delete 'po' dir ref to stop configure infinite loop: 23-stop-infinite-po-loop.
- Create 'm4' as require by gnome-doc-prepare.
* Mon Jan 16 2006 - glynn.foster@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.3
- Remove upstream patch, -22-about-me.diff.
* Tue Nov 15 2005 - brian.cameron@sun.com
- Patch code so about-me applet can build, and turn on --enable-aboutme
  at configure time.
* Wed Nov 09 2005 - glynn.foster@sun.com
- Disable gnome-screensaver temporarily. Fixes #6346174.
* Thu Oct 13 2005 - damien.carbery@sun.com
- Remove upstream patch, control-center-19-xcursor.diff.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Wed Sep 21 2005 - brian.cameron@sun.com
- Add patch 19 so that if xcursor is not present, the configure doesn't
  bomb out.  The HAVE_XCURSOR stuff is #ifdef'ed in the code so this
  should just build okay without xcursor support.  Better than not
  building at all. 
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Thu Aug 25 2005 - laca@sun.com
- Bump to 2.11.92
- add help to %files
* Thu Aug 25 2005 - damien.carbery@sun.com
- Add automake build dependency, as it will fail for earlier automake.
* Mon Aug 15 2005 - laca@sun.com
- remove patches read-alert-dialog.diff (reported in bugzilla #172090) and
  menu-reorder.diff. Renumber patches.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Thu Aug 04 2005 - laca@sun.com
- patches 37, 38, 40 merged by Wipro; renamed 37, 38, 39, 40 to
  17, 18, 19, 20.
* Fri Jul 22 2005 - srirama.sharma@wipro.com
- Updated control-center-13-anykey-grab.diff to fix the gnome-setting-daemon
  crash on gnome-2.10 Linux.
* Tue Jun 14 2005 - damien.carbery@sun.com
- Remove backgrounds.xml and backgrounds-linux.xml as they are now in a patch.
* Mon Jun 06 2005 - leena.gunda@wipro.com
- Added patches/control-center-40-xkb-check-remote-login.diff to
  make gnome-settings-daemon and the keyboard capplet check for 
  remote login before activating the XKB extension.
  Fixes bug #6271501.
* Thu Jun 02 2005 - brian.cameron@sun.com
- Added patch 16 to remove Wall from Makefile.am files.
* Thu May 26 2005 - arvind.samptur@wipro.com
- Add patch control-center-39-background-crash.diff to fix 
  crash when background properties capplet is closed with
  with the WM's X button option. Fixes #6275902 
* Sat May 21 2005 - arvind.samptur@wipro.com
- Add patch control-center-38-layout-deletion.diff from Leena.
  Fixes the issue of deleting all the keyboard layouts #6272904
* Fri May 13 2005 - arvind.samptur@wipro.com
- Redoing patches for gnome-2.10
* Fri Apr 29 2005 - dinoop.thomas@wipro.com
- Added control-center-36-https-default-browser.diff to make the default browser
  settings apply for https also.
  Fixes #6262124.
* Thu Mar 31 2005 - takao.fujiwara@sun.com
- Added control-center-35-g11n-filename.diff to avoid segv with filename.
  Fixes 6247833
* Thu Mar 31 2005 - vinay.mandyakoppal@wipro.com
- Added control-center-34-read-alert-dialog.diff patch to make screen reader read the
  sticky key alert dialog. Fixes bug #6240627.
* Mon Mar 07 2005 - dinoop.thomas@wipro.com
- Added patch control-center-32-homefolder-keybindings.diff. Makes the shortcut for  
  home folder go to home directory of user instead of computer:///
  Fixes bug #6231348. 
* Fri Feb 25 2005 - vinay.mandyakoppal@wipro.com
- Added patch control-center-31-dnd-non-image.diff. Prevents from adding non image 
  files to the desktop background capplet when dnd from nautilus. Fixes bug #6227064
* Fri Feb 21 2005 - archana.shah@wipro.com
- Added patch control-center-30-remove-warning-dialog.diff.
  Remove the warning dialog. Fixes bug #6215642
* Fri Feb 11 2005 - vinay.mandyakoppal@wipro.com
- Added patch control-center-29-default-browser.diff. Fixes the issue of changing the default browser. Fixes bug#6217648.
* Tue Jan 25 2005 - archana.shah@wipro.com
- Add patch control-center-28-a11y-issues.diff. Fixed a11y issues in keyboard
  accessibility capplet.
  Fixes #5028065
* Mon Dec 20 2004 - ghee.teo@sun.com
- Added Obsoletes/Provides for acme which has been merged into
  control-center in 2.6. Fixes 6211773.
* Thu Dec 09 2004 - arvind.samptur@wipro.com
- Add patch  control-center-27-settings-daemon-per-display.diff
  Starts g-s-d per display. fixes 4886754, 6195818. bugzilla id 94049
* Wed Dec 08 2004 - federic.zhang@sun.com
- Modified patch control-center-09-fontview-performance.diff
  The gettexted string shouldn't be freed.
* Tue Dec 07 2004 - padraig.obriain@sun.com
- Add patch control-center-26-window-props.diff to fix bug #6191372.
* Wed Nov 10 2004 - srirama.sharma@wipro.com
- Added patch control-center-25-volume-control.diff to control sound 
  using keyboard shortcut keys. Fixes Bug #6173921.
* Tue Nov 09 2004 - arvind.samptur@wipro.com
- Add patch to fix keybinding capplet behave right when caps lock 
  is on. Fixes #6180767
* Thu Nov 04 2004 - ciaran.mcdermott@sun.com
- Added control-center-23-g11n-potfiles.diff to update POTFILES.in 
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gnome-at-properties.1, gnome-font-viewer.1 man pages
* Tue Oct 19 2004 - arvind.samptur@wipro.com
- Forward port a patch from GNOME 2.0 to add custom keyboard
  shortcuts. Fixes #4878555
* Tue Oct 19 2004 - srirama.sharma@wipro.com
- Removing control-center-21-sun-volume-keys.diff as it should get added only for
  sparc. 
* Tue Oct 19 2004 - srirama.sharma@wipro.com
- Added control-center-21-sun-volume-keys.diff to associate the proper
  entries for the sunkeys (volume up, down and mute) to control volume.
  Fixes the Bug #6173921.   
* Mon Oct 18 2004 - leena.gunda@wipro.com
- Added control-center-20-build-typing-break.diff to check for correct
  screensaver library on solaris which is required to build typing-break.
  Fixes bug #5083708.
* Wed Oct 06 2004 - vinay.mandyakoppal@wipro.com
- Added control-center-19-logout-shortcut.diff Patch to remove the
  "/apps/gnome_settings_daemon/keybindings/power" and use
  "/apps/metacity/global_keybindings/logout" in the capplet.
  Fixes bug #5101706.
* Fri Sep 24 2004 - yuriy.kuznetsov@sun.com
- Added control-center-17-g11n-potfiles.diff
* Sat Sep 11 2004 - laca@sun.com
- Move Solaris specific LDFLAGS to the Solaris spec file
* Fri Sep 10 2004 - damien.carbery@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Aug 26 2004 - vinay.mandyakoppal@wipro.com
- Modified Patch control-center-03-help-links.diff to provide help
  link to Assistive Technology.
* Thu Aug 19 2004 - kaushal.kumar@wipro.com
- Added patch control-center-16-solaris-tar-command.diff to
  fix problem of directory option for Solaris tar.
* Fri Aug 06 2004 - takao.fujiwara@sun.com
- Updated control-center-07-g11n-potfiles.diff
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to control-center-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - stephen.browne@sun.com
- ported to rpm4/suse9.1, packaged missing files, added new devel pkg
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 - arvind.samptur@wipro.com
- Get the backgrounds.xml file in DATADIR/gnome-background-properities
  The Add Wallpaper file selector dialog will open $HOME/Document/Pictures
  or $HOME/Documents if pictures dir does not exist
* Mon Jun 14 2004 - leena.gunda@wipro.com
  Added control-center-14-customize-system-bell.diff and
  control-center-15-keyboard-layout.diff to fix bugs 5046592 and 5046596
  respectively.
* Tue Jun 8 2004 - federic.zhang@sun.com
- Added the missing %{_sysconfdir}/gnome-vfs-2.0/modules/*
* Mon May 31 2004 - padraig.obriain@sun.com
- Add control-center-12-accessible-names.diff. Backport of fix for
  bugzilla - bug #142402.
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Changed name of control-center-10-potfiles.diff to 
  control-center-10-g11n-potfiles.diff to comply with g11n naming standard.
  Patch control-center-10-g11n-potfiles.diff replaced 
  control-center-10-potfiles.diff
* Mon May 24 2004 -  muktha.narayan@wipro.com
- Added control-center-11-file-types-hang.diff to fix the file types capplet 
  hang when the requested icon file is not found. Bug #5028020.
  Uploaded the patch in bugzilla - bug #142894.
* Fri May 21 2004 -  hidetoshi.tajima@sun.com
- restore 09-potfiles.diff as 10-potfiles.diff.
* Fri May 21 2004 -  federic.zhang@sun.com
- Fixed bug 5050932: gnome-font-viewer takes too long time to view CJK fonts
  Added patch control-center-09-fontview-performance.diff and hope it can go
  upstream, see http://bugzilla.gnome.org/show_bug.cgi?id=142878, 
* Fri May 21 2004 -  federic.zhang@sun.com
- Fixed bug 5050926: Can't launch gnome-font-viewer in nautilus.
  Updated the spec file to include those files under /usr/lib/gnome-vfs-2.0/modules,
  /usr/share/application-registry and /usr/share/mime-info directory
* Fri May 14 2004 - kaushal.kumar@wipro.com
- Modified patch control-center-03-help-links.diff to 
  remove obsolete stuff.
  Removed patch control-center-09-window-properties-help.diff.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to control-center-l10n-po-1.1.tar.bz2
* Tue May 04 2004 - kaushal.kumar@wipro.com
- Added patch control-center-09-window-properties-help.diff to
  s/wgos*.xml/user-guide.xml.
* Mon Apr 26 2004 - glynn.foster@sun.com
- Bump to 2.6.1
* Wed Apr 21 2004 - vijaykumar.patwari@wipro.com
- Appended "desktop_gnome_peripherals_keyboard_xkb.schemas" file for
  schemas list.
* Fri Apr 16 2004 - vijaykumar.patwari@wipro.com
- Set the correct browser in command entry box.
* Tue Apr 6 2004 - glynn.foster@sun.com
- Bump to 2.6.0.3, and merge a bunch of the menu/title patches
  into one easy maintainable one. Patch the forte build issue
  on linux as well - we shouldn't special case this.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to control-center-l10n-po-1.0.tar.bz2
* Thu Mar  4 2004 - takao.fujiwara@sun.com
- Added control-center-09-g11n-schemas.diff to localize schemas.in
- Added control-center-10-g11n-potfiles.diff to fix 4957377
* Thu Feb 26 2004 - niall.power@sun.com
- add libexecdir to pick up missing files
* Thu Feb 26 2004 - matt.keenan@sun.com
- Update Distro, l10n to 0.8
* Tue Feb 24 2004 - niall.power@sun.com
- define correct auto*-jds and libtool-jds versions
* Tue Feb 24 2004 - niall.power@sun.com
- set and export ACLOCAL_FLAGS on linux to
  pick up necessary JDS_CBE  aclocal macros.
* Fri Feb 20 2004 - niall.power@sun.com
- Added build dependencies on jds CBE auto* tools
  and set PATH to pick up their location on linux
* Wed Feb 18 2004 - niall.power@sun.com
- Bump to 2.5.3
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 2.5.0
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Support keywords since
  we're moving away from the Extras menu.
* Tue Oct 21 2003 - glynn.foster@sun.com
- Add nautilus dependancy
* Mon Oct 19 2003 - glynn.foster@sun.com
- New tarball, bump version, reset release
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Tue Aug 05 2003 - glynn.foster@sun.com
- Close keybindings capplet on escape
* Tue Aug 05 2003 - glynn.foster@sun.com
- Add some metacity docs.
* Sat Aug 02 2003 - glynn.foster@sun.com
- Now we can theme X cursors
* Sat Aug 02 2003 - glynn.foster@sun.com
- Don't install gnomecc.desktop
* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu categorization cluepackets. Or something.
* Thu Jul 24 2003 - glynn.foster@sun.com
- Hide the password entry
* Tue Jul 22 2003 - glynn.foster@sun.com
- Change the window titles
* Mon Jul 21 2003 - glynn.foster@sun.com
- Reorder desktop preferences menu
* Thu Jul 17 2003 - ghee.teo@sun.com
- gnome-keybindings-properties uses the panel keys which are essential
  obsolete in the current release of GNOME. So replace these keys
  with the appropriate one that are appropriate in metacity.
* Thu Jul 17 2003 - glynn.foster@sun.com
- s/Files types and programs/File Associations
* Thu Jul 17 2003 - glynn.foster@sun.com
- Make sure the window icon lookup uses icon themes
* Tue Jul 15 2003 - michael.twomey@sun.com
- Backported the option to open the fonts folder from the fonts control panel.
* Wed Jul 09 2003 - michael.twomey@sun.com
- Added gnome-keyboard-layout to control centre.
* Fri Jul 03 2003 - markmc@sun.com
- Add correct location for new sound icon and 
  add a theme icon.
* Fri Jul 03 2003 - markmc@sun.com
- Install the .directory things
* Mon Jun 30 2003 - markmc@sun.com
- add display properties capplet
* Fri Jun 27 2003 - glynn.foster@sun.com
- bump the version on the control center tarball
* Wed Jun 25 2003 - markmc@sun.com
- add control-center-01-theme-failsafe.diff
* Wed May 14 2003 - Stephen.Browne@sun.com
- initial release
