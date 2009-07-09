#
# spec file for package gnome-settings-daemon.
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:         gnome-settings-daemon
License:      GPL
Group:        System/GUI/GNOME
Version:      2.25.92
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The GNOME Settings Daemon
Source:       http://ftp.gnome.org/pub/GNOME/sources/gnome-settings-daemon/2.25/gnome-settings-daemon-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# TODO - l10n extraction from existing gnome-control-center.
#Source1:     %{name}-po-sun-%{po_sun_version}.tar.bz2
# date:2006-12-07 owner:dcarbery type:bug bugzilla:383356
Patch1:       gnome-settings-daemon-01-no-libgnomekbd.diff
# date:2008-11-07 owner:jedy type:bug bugster:6767860 bugzilla:170175
Patch2:       gnome-settings-daemon-02-sleep-action.diff
# date:2004-10-19 owner:dkenny type:feature bugster:4878555
Patch3:       gnome-settings-daemon-03-custom-keybinding.diff
# date:2006-06-30 owner:stephen type:feature
Patch4:       gnome-settings-daemon-04-trusted-extensions.diff
# date:2006-08-28 owner:pwade type:bug bugster:6327546
Patch5:       gnome-settings-daemon-05-sticky-timeout.diff
# date:2008-01-24 owner:dkenny type:bug bugzilla:511733
Patch6:       gnome-settings-daemon-06-xft.diff
# date:2008-01-24 owner:erwannc type:bug doo:146 bugster:6717847 
Patch7:      gnome-settings-daemon-07-default-dpi-and-aa.diff
# date:2008-09-23 owner:dkenny type:branding
Patch8:      gnome-settings-daemon-08-find-xrdb.diff
# date:2009-03-27 owner:bewitche type:bug bugzilla:576535
Patch9:      gnome-settings-daemon-09-notification-closed.diff
# date:2009-04-02 owner:lin type:branding bugzilla:6746963
Patch10:     gnome-settings-daemon-10-default-keybinding.diff
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
Summary:       Development files for the GNOME Settings Daemon
Group:         Development/Libraries/GNOME
Requires:      %name = %version-%release

%description devel
This package contains the files need for development of GNOME control center capplets

%prep
%setup -q
# TODO - l10n extraction from existing gnome-control-center.
#%if %build_l10n
#bzcat %SOURCE1 | tar xf -
#cd po-sun; make; cd ..
#%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# Rename dir so that #include does not have to change on gnome-control-center.
# Combines with patch mv-src-dir.diff (see bugzilla 511820).
##mv src gnome-settings-daemon

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
bash -x %SOURCE1 --enable-copyright
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
rm $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-2.0/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-2.0/*.la
                                                                               
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
* Thu Apr 02 2009 - lin.ma@sun.com
- Add patch 10 for fix bugzilla 6746963.
* Mon Mar 30 2009 - chris.wang@sun.com
- Add patch 09 to fix bugzilla 576535 notification crash on close
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Feb 10 2009 - matt.keenan@sun.com
- Bump to 2.25.90
* Tue Jan 13 2009 - matt.keenan@sun.com
- Bump to 2.25.3
* Thu Jan 08 2008 - jedy.wang@sun.com
- Update patch comments for 02-sleep-action.diff.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Nov 13 2008 - jedy.wang@sun.com
- Remove 02-logout-shortcut.diff and create 02-sleep-action.diff.
* Fri Sep 26 2008 - brian.cameron@sun.com
- Fix download link.
* Thu Sep 25 2008 - matt.keenan@sun.com
- Bump to 2.24.0 to get correct copyright info
* Tue Sep 23 2008 - darren.kenny@sun.com
- Add patch gnome-settings-daemon-08-find-xrdb.diff to handle issue where xrdb
  isn't on default user path - specific to Solaris so is branding patch.
* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Wed Aug 20 2008 - darren.kenny@sun.com
- Attempt to fix gnome-settings-daemon-05-sticky-timeout.diff to apply.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Fri Jul 25 2008 - damien.carbery@sun.com
- Bump to 2.23.5. Remove upstream patch, 07-uninstalled. Renumber
  08-use-default-dpi to 07.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4. Remove upstream patch, 08-esound-prefix-branding.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3. Remove upstream patch, 08-gnomeinit. Renumber remainder.
* Fri May 30 - darren.kenny@sun.com
- Bump to 2.23.1.1.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Fri May 16 2008 - stephen.browne@sun.com
- remove conditional build of tx patch
* Thu May 06 2008 - lin.ma@sun.com
- Fix g-s-d so that it can find /usr/lib/esd.
* Thu May 01 2008 - brian.cameron@sun.com
- Fix g-s-d so that it will start up if the user doesn't have a writable
  $HOME directory via patch gnome-settings-daemon-08-gnomeinit.diff.  This
  is needed for the new GDM rewrite, which needs to run g-s-d and does not
  have a writable $HOME directory.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Mar 3 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Add patch 07-uninstalled to correct Cflags path in the uninstalled.pc.in file.  Correct path to the plugins.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91. Remove upstream patches 07-uninstalled and 09-mv-src-dir.
  Remove 06-relocate-plugins as the change is implemented in configure.
* Fri Feb 01 2008 - damien.carbery@sun.com
- Bump to 2.21.90.2.
* Tue Jan 29 2008 - brian.cameron@sun.com
- Bump to 2.21.90.1.
* Thu Jan 24 2007 - damien.carbery@sun.com
- Add patch 10-mv-src-dir to rename 'src' to 'gnome-settings-daemon' to
  simplify uninstalled building. Bugzilla 511820.
* Thu Jan 24 2007 - darren.kenny@sun.com
- Add patch 09-xft to fix bugzilla 511733.
* Wed Jan 23 2007 - damien.carbery@sun.com
- Add patch 08-uninstalled to create an uninstalled.pc.in file to permit
  building.
* Wed Jan 23 2007 - darren.kenny@sun.com
- Initial SPEC file for new g-s-d project.
  Extracted from control-center project.
- Removed gnome screensaver patch which isn't needed (and was actually
  ineffective). 
