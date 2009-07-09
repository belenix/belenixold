#
# spec file for package SUNWgnome-session
#
# includes module(s): gnome-session
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use gsession = gnome-session.spec

Name:                    SUNWgnome-session
Summary:                 GNOME session manager
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-vfs-root
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-component
Requires: SUNWgnome-panel
Requires: SUNWperl584usr
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWgnome-audio
Requires: SUNWgnome-base-libs
Requires: SUNWdesktop-cache
Requires: SUNWgnome-desktop-prefs
Requires: SUNWgnome-wm
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-desktop-prefs-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gsession.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/openwin/lib -R/usr/openwin/lib"
export CFLAGS="%optflags -I/usr/X11/include"
export RPM_OPT_FLAGS="$CFLAGS"

%gsession.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gsession.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/splash/flash.gif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gnome-session-%{gsession.version} README AUTHORS
%doc(bzip2) -d gnome-session-%{gsession.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-session/helpers/*
%{_libdir}/compiz-by-default
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (0755, root, other) %{_datadir}/gnome-session
%{_datadir}/gnome-session/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/session-properties*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/session-properties*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/session-properties*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/session-properties*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/session-properties*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/session-properties.svg
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/xsessions
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-session.schemas
%attr (0755, root, sys) %dir %{_sysconfdir}/xdg
%attr (0755, root, sys) %dir %{_sysconfdir}/xdg/autostart
%{_sysconfdir}/xdg/autostart/*.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Feb 11 2009 - matt.keenan@sun.com
- Add /usr/lib/compiz-by-default to %files section
* Mon Sep 08 2008 - ghee.teo@sun.com
- Removed ${_datadir}/autostart which is not being used according to spec.
  since autostart for GNOME is under ${_datadir}/gnome/autostart.
* Tue Aug 19 2008 - halton.huo@sun.com
- Add %attr (-, root, other) for subfolders under %{_datadir}/icons, this
  will resolve install conflict issue.
* Wed Jul 23 2008 - matt.keenan@sun.com
- Remove man5 from %files, default.session.5 removed from gnome-session
* Thu Jun 19 2008 - niall.power@sun.com
- Add %{_libdir}/gnome-session/helpers for 2.23.4 tarball.
- Add %{_datadir}/gnome-session fpr 2.23.4 tarball.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Add %{_datadir}/xsessions to %files for 2.21.5 tarball.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
- delete some unneeded env vars
* Wed Jun 06 2007 - irene.huang@sun.com
- remove %if %with_hal section because it is useless. 
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Sun Jan 28 2007 - add /usr/openwin/lib to library search path, needed
  for libXau on s10
* Mon Jan 22 2007 - damien.carbery@sun.com
- Add %{_datadir}/icons to %files for new gnome-session tarball.
* Tue Oct 31 2006 - takao.fujiwara@sun.com
- Added l10n package. Fixes 6488189.
* Mon Oct 30 2006 - Irene.Huang@sun.com
- move patch gnome-session-01-gnome-volcheck-default-session.diff
  to ../patches/
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Jul 26 2006 - brian.cameron@sun.com
- Only apply the gnome-volcheck-default-session.diff patch if HAL is not
  present on the system.  
* Fri Jul 28 2006 - damien.carbery@sun.com
- Remove l10n pkg as nothing installed.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-desktop-prefs/-devel for gnome-settings-daemon.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Fri Jun 23 2006 - Christopher.Hanna@sun.com
- Removed gnome-smproxy manpage because it is no longer needed
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Fri May 12 2006 - glynn.foster@sun.com
- Add dummy autostart location so that we at least have it on the
  system if people want to use it.
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-panel/-devel for gnome-desktop.
* Fri Feb 10 2006 - damien.carbery@sun.com
- Added BuildRequires lines to ensure it is built in the correct order.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Thu May 19 2005 - brian.cameron@sun.com
- Update to 2.10 and fix packaging.
* Tue Nov 16 2004 - laca@sun.com
- merged devel-share into share (included default.session(5) only)
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Sep 11 2004 - laca@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added gnome-session-remove.1 manpage
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files should be in a separate devel package
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004  damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Fri Mar 28 2004 - danek.duvall@sun.com
- Removed flash.gif from distribution
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Thu Mar 04 2004 - <laca@sun.com>
- fix 2 more gconf clashes
* Sat Feb 28 2004 - <niall.power@sun.com>
- fix gconf dir permissions (a+rX)
- remove clashing gconf.xml file
* Mon Feb 23 2004 - <niall.power@sun.com>
- install gconf schemas at end of install stage.
