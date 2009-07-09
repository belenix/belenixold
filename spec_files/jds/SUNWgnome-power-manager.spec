#
# spec file for package SUNWgnome-power-manager
#
# includes module(s): gnome-power-manager
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc
%use gpm = gnome-power-manager.spec
%define with_xmlto %(test -x /usr/bin/xmlto && echo 1 || echo 0)

Name:                    SUNWgnome-power-manager
Summary:                 GNOME Power Manager utilities for desktop users
Version:                 %{gpm.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-base-libs
BuildRequires:           SUNWgnome-base-libs-devel
Requires:                SUNWgnome-libs
BuildRequires:           SUNWgnome-libs-devel
Requires:                SUNWdbus
BuildRequires:           SUNWdbus-devel
Requires:                SUNWdbus-glib
BuildRequires:           SUNWdbus-glib-devel
Requires:                SUNWhal
Requires:                SUNWgnome-panel
BuildRequires:           SUNWgnome-panel-devel
Requires:                SUNWgnome-media
BuildRequires:           SUNWgnome-media-devel
Requires:                SUNWdesktop-cache
Requires:                %{name}-root
Requires:                SUNWxdg-utils

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
%gpm.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%gpm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gpm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Replace debian format man pages with solaris-specical man pages.
rm -rf $RPM_BUILD_ROOT%{_mandir}/
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Disable gnome-inhibit applet. Because it's unable to inhibit all suspend 
# actions, e.g. some suspend actions are done by powerd daemon on Solaris.
rm -rf  $RPM_BUILD_ROOT%{_bindir}/gnome-inhibit-applet
rm -rf  $RPM_BUILD_ROOT%{_datadir}/gnome-power-manager/gpm-inhibit-test.glade
rm -rf  $RPM_BUILD_ROOT%{_datadir}/gnome-2.0/ui/GNOME_InhibitApplet.xml
rm -rf  $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/GNOME_InhibitApplet.server

# Move scripts from /usr/bin to /usr/lib/gnome-power-manager as part of libexec directory.
mkdir $RPM_BUILD_ROOT%{_libdir}/gnome-power-manager
mv $RPM_BUILD_ROOT%{_bindir}/gnome-power-*.sh $RPM_BUILD_ROOT%{_libdir}/gnome-power-manager

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/gnome-power-manager/[a-z][a-z]
rm $RPM_BUILD_ROOT%{_datadir}/omf/gnome-power-manager/gnome-power-manager-[a-z][a-z].omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gnome-power-manager-%{gpm.version} README AUTHORS
%doc(bzip2) -d gnome-power-manager-%{gpm.version} COPYING NEWS ChangeLog po/ChangeLog help/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%{_bindir}/*
%{_libdir}/gnome-*-applet
%{_libdir}/gnome-power-manager/gnome-power-*.sh
%{_libdir}/bonobo/servers/GNOME_BrightnessApplet.server
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/autostart/gnome-power-manager.desktop
%{_datadir}/gnome/help/gnome-power-manager/C/*
%{_datadir}/gnome-2.0/ui/GNOME_BrightnessApplet.xml
%{_datadir}/gnome-power-manager/*
%if %with_xmlto
%{_datadir}/doc/gnome-power-manager-*/*
%endif
%{_datadir}/dbus-1/services/gnome-power-manager.service
%{_datadir}/omf/gnome-power-manager/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-power-*.desktop
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-power-manager.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-power-manager/[a-z]*/*
%{_datadir}/omf/gnome-power-manager/*-[a-z][a-z].omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Thu Feb 19 2009 - jedy.wang@sun.com
- Change owner to jedy.
* Thu Mar 27 2008 - simon.zheng@sun.com
- Add copyright.
* Wed Mar 05 2008 - simon.zheng@sun.com
- Remove help file when build_l10n option is false.
* Tue Mar 04 2008 - takao.fujiwara@sun.com
- Modify %files l10n entry to add l10n helps.
* Mon Mar 03 2008 - simon.zheng@sun.com
- Add an option to build doc if xmlto is installed.
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version number.
* Wed Feb 27 2008 - damien.carbery@sun.com
- Add SUNWgnome-media/-devel to dependency list 
  as gpm requires gstreamer.
* Fri Feb 15 2008 - simon.zheng@sun.com
- Delete redundant statement.
* Thu Feb 14 2008 - simon.zheng@sun.com
- Add manpage.
- Use install script.
- Correct the package name.
* Thu Feb 14 2008 - jeff.cai@sun.com
- Move to gnome spec repository from sourceforge.
* Wed Dec 26 2007 - simon.zheng@sun.com
- Let patch gnome-power-manager-08-brightness-install.diff 
  do moving applets.
* Fri Dec 21 2007 - simon.zheng@sun.com
- Remove redundant CFLAGS and LDFLAGS.
* Mon Dec 17 2007 - simon.zheng@sun.com
- Move gnome-brightness-applet into /usr/lib.
* Thu Dec 12 2007 - simon.zheng@sun.com
- Disable gnome-inhibit-applet, remove relevant files.
* Tue Nov 27 2007 - simon.zheng@sun.com
- Removed man installation dir.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Fix %files.
* Thu Nov 08 2007 - trisk@acm.jhu.edu
- Ensure doc dir is not installed
* Wed Nov 7 2007 - simon.zheng@sun.com
- Fix %post icon-cache.
* Thu Oct 25 2007 - simon.zheng@sun.com
- Delete installation files under /usr/share/docs.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to search paths
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Fix %post/%preun typos
* Thu Aug 30 2007 - trisk@acm.jhu.edu
- Add missing doc dir
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Include l10n files.
* Tue Mar 27 2007 - simon.zheng@sun.com
- Create
