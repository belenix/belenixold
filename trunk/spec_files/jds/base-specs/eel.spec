#
# spec file for package eel
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen
Name:         eel
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Eazel Extensions Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/eel/2.26/eel-%{version}.tar.bz2
URL:          http://www.gnome.org
#owner:stephen date:2005-05-13 type:bug bugster:6184582 bugzilla:466762
Patch1:       eel-01-multibyte-bookmark-menu.diff	
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libgnomeui_version 2.6.0
%define librsvg_version 2.5.0
%define libxml2_version 2.6.7
%define gnome_vfs_version 2.6.0
%define gail_version 1.6.3
%define GConf_version 2.6.1
%define gnome_desktop_version 2.1.4

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: librsvg-devel >= %{librsvg_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: librsvg >= %{librsvg_version}
Requires: gail >= %{gail_version}
Requires: gnome-desktop >= %{gnome_desktop_version}

%description
This library extends the Gtk+ library with some useful routines for
applications like Nautilus.

%package devel
Summary:      Eazel Extensions Development Library
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     gnome-vfs-devel >= %{gnome_vfs_version}
Requires:     GConf-devel >= %{GConf_version}

%description devel
This library extends the Gtk+ library with some useful routines for
applications like Nautilus.

%prep
%setup -q
%patch1 -p1

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

aclocal $ACLOCAL_FLAGS
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/*.la
                                                                                                                                                             
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr (-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/eel-2

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Removed upstreamed patch 02-uninstalled-pc.diff.
* Thu Feb 26 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Fri Jan 23 2009 - brian.cameron@sun.com
- Add eel-02-uninstalled-pc.diff patch to fix bug in the file.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.1
* Sun Sep 28 2008 - patrick.ale@gmail.com
- Correct download URL
* Wed Sep 24 2008 - matt.keenan@sun.com
- Bump to 2.24.0
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Mon Mar 31 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5. Call aclocal and autoconf to pick up the modified intltool.m4.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.3.
* Wed Nov 08 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
- Remove upstream patch, 02-assertion. Renumber remainder.
* Tue Aug 08 2006 - padraig.obriain@sun.com
- Bump to 2.15.91.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Web Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
- Remove upstream patch, 04-a11y-330995.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
- Add upstream patch, 04-a11y-330995. Fixes 330995.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Tue Jan 17 2006 - glynn.foster@sun.com
- Bump to 2.13.4
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Tue Aug 23 2005 - damien.carbery@sun.com
- Add gnome-desktop build and install dependencies.
* Mon Aug 15 2005 - damien.carbery@sun.com	
- Bump to 2.11.91.
* Wed Aug 03 2005 - laca@sun.com
- remove upstream patch cancel-rename.diff
* Fri May 13 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.1 
* Fri May 13 2005 - vijaykumar.patwari@wipro.com
- Added patch eel-05-cancel-rename.diff, this patch does not allow
  timeout dialog to pop up if gnome-auth-mananger dialog is visible.
  Fixex bug#6264644.
* Wed Mar 23 2005 - muktha.narayan@wipro.com
- Added patch eel-04-gok-crash.diff to fix nautilus crash when 
  folder is opened with gok. Fixes bug #6234837.
* Tue Feb 15 2005 - hidetoshi.tajima@sun.com
- Added patch eel-03-popup-menu-i18n.diff to translate "Select All"
  and "Input Methods" messages in nautilus. Fixes bug #5072488.
* Tue Jan 25 2005 - muktha.narayan@wipro.com
- Added patch eel-02-assertion.diff to fix assertion failure
  messages in nautilus. Fixes bug #4899270.
* Mon Dec 08 2004 - suresh.chandrasekharan@sun.com
- Added patch #01 to fix the cutoff of long multibyte directory
  bookmarks. Fixes bug #6184582. Applied to linux trunk only.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to eel-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to eel-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - <matt.keenan@sun.com>
- Bump to 2.6.1
* Thu Apr 15 2004 - <glynn.foster@sun.com>
- Bump to 2.6.0
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to eel-l10n-po-1.0.tar.bz2
* Tue Mar 16 2004 - <glynn.foster@sun.com>
- Bump to 2.5.91
* Wed Mar 10 2004 - <niall.power@sun.com>
- Bump to version 2.5.90 and update dependency pkg versions to something
  a bit more recent.
- Remove patches, they are merged into the lastest version.
* Wed Feb 18 2004 - <matt.keenan@sun.com>
- Updated l10n tarball to 0.8
* Tue Feb 17 2004 - <stephen.browne@sun.com>
- new tarball, removed patch #3
* Thu Feb 12 2004 - <niall.power@sun.com>
- added patches 01, 02 and 03: compilation fixes, add a -uninstalled-pc file,
  fix errors in Makefile.am
- autotoolize the build stage
* Wed Jan 07 2004 - <niall.power@sun.com>
- Updated to 2.5.4
* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Updated to 2.5.3
* Mon Oct 13 2003 - <stephen.browne@sun.com>
- Updated to 2.4 
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Thu Jul 03 2003 - Niall.Power@sun.com
- version 2.2.4
* Thu May 01 2003 - Niall.Power@sun.com
- initial Sun release.
