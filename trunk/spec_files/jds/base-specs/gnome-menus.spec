# spec file for package gnome-menus
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# Owner: mattman
#
%include l10n.inc
Name:			gnome-menus
License:		LGPL
Group:			System/GUI/GNOME
Version:		2.26.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Implementation of Desktop Menu Specification for GNOME
Source:                 http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:		%{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# date:2006-04-28 owner:gman type:branding
Patch1:                 gnome-menus-01-quickstart.diff
# date:2006-04-28 owner:gman type:branding
Patch2:                 gnome-menus-02-application-submenu-rename.diff
# date:2006-04-28 owner:gman type:branding
Patch3:                 gnome-menus-03-preferences.diff
# date:2008-03-06 type:bug owner:mattman bugzilla:504600 bugster:6666675
Patch4:					gnome-menus-04-menu-monitor.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on
Prereq:                 /sbin/ldconfig
Prereq:                 GConf

%define gnome_vfs_version 2.8.2
%define pygtk2_version 2.7.0
%define python_version 2.4

Requires: pygtk2 >= %{pygtk2_version}
BuildRequires: pygtk2 >= %{pygtk2_version}
BuildRequires: gnome-vfs >= %{gnome_common_version}
BuildRequires: intltool

%description
This package implements the freedesktop.org desktop menu specification for the GNOME
desktop. Also contained in this package, are the menu layout configuration files, .directory
and assorted menu utility programs.

%package devel
Summary:      Implementation of Desktop Menu Specification for GNOME
Group:        System/Libraries/GNOME
Autoreqprov:  on
Requires:     %name = %version
Requires:     gnome-vfs-devel >= %{gnome_vfs_version}

%description devel
This package implements the freedesktop.org desktop menu specification for the GNOME
desktop. Also contained in this package, are the menu layout configuration files, .directory
and assorted menu utility programs.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
# Remove the changes to the default menu for Indiana, so 
# patch these only when building a Sun product.
%if %option_with_sun_branding
%patch1 -p1
%endif
%patch2 -p1
%if %option_with_sun_branding
%patch3 -p1
%endif
%patch4 -p1

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

intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
            --mandir=%{_mandir}
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
# FIXME: Giga-hack part 1 of 2 follows...
# file /etc/xdg/menus/applications.menu conflicts with desktop-data-SLES
# Only on SuSE Linux !!
%ifos linux
mv $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications.menu \
   $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications.menu.new
%endif

%post
/sbin/ldconfig
# FIXME: Giga-hack part 2 of 2 follows...
# file /etc/xdg/menus/applications.menu conflicts with desktop-data-SLES
MENU=/etc/xdg/menus/applications.menu
cp $MENU $MENU.SuSE
cp $MENU.new $MENU

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libgnome-menu.so.*
%{_datadir}/desktop-directories/*
%config %{_sysconfdir}/xdg/menus/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-menus
%{_libdir}/python2.4/

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*
%{_libdir}/libgnome-menu.so
%{_includedir}/gnome-menus/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Thu Jan 29 2009 - matt.keenan@sun.com
- Bump to 2.25.5
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Oct 29 2008 - matt.keenan@sun.com
- Remove indiana branding patch 05, #6765067
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Thu Sep 25 2008 - matt.keenan@sun.com
- Indiana branding, hide Devemoper Tools Menu #6752376
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 08 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Wed Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Fri Jun 06 2008 - jedy.wang@sun.com
- Fixes broken download link.
* Wed Jun 04 2008 - matt.keenan@sun.com
- Bump to 2.23.3.
* Thu May 29 2008 - matt.keenan@sun.com
- Bump to 2.23.1. Re-factor patches
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - brian.cameron@sun.com
- Bump to 2.22.0
* Thu Mar 6 2008 - matt.keenan@sun.com
- Add patch 04-menu-monitor.diff, fix bug 6666675 stopper
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5. Remove upstream patch, 04-gio.
* Tue Jan 08 2008 - damien.carbery@sun.com
- Add upstream patch, 04-gio, to use correct gio variable type.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Fri Nov 09 2007 - jedy.wang@sun.com
- Remove 04-support-alacarte.diff.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Don't delete *.pyc files - they are needed.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Replace 05-iconv-solaris patch with call to intltoolize.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Add patch 05-iconv-solaris to fix #467309.Modify intltool-merge.in to allow
  use of non-GNU iconv.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 16 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Thu Aug 16 2006 - harry.lu@sun.com
- add patch gnome-menus-04-support-alacarte.diff to fix bug 6460249.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Tue Aug 08 2006 - glynn.foster@sun.com
- Remove alacarte patch, and reorder.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed May 03 2006 - glynn.foster@sun.com
- Remove Accessibility submenu from preferences
* Fri Apr 28 2006 - glynn.foster@sun.com
- Add patch to rename some submenus, like
  Universal Access, and Developer Tools.
* Fri Apr 28 2006 - glynn.foster@sun.com
- Add quickstart.menu, along with ability to edit
  in the simple menu editor.
* Fri Apr 21 2006 - glynn.foster@sun.com
- Add alacarte patch which adds exec in terminal
  and no display options needed for the menu editor.
* Thu Apr 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Fri Jan 21 2006 - damien.carbery@sun.com
- Bump to 2.13.5.
* Thu Oct 27 2005 - laca@sun.com
- move python stuff from site-packages to vendor-packages
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Wed Aug 24 2005 - laca@sun.com
- remove upstream patch
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri May 13 2005 - brian.cameron@sun.com
- Add unisntalled-pc files since they are needed on Solaris to build.
* Tue May 10 2005 - glynn.foster@sun.com 
- Initial spec file for gnome-menus
