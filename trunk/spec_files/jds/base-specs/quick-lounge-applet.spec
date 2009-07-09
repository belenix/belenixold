#
# spec file for package quick-lounge-applet
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# Owner: migi
#
Name:         quick-lounge-applet
License:      GPL
Group:        Productivity/Graphics/Viewers
Version:      2.13.2
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Quick Lounge Panel Applet
Source:       http://ftp.gnome.org/pub/GNOME/sources/quick-lounge-applet/2.13/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/quick-lounge-applet
Autoreqprov:  on

%define gnome_vfs_version 2.4.0
%define libgnome_version 2.4.0
%define libgnomeui_version 2.4.0.1
%define gnome_panel_version 2.4.0
%define gnome_desktop_version 2.4.0
%define gnome_menus_version 2.12.0

Requires:      gnome-vfs >= %{gnome_vfs_version}
Requires:      libgnome >= %{libgnome_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      gnome-panel >= %{gnome_panel_version}
Requires:      gnome-desktop >= %{gnome_desktop_version}
Requires:      gnome-menus >= %{gnome_menus_version}
BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires: gnome-menus-devel >= %{gnome_menus_version}

%description
Quick Lounge Applet allows you to group launchers on your panel.

%prep
%setup -q

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

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL  

rm -rf $RPM_BUILD_ROOT/var


%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="quick-lounge.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done


%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_datadir}/pixmaps/*.png
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/quick-lounge/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome/help/quick-lounge/*
%{_datadir}/omf/%{name}/*.omf
%{_libexecdir}/*

%changelog
* Wed Feb 18 2009 - Michal.Pryc@Sun.Com
- Removed quick-lounge-applet-01-remove-ditem.diff: fixed upstream
- bumped to 2.13.2
* Fri Jan 30 2009 - Michal.Pryc@Sun.Com
- added quick-lounge-applet-01-remove-ditem.diff 
  bugzilla:559584, defect.opensolaris.org:5976

* Tue Apr 15 2008 - damien.carbery@sun.com
- Bump to 2.12.5. Remove upstream patch 01-fixdirectory.

* Fri Oct 19 2007 - brian.cameron@sun.com
- Add patch quick-lounge-applet-01-fixdirectory.diff to address bugster bug
  #6616094.

* Tue Aug 28 2007 - damien.carbery@sun.com
- Add intltoolize call.

* Wed Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.12.4. Remove all patches as they are all upstream.

* Fri Oct 12 2006 - glynn.foster@sun.com
- Add patch to fix bugzilla #319050 and other issues on 
  multihead/xinerama.

* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff

* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.1.

* Sun Sep 18 2005 - glynn.foster@sun.com
- Fix up the help patch so we build.

* Tue Aug 30 2005 - glynn.foster@sun.com
- Add patch to build against newer gmenu

* Tue Aug 30 2005 - glynn.foster@sun.com
- Add gnome-menus dependency.

* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.10.1.

* Thu Jun 16 2005 - matt.keenan@wipro.com
- Bump to 2.10.1 Remove/Add/Realign patches

* Wed Feb 02 2005 - srirama.sharma@wipro.com
- Added quick-lounge-applet-09-help-from-launcher-dialog.diff
  to launch help when user clicks on the help button in the "Add Launcher"
  dialog.
 
* Thu Jan 20 2005 - srirama.sharma@wipro.com
- Added quick-lounge-applet-08-launch_default_help.diff
  to make sure that default help gets launched, not always yelp.
  Fixes bug #5097716

* Wed Jan 19 2005 - srirama.sharma@wipro.com
- Added quick-lounge-applet-07-min_max_update.diff to
  set the minimum and maximum values properly in the 
  preferences dialog. Fixes Bug #5028045.
  committing on behalf of dinoop.thomas@wipro.com

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
                                                                                
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR

* Mon Sep 20 2004 ciaran.mcdermott@sun.com
- Added quick-lounge-applet-05-g11n-alllinguas.diff to support hu

* Wed Aug 25 2004 Kazuhiko.Maekawa@sun.com
- Updated l10n help tarball name for Cinnabar

* Thu Aug 05 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Mon Jul 19 2004 - niall.power@sun.com
- synced with HEAD, fixed up packaging

* Thu Jul 08 2004 - dermot.mccluskey@sun.com
- fixed typo in patch 04 (p->P)

* Thu Jul 08 2004 - dermot.mccluskey@sun.com
- fixed typo in patch 04 (p->P)

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed Jun 25 2004 - arvind.samptur@wipro.com
- Add patch from Vinay M R  to fix quicklounge to be usable as root 

* Wed Jun 23 2004 - arvind.samptur@wipro.com
- Add patch from Vinay M R  to fix the properites dialog crash

* Wed Jun 09 2004 - kazuhiko.maekawa@sun.com
- Remove l10n online help patch(#2). Changes are now included in base source.

* Wed Jun 02 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to quick-lounge-applet-l10n-po-1.1.tar.bz2

* Fri Apr 30 2004 - muktha.narayan@wipro.com
- add libexecdir to %files.  

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris

* Wed Apr 07 2004 - laca@sun.com
- add patch 03 to add the Xlibs to LDFLAGS.
- add --libexecdir=%{_libexecdir} to configure args
* Tue Apr 06 2004 - matt.keenan@sun.com
- Remove *.so* from files, as none delivered anymore

* Tue Apr 06 2004 - matt.keenan@sun.com
- Forgot to rename patches in spec file

* Mon Apr 05 2004 - matt.keenan@sun.com
- Bump to 2.1.1
- Remove 3 patches and re-align the remaining two

* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to quick-lounge-applet-l10n-po-1.0.tar.bz2

* Thu Mar 04 2004 - <leena.gunda@wipro.com>
- Added quick-lounge-applet-05-display-help.diff to display help with 
  correct section id.

* Thu Feb 05 2004 - <matt.keenan@sun.com>
- Upgrade tarball to 2.0.3 for Cinnabar, add l10n docs/help

* Fri Jan 09 2004 - <matt.keenan@sun.com>
- Patch for deprecated widgets compiling

* Tue Oct 14 2003 - <matt.keenan@sun.com>
- Upgrade tarball to 2.0.1 for QS

* Wed Oct 01 2003 - <matt.keenan@sun.com>
- #4930772 and #4930772

* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la

* Fri Jun 30 2003 - Glynn Foster <glynn.foster@sun.com>
- Add in the bonobo ui xml menus to the %files directive

* Wed May 15 2003 - Glynn Foster <glynn.foster@sun.com>
- initial Sun release
