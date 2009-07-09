#
# spec file for package deskbar-applet
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# Owner: migi
#
Name:			deskbar-applet
License:		GPL
Group:			System/GUI/GNOME
Version:		2.26.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Deskbar Applet
Source:                 http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
# date:2003-10-17 owner:gman type:branding
Patch1:                 deskbar-applet-01-webeyes-compatibility.diff
# date:2008-04-15 owner:mattman type:bug bugster:6436071 bugzilla:353412
Patch2:         deskbar-applet-02-multihead-support.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on
Prereq:                 /sbin/ldconfig
Prereq:                 GConf

%define pygtk2_version 2.7.0
%define python_version 2.4
%define gnome_desktop_version 2.10
%define gnome_python 2.10
%define gnome_python_desktop 2.13
%define evolution_data_server_version 1.5

Requires: pygtk2 >= %{pygtk2_version}
Requires: gnome-python >= %{gnome_python_version}
Requires: gnome-python-desktop >= %{gnome_python_desktop_version}
Requires: gnome-desktop >= %{gnome_desktop_version}
Requires: evolution-data-server >= %{evolution_data_server_version}
BuildRequires: pygtk2-devel >= %{pygtk2_version}
BuildRequires: gnome-python-devel >= %{gnome_python_version}
BuildRequires: gnome-python-desktop-devel >= %{gnome_python_desktop_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires: evolution-data-server-devel >= %{evolution_data_server_version}
BuildRequires: intltool

%description
Search applet for the GNOME panel.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

for po in po/*.po; do
  dos2unix -ascii $po $po
done

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
aclocal $ACLOCAL_FLAGS -I ./m4
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --disable-scrollkeeper		\
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

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="deskbar-applet.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/bonobo/servers
%{_libdir}/pkgconfig
%{_libdir}/deskbar-applet
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/deskbar-applet/
%{_datadir}/locale
%{_datadir}/pixmaps
%{_libdir}/python2.4/

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Thu Mar 05 2009 - Matt.Keenan@Sun.Com
- Uncoomment deskbar-applet-02-multihead-support.diff reworked
* Mon Feb 16 2009 - Matt.Keenan@sun.com
- Bump to 2.25.90
* Fri Jan 30 2009 - Michal.Pryc@Sun.Com
- Commented deskbar-applet-02-multihead-support.diff, needs rework.
* Thu jan 22 2009 - brian.cameron@sun.com
- Add call to libtoolize.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Sun Sep 28 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Wed Sep 03 2008 - christian.kelly@sun.com
- Rework patch #2.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Wed Jul 23 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Tue May 29 2008 - matt.keenan@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.1.
* Tue Apr 15 2008 - matt.keenan@sun.com
- Patch for multihead support
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.1.
* Thu Feb 28 2008 - damien.carbery@sun.com
- Reorder aclocal params to pick up patched intltool.m4 instead of the one
  in the deskbar-applet area.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.1.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1. Remove upstream patches, 02-iconv-solaris and 03-add-newline.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Don't delete *.pyc files - they are needed.
* Thu Sep 27 2007 - brian.cameron@sun.com
- Add patch deskbar-applet-03-add-newline.diff which fixes a bug that
  was causing you to be unable to add the deskbar applet to the panel.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.1.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Aug 07 2007 - damien.carbery@sun.com
- Bump to 2.19.6.1. Remove upstream patch, 02-evo-handler.
* Tue Aug 07 2007 - damien.carbery@sun.com
- Remove patch 01-browser-locations because it is obsolete. Renumber rest.
- Add upstream patch, 02-evo-handler, to fix build error.
* Tue Aug 07 2007 - damien.carbery@sun.com
- Bump to 2.19.6. Disable patch1 01-browser-locations because we don't install
  mozilla or firefox under /usr/sfw.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Sun Apr 08 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.17.93.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Thu Jan 11 2007 - damien.carbery@sun.com
- Bump to 2.17.5.1.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Disable scrollkeeper in configure as files not needed.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Tue Oct 24 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Oct 17 2006 - glynn.foster@sun.com
- Add a patch for webeyes compatibility, a recently
  EOL'd component.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 29 2006 - damien.carbery@sun.com
- Bump to 2.15.92.1.
* Thu Aug 24 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Fri Jul 28 2006 - damien.carbery@sun.com
- Bump to 2.15.90.1. dos2unix the po files.
* Wed Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.5.
* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 2.14.1.1.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Fri Mar 17 2006 - glynn.foster@sun.com
- Fix up the browser locations. Patch from Rich Lowe.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Mar 1 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Wed Mar 1 2006 - glynn.foster@sun.com
- Initial version

