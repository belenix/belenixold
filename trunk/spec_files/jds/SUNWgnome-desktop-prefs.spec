#
# spec file for package SUNWgnome-desktop-prefs
#
# includes module(s): desktop-file-utils, control-center
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

# NOTE: You must set up the OpenGL symlinks before building SUNWcompiz:
#   #  /lib/svc/method/ogl-select start

%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use dfu = desktop-file-utils.spec
%use cc = control-center.spec
%use gsd = gnome-settings-daemon.spec

Name:                    SUNWgnome-desktop-prefs
Summary:                 GNOME desktop wide preference configuration tools
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
# date:2007-11-07 bugster:6531454 owner:dkenny type:bug
Patch1:                  control-center-01-passwd-in-terminal.diff
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWdbus-glib
Requires: SUNWevolution-data-server
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-audio
Requires: SUNWgnome-desktop-prefs-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-component
Requires: SUNWgnome-panel
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-libs
Requires: SUNWgnome-media
Requires: SUNWgnome-vfs
Requires: SUNWgnome-wm
Requires: SUNWlibcanberra
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlxml
Requires: SUNWdesktop-cache
Requires: SUNWxwxft
Requires: SUNWbash
%if %with_hal
Requires: SUNWhal
%endif
# Depend on SUNWxorg-mesa on x86 for OpenGL support.
%ifnarch sparc
Requires: SUNWxorg-mesa
%endif

BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibcanberra-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-wm-devel
%if %option_without_fox
BuildRequires: SUNWxorg-headers
%endif
%if %option_with_dt
BuildRequires: SUNWtltk
%endif
BuildRequires: SUNWevolution-data-server-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-file-mgr-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWdbus-glib-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package  devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-desktop-prefs
Requires: SUNWgamin
                                                                                
%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%ifnarch sparc
# Testing that the OpenGL headers and libs are installed.
# If this fails it means that the build machine is not properly configured
test -f /usr/X11/include/GL/glx.h || {
  echo "Missing OpenGL headers. Stopping."
  echo "As root, run: \"/lib/svc/method/ogl-select start\""
  false
  }
test -f /usr/X11/lib/modules/extensions/libglx.so  || {
  echo "Missing OpenGL libraries. Stopping."
  echo "As root, run: \"/lib/svc/method/ogl-select start\""
  false
  }
%endif
rm -rf %name-%version
mkdir %name-%version
%dfu.prep -d %name-%version
%cc.prep -d %name-%version
%gsd.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -
cd %{_builddir}/%name-%version/%{cc.name}-%{cc.version}
%patch1 -p1
cd ..

%build
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/X11/include -DGNOME_DESKTOP_USE_UNSTABLE_API"
export RPM_OPT_FLAGS="$CFLAGS"
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
export PKG_CONFIG_PATH="../gnome-settings-daemon-%{gsd.version}/data:%{_pkg_config_path}"
#FIXME: This stuff should be fixed in the component or the configure script
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -lfreetype -lresolv -lgthread-2.0"
export EMACS=no

%dfu.build -d %name-%version
%gsd.build -d %name-%version
%cc.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%dfu.install -d %name-%version
export PATH=%{_builddir}/%name-%version/desktop-file-utils-%{dfu.version}/src:$PATH
%cc.install -d %name-%version
%gsd.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove %{_datadir}/mime until clash with SUNWgnome-vfs resolved.
rm -r $RPM_BUILD_ROOT%{_datadir}/mime

