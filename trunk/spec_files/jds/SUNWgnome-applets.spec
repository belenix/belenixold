#
# spec file for package SUNWgnome-applets
#
# includes module(s): gnome-applets, quick-lounge-applet
#		      gnome-netstatus, deskbar-applet
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: migi
#
%include Solaris.inc
%use gapplets = gnome-applets.spec
%use qlounge = quick-lounge-applet.spec
%use gnetstatus = gnome-netstatus.spec
%use deskbar_applet = deskbar-applet.spec

Name:                    SUNWgnome-applets
Summary:                 GNOME panel applets
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-character-map-devel
BuildRequires: SUNWgnome-doc-utils
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-python-desktop-devel
BuildRequires: SUNWpython-setuptools
BuildRequires: SUNWsolnm
BuildRequires: SUNWarc
BuildRequires: SUNWevolution-data-server-devel
BuildRequires: SUNWlibgtop
BuildRequires: SUNWdbus-python24-devel
Requires: SUNWgnome-python-desktop
Requires: SUNWgnome-character-map
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWlxml
Requires: SUNWgnome-component
Requires: SUNWlibpopt
Requires: SUNWlibms
Requires: SUNWpng
Requires: SUNWlibgtop
Requires: SUNWdbus-python24

%if %option_without_fox
%ifarch i386
Requires: SUNWxorg-xkb
BuildRequires: SUNWxorg-xkb
%endif
%endif

%package -n SUNWgnome-fun-applets
Summary:                 %{summary} - amusements
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-fun-applets-root
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SUNWdesktop-cache

%package -n SUNWgnome-fun-applets-root
Summary:                 %{summary} - amusements - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-internet-applets
Summary:                 %{summary} - internet
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWPython

%package -n SUNWgnome-intranet-applets
Summary:                 %{summary} - intranet
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-intranet-applets-root
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SUNWdesktop-cache

%package -n SUNWgnome-intranet-applets-root
Summary:                 %{summary} - intranet - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-mm-applets
Summary:                 %{summary} - multimedia
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-mm-applets-root
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-media
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SUNWdesktop-cache

%package -n SUNWgnome-mm-applets-root
Summary:                 %{summary} - multimedia - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-utility-applets
Summary:                 %{summary} - utility
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-python-desktop
Requires: SUNWgnome-utility-applets-root
Requires: SUNWgnome-applets
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-character-map
Requires: SUNWgnome-component
Requires: SUNWgnome-vfs
Requires: SUNWevolution-data-server
Requires: SUNWlxml
Requires: SUNWlibms
Requires: SUNWdesktop-cache
Requires: SUNWPython
Requires: SUNWhal

%package -n SUNWgnome-utility-applets-root
Summary:                 %{summary} - utility - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-utility-applets-devel
Summary:                 %{summary} - utility - development files
SUNW_BaseDir:            %{_basedir}
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
%gapplets.prep -d %name-%version
%qlounge.prep -d %name-%version
%gnetstatus.prep -d %name-%version
%deskbar_applet.prep -d %name-%version
chmod -R u+w %{_builddir}/%name-%version

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -L/usr/X11/lib -R/usr/X11/lib -lX11"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%gapplets.build -d %name-%version

export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

%qlounge.build -d %name-%version
%gnetstatus.build -d %name-%version
%deskbar_applet.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gapplets.install -d %name-%version
%qlounge.install -d %name-%version
%gnetstatus.install -d %name-%version
%deskbar_applet.install -d %name-%version

# Remove the invest-chart files as it is not in the UI spec (#6488895).
rm $RPM_BUILD_ROOT%{_bindir}/invest-chart

chmod 0644 $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/C/*.xml

#rm -r $RPM_BUILD_ROOT%{_prefix}/var

# Never install English locales because should support full functions
# on English locales as same as Solaris. See SUNWzz-gnome-l10n.spec.
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/en_GB
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/en_GB
rm -r $RPM_BUILD_ROOT%{_datadir}/omf/*/*-en_GB.omf

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/[a-c]*/[a-z]*
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/deskbar/[a-z]*
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/[e-z]*/[a-z]*
rm -r $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -r $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SUNWgnome-fun-applets
%restart_fmri icon-cache gconf-cache

%post -n SUNWgnome-intranet-applets
%restart_fmri icon-cache gconf-cache

%post -n SUNWgnome-utility-applets
%restart_fmri icon-cache gconf-cache

%post -n SUNWgnome-mm-applets
%restart_fmri gconf-cache

%files
%doc -d gnome-applets-%{gapplets.version} README stickynotes/README cpufreq/README geyes/README mini-commander/README trashapplet/README gkb-new/README null_applet/README AUTHORS gweather/AUTHORS cpufreq/AUTHORS geyes/AUTHORS multiload/AUTHORS mini-commander/AUTHORS drivemount/AUTHORS gkb-new/AUTHORS accessx-status/AUTHORS mixer/AUTHORS modemlights/AUTHORS COPYING-DOCS accessx-status/COPYING COPYING MAINTAINERS
%doc(bzip2) -d gnome-applets-%{gapplets.version} ChangeLog stickynotes/ChangeLog charpick/ChangeLog gswitchit/ChangeLog gweather/ChangeLog cpufreq/ChangeLog cpufreq/help/ChangeLog geyes/docs/ChangeLog geyes/ChangeLog multiload/ChangeLog mini-commander/ChangeLog drivemount/ChangeLog drivemount/help/ChangeLog trashapplet/docs/ChangeLog trashapplet/ChangeLog gkb-new/ChangeLog accessx-status/docs/ChangeLog accessx-status/ChangeLog battstat/ChangeLog null_applet/ChangeLog mixer/ChangeLog modemlights/ChangeLog invest-applet/ChangeLog po/ChangeLog NEWS geyes/NEWS mini-commander/NEWS
%doc gnome-netstatus-%{gnetstatus.version}/README
%doc gnome-netstatus-%{gnetstatus.version}/NEWS
%doc gnome-netstatus-%{gnetstatus.version}/AUTHORS
%doc gnome-netstatus-%{gnetstatus.version}/MAINTAINERS
%doc gnome-netstatus-%{gnetstatus.version}/COPYING
%doc(bzip2) gnome-netstatus-%{gnetstatus.version}/ChangeLog
%doc(bzip2) gnome-netstatus-%{gnetstatus.version}/po/ChangeLog
%doc(bzip2) gnome-netstatus-%{gnetstatus.version}/help/ChangeLog
%doc quick-lounge-applet-%{qlounge.version}/README
%doc quick-lounge-applet-%{qlounge.version}/AUTHORS
%doc quick-lounge-applet-%{qlounge.version}/NEWS
%doc(bzip2) quick-lounge-applet-%{qlounge.version}/help/ChangeLog
%doc(bzip2) quick-lounge-applet-%{qlounge.version}/ChangeLog
%doc(bzip2) quick-lounge-applet-%{qlounge.version}/po/ChangeLog
%doc deskbar-applet-%{deskbar_applet.version}/README
%doc deskbar-applet-%{deskbar_applet.version}/NEWS
%doc deskbar-applet-%{deskbar_applet.version}/AUTHORS
%doc deskbar-applet-%{deskbar_applet.version}/MAINTAINERS
%doc deskbar-applet-%{deskbar_applet.version}/COPYING
%doc(bzip2) deskbar-applet-%{deskbar_applet.version}/ChangeLog
%doc(bzip2) deskbar-applet-%{deskbar_applet.version}/po/ChangeLog
%doc(bzip2) deskbar-applet-%{deskbar_applet.version}/help/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_NullApplet_Factory.server
%{_libdir}/null_applet

%files -n SUNWgnome-fun-applets
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_GeyesApplet.server
%{_libexecdir}/geyes_applet2
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/geyes/C
%{_datadir}/omf/geyes/geyes-C.omf
%{_datadir}/gnome-2.0/ui/GNOME_GeyesApplet.xml
%{_datadir}/gnome-applets/geyes
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/gnome-eyes-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/gnome-eyes-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/gnome-eyes-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/gnome-eyes-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/gnome-eyes-applet.*
%{_datadir}/xmodmap