# put real version number in gnome-control-center.1
perl -pi -e 's/%%{cc_version}/%{cc.version}/g' $RPM_BUILD_ROOT%{_mandir}/man1/gnome-control-center.1

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/window-manager-settings/*.so
%{_libdir}/gnome-settings-daemon-2.0
%{_libexecdir}/gnome-settings-daemon
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%{_datadir}/applications/mimeinfo.cache
%if %is_s10
%dir %attr (-, root, other) %{_datadir}/control-center
%{_datadir}/control-center/*
%else
%{_datadir}/gnome-control-center
%{_datadir}/gnome-settings-daemon
%endif
%{_datadir}/desktop-directories
%{_datadir}/dbus-1
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/cursor-fonts
%{_datadir}/gnome/help/*/C
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/omf/*/*-C.omf
#%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc desktop-file-utils-%{dfu.version}/AUTHORS
%doc desktop-file-utils-%{dfu.version}/README
%doc(bzip2) desktop-file-utils-%{dfu.version}/COPYING
%doc(bzip2) desktop-file-utils-%{dfu.version}/ChangeLog
%doc(bzip2) desktop-file-utils-%{dfu.version}/NEWS
%doc gnome-control-center-%{cc.version}/AUTHORS
%doc gnome-control-center-%{cc.version}/capplets/about-me/AUTHORS
%doc gnome-control-center-%{cc.version}/README
%doc(bzip2) gnome-control-center-%{cc.version}/COPYING
%doc(bzip2) gnome-control-center-%{cc.version}/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/about-me/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/accessibility/at-properties/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/appearance/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/common/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/default-applications/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/display/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/keybindings/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/keyboard/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/mouse/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/network/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/capplets/windows/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/help/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/libslab/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/libwindow-settings/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/po/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/shell/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/typing-break/ChangeLog
%doc(bzip2) gnome-control-center-%{cc.version}/NEWS
%doc gnome-settings-daemon-%{gsd.version}/AUTHORS
#%doc gnome-settings-daemon-%{gsd.version}/plugins/sound/libsounds/README
%doc(bzip2) gnome-settings-daemon-%{gsd.version}/COPYING
%doc(bzip2) gnome-settings-daemon-%{gsd.version}/ChangeLog
%doc(bzip2) gnome-settings-daemon-%{gsd.version}/po/ChangeLog
%doc(bzip2) gnome-settings-daemon-%{gsd.version}/NEWS
#%doc(bzip2) gnome-settings-daemon-%{gsd.version}/plugins/sound/libsounds/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_keybindings.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_screensaver.schemas
%{_sysconfdir}/gconf/schemas/apps_gnome_settings_daemon_xrandr.schemas
%{_sysconfdir}/gconf/schemas/control-center.schemas
%{_sysconfdir}/gconf/schemas/gnome-settings-daemon.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_font_rendering.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_keybindings.schemas
%{_sysconfdir}/gconf/schemas/fontilus.schemas
%{_sysconfdir}/xdg

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Tue Jan 13 2009 - matt.keenan@sun.com
- Remove sound capplet reference as removed from 2.25.3 tarball
* Tue Jan 06 2009 - takao.fujiwara@sun.com
- Modify pkgmap for omf.
* Thu Sep 25 2008 - matt.keenan@sun.com
- Update copyright
* Wed Sep 17 2008 - halton.huo@sun.com
- Add script to replace real control-center version number in
  gnome-control-center.1
- Add %attr (-, root, other) for subfolders under %{_datadir}/icons
* Tue Aug 05 2008 - damien.carbery@sun.com
- Add apps_gnome_settings_daemon_xrandr.schemas to %post and %files. Remove
  hack that created mimeinfo.cache - it is not needed because gnome-vfs is
  obsolete now.
* Mon Aug 04 2008 - ghee.teo@sun.com
- Removed control-center-01-solaris-printmgr.diff now that the Presto's
  print manager is integrated into vermillion.
* Sat Jul 26 2008 - damien.carbery@sun.com
- Create mimeinfo.cache because build breaking with /dev/null in proto. Remove
  fontilus.schemas from %post and %files as it is not installed. Also remove
  %{_sysconfdir}/gnome-vfs-2.0 from %files as it is not installed either.
* Fri Jul 25 2008 - damien.carbery@sun.com
- Update %files, removing %{_libdir}/gnome-vfs-2.0/modules/*.so and
  %{_libdir}/nautilus.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Remove themus.schemas as it is no longer installed.
* Wed May 21 2008 - damien.carbery@sun.com
- Add 'Requires: SUNWxorg-mesa' to base package to fix #6705123.
* Wed Apr 16 - damien.carbery@sun.com
- Add Requires SUNWgamin to devel package. Mentioned in #6688818.
* Mon Apr 07 - damien.carbery@sun.com
- Change OpenGL check to only happen on x86.
* Wed Apr 02 - damien.carbery@sun.com
- Copy in changes from gnome-2-20 branch: break the build if the openGL headers
  and libraries are not present on the machine.
* Wed Mar 12 2008 - damien.carbery@sun.com
- Update %files for new tarball.
* Tue Feb 26 2008 - brian.cameron@sun.com
- Now gnome-settings-daemon depends on gnome-desktop in the SUNWgnome-panel
  package.  So add this dependency.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Remove obsolete sparc patches, 02-sun-volume-keys and 03-sun-help-key.
  Renumber rest.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus-bindings/-devel; Update %files for new location
  of plugins.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Add -DGNOME_DESKTOP_USE_UNSTABLE_API to CFLAGS to get it to build.
* Wed Jan 23 2008 - damien.carbery@sun.com
- Set PKG_CONFIG_PATH to find the gnome-settings-daemon uninstalled.pc file.
* Wed Jan 23 2008 - darren.kenny@sun.com
- Move gnome-settings-daemon into it's own spec file to match project
  structures.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Nov 07 2007 - darren.kenny@sun.com
- Add new patch control-center-04-passwd-in-terminal.diff
- This is a tempoary fix for Bug#6531454 - using gnome-terminal & passwd - the
  correct fix depends on ON RFE 6627014 being implemented.
* Tue Oct 30 2007 - laca@sun.com
- s/without_java/with_java
* Mon Oct  1 2007 - laca@sun.com
- move export EMACS=no to %build from %prep and delete emacs dir from %files
* Mon Oct  1 2007 - damien.carbery@sun.com
- Add %{_datadir}/emacs to %files.
* Fri Sep 28 2007 - laca@sun.com
- add support to build on FOX instead of Nevada X
- disable emacs support
* Wed Sep 05 2007 - darren.kenny@sun.com
- Bump to 2.19.92
- Update files sections for new version.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Thu Mar 15 2007 - damien.carbery@sun.com
- Add Requires SUNWbash after check-deps.pl run.
* Wed Feb 14 2007 - damien.carbery@sun.com
- Update %files for new tarball.
* Thu Feb  8 2007 - takao.fujiwara@sun.com
- Update control-center-01-solaris-printmgr.diff for SUN_BRANDING
* Sun Jan 28 2007 - laca@sun.com
- update dir attributes so they work on both s10 and nevada
* Wed Jan 24 2007 - damien.carbery@sun.com
- Add %{_datadir}/icons to %files.
* Tue Dec 19 2006 - ghee.teo@sun.com
- Replace the script, solaris-printmgr-wrappper to use gksu instead of sticking
  with the old CDE action script.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Remove schema file from %preun root and %files as it is no longer in the 
  control-center module. Remove icons dir from %files as they are not installed.
* Fri Oct 20 2006 - damien.carbery@sun.com
- Remove SUNWhalh BuildRequires because header files are in SUNWhea in snv_51.
* Mon Sep 18 2006 - brian.cameron@sun.com
- Add SUNWhalh BuildRequires
* Tue Sep 05 2006 - brian.cameron@sun.com
- Now check for HAL so we can use --enable/disable-hal as appropriate in 
  the control-center.spec file.  Remove panel dependency now that we no
  longer link against libxklavier.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Wed Jul 12 2006 - laca@sun.com
- set correct attributes for mimeinfo.cache, fixes #6431057
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Fri Jun 23 2006 - christopher.hanna@sun.com
- removed manpages not needed: gnome-file-types-properties and gnome-settings-daemon
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Apr 18 2006 - damien.carbery@sun.com
- Add desktop-directories directory.
* Wed Apr 05 2006 - glynn.foster@sun.com
- Remove screensaver hack since xscreensaver installs into the
  right location.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Add X packages to Requires after running check-deps.pl script.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Jan 19 2006 - brian.cameron@sun.com
- Added %{_datadir}/gnome-default-applications to share package.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Thu Dec 01 2005 - damien.carbery@sun.com
- Add Build/Requires SUNWevolution-data-server/-devel for libebook dependency.
* Tue Jul 19 2005 - damien.carbery@sun.com
- Add BuildRequires SUNWtltk because build was breaking without that package.
* Wed Jul 13 2005 - brian.cameron@sun.com
- Added SUNWgnome-panel dependency
* Thu Jun 02 2005 - brian.cameron@sun.com
- Bumped to 2.10, fixed packaging.
* Tue Oct 26 2004 - srirama.sharma@wipro.com
- Added patch control-center-03-sun-help-key.diff (to sparc only) to bind the 
  Sun help key to launch default help with Sun tpe Keyboards. Fixes the bugtraq
  bug#6182405.
* Tue Oct 19 2004 - srirama.sharma@wipro.com
- Added patch control-center-02-sun-volume-keys.diff (to sparc only) to bind 
  Sun keys Volume up, Volume Down and Volume Mute to control volume with Sun type
  keyboards. Fixes bugtraq bug#6173921.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Sep 11 2004 - laca@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added gnome-at-properties.1, gnome-font-viewer.1 manpages
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Fri Aug  6 2004 - danek.duvall@sun.com
- Add support for running the Solaris Print Manager (as root)
* Tue Jul 13 2004 - damien.carbery@sun.com
- Create symlink to screensaver-properties.desktop in capplets dir to fix
  bug 5070633.
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Tue Mar 02 2004 - niall.power@sun.com
- add {_libdir}/window-manager-settings
* Mon Mar 01 2004 - laca@sun.com
- remove libxklavier
- add dependency on SUNWgnome-wm
* Mon Feb 23 2004 - Niall.Power@sun.com
- install gconf schemas at the end of the install
  stage.
* Thu Feb 19 2004 - Niall.Power@sun.com
- initial Solaris spec file