%files -n SUNWgnome-fun-applets-root
%defattr(-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/geyes.schemas

%files -n SUNWgnome-internet-applets
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_GWeatherApplet_Factory.server
%{_libdir}/bonobo/servers/Invest_Applet.server
%{_libdir}/bonobo/servers/GNOME_GtikApplet.server
%{_libdir}/invest-applet
%{_libdir}/python?.?/vendor-packages/invest
%{_libexecdir}/gweather-applet-2
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gweather/C
%{_datadir}/gnome/help/invest-applet/C
%{_datadir}/gnome-applets/invest-applet
%{_datadir}/omf/gweather/gweather*-C.omf
%{_datadir}/omf/invest-applet/invest-applet*-C.omf
%{_datadir}/gnome-2.0/ui/GNOME_GWeatherApplet.xml
%{_datadir}/gnome-2.0/ui/Invest_Applet.xml
%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/invest-48_neutral.png
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/48x48/apps/invest-applet.png
%{_datadir}/icons/hicolor/16x16/apps/invest-applet.png
%{_datadir}/icons/hicolor/scalable/apps/invest-applet.svg
%{_datadir}/icons/hicolor/22x22/apps/invest-applet.png

%files -n SUNWgnome-intranet-applets
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_MailcheckApplet_Factory.server
%{_libdir}/bonobo/servers/GNOME_Panel_NowApplet.server
%{_libdir}/bonobo/servers/GNOME_NetstatusApplet_Factory.server
%{_libdir}/bonobo/servers/GNOME_Panel_WirelessApplet.server
%{_libexecdir}/gnome-netstatus-applet
%{_libexecdir}/gnome-netstatus-wifi-info
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-netstatus/C
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/omf/gnome-netstatus/*-C.omf
#%{_datadir}/gnome-2.0/ui/GNOME_Panel_NowApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_NetstatusApplet.xml
%{_datadir}/gnome-netstatus

%files -n SUNWgnome-intranet-applets-root
%defattr(-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%dir %attr(0755, root, sys) %{_sysconfdir}/security
%{_sysconfdir}/gconf/schemas/netstatus.schemas
%config %class(rbac) %attr (0644, root, sys) %{_sysconfdir}/security/exec_attr
%config %class(rbac) %attr (0644, root, sys) %{_sysconfdir}/security/prof_attr

%files -n SUNWgnome-mm-applets
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_MixerApplet.server
%{_libdir}/bonobo/servers/GNOME_CDPlayerApplet.server
%{_libexecdir}/mixer_applet2
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/mixer_applet2/C
%{_datadir}/omf/mixer_applet*/mixer_applet*-C.omf
%{_datadir}/gnome-2.0/ui/GNOME_MixerApplet.xml

%files -n SUNWgnome-mm-applets-root
%defattr(-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/mixer.schemas

%files -n SUNWgnome-utility-applets
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/trashapplet
%{_libdir}/bonobo/servers/GNOME_CharpickerApplet.server
%{_libdir}/bonobo/servers/GNOME_MiniCommanderApplet.server
%{_libdir}/bonobo/servers/GNOME_StickyNotesApplet.server
%{_libdir}/bonobo/servers/GNOME_AccessxStatusApplet.server
%{_libdir}/bonobo/servers/GNOME_QuickLoungeApplet_Factory.server
%{_libdir}/bonobo/servers/GNOME_Panel_TrashApplet.server
%{_libdir}/bonobo/servers/GNOME_MultiLoadApplet_Factory.server
%{_libdir}/bonobo/servers/Deskbar_Applet.server
%{_libdir}/bonobo/servers/GNOME_WebEyes.server
%{_libdir}/bonobo/servers/GNOME_BattstatApplet.server
%{_libdir}/deskbar-applet
%{_libdir}/python?.?/vendor-packages/deskbar
%{_libexecdir}/charpick_applet2
%{_libexecdir}/stickynotes_applet
%{_libexecdir}/accessx-status-applet
%{_libexecdir}/quick-lounge-applet
%{_libexecdir}/multiload-applet-2
%{_libexecdir}/battstat-applet-2
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/gnome-applets/builder
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/char-palette/C
%{_datadir}/gnome/help/deskbar/C
%{_datadir}/gnome/help/stickynotes_applet/C
%{_datadir}/gnome/help/accessx-status/C
%{_datadir}/gnome/help/quick-lounge/C
%{_datadir}/gnome/help/multiload/C
%{_datadir}/gnome/help/trashapplet/C
%{_datadir}/gnome/help/battstat/C
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/accessx-status-applet
%{_datadir}/pixmaps/stickynotes
%{_datadir}/omf/char-palette/char-palette-C.omf
%{_datadir}/omf/deskbar/deskbar-C.omf
%{_datadir}/omf/stickynotes_applet/stickynotes_applet-C.omf
%{_datadir}/omf/accessx-status/accessx-status-C.omf
%{_datadir}/omf/trashapplet/trashapplet-C.omf
%{_datadir}/omf/multiload/multiload-C.omf
%{_datadir}/omf/battstat/battstat-C.omf
%{_datadir}/gnome-2.0/ui/GNOME_CharpickerApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_StickyNotesApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_AccessxApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_QuickLoungeApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_Panel_TrashApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_MultiloadApplet.xml
%{_datadir}/gnome-2.0/ui/GNOME_BattstatApplet.xml
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/gnome-sticky-notes-applet.*
%{_datadir}/icons/hicolor/16x16/apps/deskbar-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/gnome-sticky-notes-applet.*
%{_datadir}/icons/hicolor/22x22/apps/deskbar-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/gnome-sticky-notes-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/gnome-sticky-notes-applet.*
%{_datadir}/icons/hicolor/32x32/apps/deskbar-applet.*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/ax-applet*
%{_datadir}/icons/hicolor/48x48/apps/deskbar-applet*
%{_datadir}/icons/hicolor/48x48/apps/quick-lounge*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/deskbar-applet*
%{_datadir}/icons/hicolor/scalable/apps/gnome-sticky-notes-applet.*
%{_datadir}/quick-lounge-applet
%{_datadir}/deskbar-applet

%files -n SUNWgnome-utility-applets-root
%defattr(-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/charpick.schemas
%{_sysconfdir}/gconf/schemas/stickynotes.schemas
%{_sysconfdir}/gconf/schemas/quick-lounge.schemas
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
%{_sysconfdir}/gconf/schemas/multiload.schemas
%{_sysconfdir}/gconf/schemas/battstat.schemas
%{_sysconfdir}/sound/events/battstat_applet.soundlist

%files -n SUNWgnome-utility-applets-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/deskbar-applet.pc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/[a-c]*/[a-z]*
%{_datadir}/gnome/help/deskbar/[a-z]*
%{_datadir}/gnome/help/[e-z]*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

# Put back in when localized help is delivered from l10n 
# %{_datadir}/omf/gnome-desktop/*-[a-z][a-z].omf
# %{_datadir}/omf/gnome-desktop/*-[a-z][a-z]_*.omf
# %{_datadir}/omf/gnome-feedback/*-[a-z][a-z].omf
# %{_datadir}/omf/gnome-feedback/*-[a-z][a-z]_*.omf
# %{_datadir}/omf/gnome-netstatus/*-[a-z][a-z].omf
# %{_datadir}/omf/gnome-netstatus/*-[a-z][a-z]_*.omf

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Apr 02 2009 - brian.cameron@sun.com
- Add SUNWhal as a dependency since the Battery Status applet uses it.
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/lib/invest-applet (SUNWgnome-internet-applets) requires
  /usr/bin/i86/isapython2.4 which is found in SUNWPython, add the
  dependency.
- Since /usr/lib/deskbar-applet/deskbar-applet (SUNWgnome-utility-applets)
  requires /usr/bin/i86/isapython2.4 which is found in SUNWPython, add the
  dependency.
* Tue Feb 24 2009 - dave.lin@sun.com
- Fixed %{_datadir}, %{_datadir}/doc attribute issue.
* Wed Feb 18 2009 - Michal.Pryc@Sun.Com
- Fixed %files section for new quick-lounge-applet
* Tue Feb 17 2009 - Matt.Keenan@sun.com
- Bump tarball to 2.25.90, and add back mixer applet files
* Fri Jan 30 2009 - Michal.Pryc@Sun.Com
- Removed lines to remove all drivemount files, this is now done
  through reworked patch: gnome-applets-01-disable-drivemount.diff
- Temporary commented lines for mixer applet. The mixer applet will be available
  in the new tarball of gnome-applets.
* Mon Sep 15 2008 - darren.kenny@sun.com
- Removed icon dirs not being used any more.
- Added line to remove empty drivemount directory that was causing build
  error.
* Mon Sep 08 2008 - dave.lin@sun.com
- Fixed /usr/share/icons/... attribute issue for SUNWgnome-internet-applets
* Fri Aug 22 2008 - darren.kenny@sun.com
- Update for additional netstatus wireless files (icons and helper).
* Fri May 30 2008 - damien.carbery@sun.com
- Update %files for new tarballs.
* Fri May 16 2008 - jedy.wang@sun.com
- Remove panel-default-setup-laptop.entries and corresponding post and preun
  script to fix 6703518.
* Thu Feb 28 2008 - damien.carbery@sun.com
- Update %files for new tarballs.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Remove Requires: SUNWgnome-internet-applets-root from
  SUNWgnome-internet-applets list.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Remove SUNWgnome-internet-applets-root and SUNWgnome-internet-applets-devel
  packages as the libgweather module is in SUNWgnome-panel now.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu Jan  3 2008 - laca@sun.com
- use includes instead of inline scripts
* Thu Oct 11 2007 - brian.cameron@sun.com
- Fix packaging so that invest applet's python code gets installed.
  Fixes bug #6502277.
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps; make xorg-xkb dep dependent upon nevada X build
* Thu Sep 27 2007 - laca@sun.com
- add postrun script that rebuilds the icon cache for each package that
  installs icons
* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of %{_prefix}/var dir as it's no longer created.
* Tue Aug 07 2007 - damien.carbery@sun.com
- Update l10n %files for new deskbar-applet tarball.
* Wed Aug 01 2007 - damien.carbery@sun.com
- Update %files for new tarball.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Sun Apr 15 2007 - jedy.wang@sun.com
- Ship battstat applet on sparc.
* Wed Mar 07 2007 - damien.carbery@sun.com
- Delete en_GB locale files in %install as it breaks SUNWzz-gnome-l10n build. 
* Mon Feb 19 2007 - damien.carbery@sun.com
- Add now applet back to %files.
* Sun Feb 18 2007 - glynn.foster@sun.com
- Update the install location for the python files into vendor-packages.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Rename %{_datadir}/quick-lounge to quick-lounge-applet.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Add deskbar help files to %files.
* Wed Jan 03 2007 - damien.carbery@sun.com
- Changes in %files for 2.17.1 update. Remove GNOME_KeyboardApplet.server as the
  base patch that creates it has been removed. Added %{_datadir}/xmodmap dir.
* Fri Nov 03 2006 - damien.carbery@sun.com
- Remove the 'rm' of invest-big.png as it is referenced in %files.
* Thu Nov 02 2006 - damien.carbery@sun.com
- Remove the invest-chart files as it is not in the UI spec (#6488895).
* Thu Oct 19 2006 - damien.carbery@sun.com
- Remove obsolete 'rm -r' calls from %install.
* Tue Oct 17 2006 - glynn.foster@sun.com
- Remove webeyes from the build. deskbar-applet is the natural
  (and better) replacement. Compatibility is preserved through 
  user migration to the new applet.
* Mon Sep 04 2006 - brian.cameron@sun.com
- Remove libical since we no longer ship the now applet.  Also
  remove -g from CFLAGS.  Not good to have on by default for
  performance.
* Fri Aug 25 2006 - damien.carbery@sun.com
- More updates to %files for new deskbar-applet tarball.
* Thu Aug 24 2006 - damien.carbery@sun.com
- Minor update to %files.
* Wed Aug 23 2006 - damien.carbery@sun.com
- Update %files for new icons.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Add invest-applet to internet-applets package.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Thu Aug 03 2006 - damien.carbery@sun.com
- Add 'multiload' files back to %files.
* Tue Aug 01 2006 - darren.kenny@sun.com
- Add SUNWlibgtop build dependency for multiload
* Sat Jul 29 2006 - damien.carbery@sun.com
- Remove 'multiload' files from %files.
* Fri Jul 28 2006 - damien.carbery@sun.com
- Remove 'gtik' stuff and add deskbar stuff to %files. Fix dir perms.
* Fri Jul 28 2006 - darren.kenny@sun.com
- Add multiload applet.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Sat Jul 15 2006 - glynn.foster@sun.com
- Remove gswitchit and friends.
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Wed Mar 15 2006 - damien.carbery@sun.com
- Add to Build/Requires after running check-deps.pl.
* Wed Mar 15 2006 - glynn.foster@sun.com
- Add deskbar-applet to the utility package.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Remove mini-commander stuff that is gone.
* Fri Jan 06 2006 - damien.carbery@sun.com
- Add internet-applets-devel for gweather files.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Wed Oct 19 2005 - damien.carbery@sun.com
- Add SUNWgnome-doc-utils build dependency for /usr/bin/xml2po.
* Tue Sep 13 2005 - laca@sun.com
- remove unpackaged files or add to %files
* Wed Jul 13 2005 - brian.cameron@sun.com
- Split from SUNWgnome-panel.spec.
