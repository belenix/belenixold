#
# spec file for package gnome-desktop
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:         gnome-desktop
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Desktop Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:      blueprint-extra-icons.tar.bz2
Source2:      gnome-feedback.xml
Source3:      sun-gnome-version.xml
Source4:      jds-64.gif
Source5:      header-bg-jds1.png
Source6:      gnome-cleanup
Source7:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source8:                 l10n-configure.sh
%endif
# date:2004-03-22 type:branding owner:gman
Patch1:       gnome-desktop-01-jds-about-branding.diff
# date:2005-04-08 type:bug owner:gman
Patch2:       gnome-desktop-02-hicolor-icons.diff
# date:2006-06-30 type:feature owner:stephen
Patch3:       gnome-desktop-03-trusted-extensions.diff
# date:2008-05-29 type:bug owner:mattman bugster:6695640 bugzilla:104753
Patch4:       gnome-desktop-04-gnome-about-label-size.diff
# date:2008-08-14 type:bug owner:dkenny bugster:6732089
Patch5:       gnome-desktop-05-randr-xerror.diff
# date:2008-10-03 type:bug owner:dkenny bugster:6754036
Patch6:       gnome-desktop-06-xrandr-probing.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libwnck_version 2.4.0
%define libgnomeui_version 2.2.0
%define startup_notification_version 0.5
%define popt_version 1.6.4
%define libgnome_version 2.4.0
%define scrollkeeper_version 0.3.12
 
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: popt-devel >= %{popt_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: gnome-doc-utils

%description
libgnome-desktop is a private library containing API that are 
not considered stable.

gnome-desktop also contains icons and documents used in the 
base GNOME Desktop.

%package devel
Summary:      GNOME Desktop Library
Group:        Development/Libraries/GNOME
Requires:     %name = %version-%release
Requires:     libgnomeui-devel >= %{libgnomeui_version}
Requires:     libgnome-devel >= %{libgnome_version}

%description devel
libgnome-desktop is a private library containing API that are 
not considered stable.

%prep
%setup -q
%if %option_with_sun_branding
bzcat %SOURCE1 | tar xvf -
## 2.17.5 update: the gnome-feedback sub-module has been removed.
##cp %SOURCE2 desktop-docs/gnome-feedback/C/gnome-feedback.xml
cp %SOURCE3 gnome-version.xml.in.in
cp %SOURCE4 gnome-about/gnome-64.gif
%endif
%if %build_l10n
bzcat %SOURCE7 | tar xf -
cd po-sun; make; cd ..
%endif
%patch4 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
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

gnome-doc-common
gnome-doc-prepare
libtoolize --force
gtkdocize
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE8 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f

%ifos solaris
release_version="GNOME %{version} Desktop"
%else
release_version=`head -1 /etc/sun-release`
%endif
#FIXME: Disable scrollkeeper for now
CFLAGS="$RPM_OPT_FLAGS"		\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --localstatedir=/var/lib \
	    --mandir=%{_mandir} \
	    --with-gnome-distributor="Sun Microsystems, Inc." \
	    --with-gnome-distributor-version="$release_version" \
	    --disable-scrollkeeper
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
%if %option_with_sun_branding
install --mode=0644 %SOURCE5 $RPM_BUILD_ROOT%{_datadir}/gnome-about/headers
%endif
install --mode=0755 %SOURCE6 $RPM_BUILD_ROOT%{_bindir}
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/gnome-suse.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_bindir}/*
%{_datadir}/applications/
%{_datadir}/gnome-about/*.png
%{_datadir}/gnome-about/*.xml
%{_datadir}/gnome-about/headers/header-bg-*.png
%{_datadir}/gnome/help/*
%{_datadir}/omf/*
%{_datadir}/pixmaps/
%{_datadir}/icons/
%{_libdir}/libgnome-desktop-2.so.*

%files devel
%defattr (-, root, root)
%{_includedir}/gnome-desktop-2.0/libgnome/*.h
%{_includedir}/gnome-desktop-2.0/libgnomeui/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libgnome-desktop-2.so

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Added 07-gtkdoc-rebase.diff to fix GTKDOC_REBASE issue.
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.90
* Thu Jan 29 2009 - matt.keenan@sun.com
- Bump to 2.25.5
* Wed Jan 07 2009 - christian.kelly@sun.com
- Unbump to 2.25.2 because of build issues.
* Sat Dec 27 2008 - dave.lin@sun.com
- Bump to 2.25.3
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Oct  3 2008 - darren.kenny@sun.com
- Add patch gnome-desktop-06-xrandr-probing.diff for bug#6754036 to reduce the
  number of Xrandr related probes being generated when there is a change in
  the number of screens, etc.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92, remove patches/gnome-desktop-05-union-name.diff.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 21 2008 - jedy.wang@sun.com
- Remove option_with_sun_branding.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Thu Aug 14 2008 - darren.kenny@sun.com
- Add new patch gnome-desktop-06-randr-xerror.diff to fix bugster:6732089
  where g-settings-d was crashing due to an XError. This is really a
  workaround until we figure out why XRRSetResolution is working yet still
  generating an XError, which doesn't make sense.
* Thu Aug 08 2008 - damien.carbery@sun.com
- Bump to 2.23.6. Open a new bug for patch5 because most of it was already
  upstream and the original bug marked as a duplicate.
* Thu Jul 24 2008 - matt.keenan@sun.com
- patch5 : fixes empty struct and unnamed unions sun studio compiler issues.
* Wed Jul 23 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Thu May 29 2008 - matt.keenan@sun.com
- Re-apply patch 04-gnome-about-label-size.diff, fix bugster:6695640
  bugzilla:104753, incorrectly removed because of gpatch error
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2. Remove upstream patches, 04-gnome-aobut-utf-8 and
  05-gnome-about-label-size.
* Fri May 16 2008 - stephen.browne@sun.com
- remove conditional build of tx patch
* Wed May 07 2008 - matt.keenan@sun.com
- new patch 05-gnome-about-label-size.diff, fix bugster:6695640
  bugzilla:104753
* Thu Apr 29 2008 - matt.keenan@sun.com
- fix bugster:6674496 bugzilla:530382, new patch 04-gnome-about-utf-8.diff
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - brian.cameron@sun.com
- Bump to 2.22.0
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92. Remove upstream patch, 04-fixcrash.
* Tue Feb 26 2008 - brian.cameron@sun.com
- Add patch gnome-desktop-04-fixcrash.diff to fix 
  P1 bug 6667885.  This problem was causing gnome-settings-daemon
  to crash on login.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Wed Dec 19 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Fri Sep 28 2007 - laca@sun.com
- disable the jds branding patch when jds branding is not requested
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3.1.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 06 2007 - damien.carbery@sun.com
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.92. Remove obsolete patch, 04-gok-menu. Patched code gone.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Sun Jan 28 2007 - laca@sun.com
- add %if %build_tjds guard around tjds patch so we can build without trusted
  jds support
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5. Comment out the copying of gnome-feedback.xml because the
  destination dir in the source area has been removed.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Thu Jun  8 2006 - laca@sun.com
- Delete gnome-suse.png from the pkgs
* Thu Apr 13 2006 - damien.carbery@sun.com
- Bump to 2.14.1.1.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Wed Jan 18 2006 - brian.cameron@sun.com
- Calling glib-gettextize also fixes the infinite loop and is better than
  patching the Makefile to not build the po directory.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Add intltoolize call.
- Add patch to fix infinite loop in configure.
* Mon Jan 16 2006 - damien.carbery@sun.com
- Bump to 2.13.5. Increment displayed version.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
* Thu Dec 22 2005 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Wed Aug 24 2005 - laca@sun.com
- add gnome-doc-utils dependency and run gnome-doc-prepare to fix
  doc makefiles.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.90.
* Fri Jun 24 2005 - balamurali.viswanathan@wipro.com
- Add patch pkgconfig.diff that adds the required libs explictly
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Fri Apr 08 2005 - glynn.foster@sun.com
- Add some hicolor icons. Should really be fixed in the code though.
* Fri Jan 28 2005 - balamurali.viswanathan@wipro.com
- Modified patch gnome-desktop-01-jds-about-branding.diff so that Sun and gnome
  contributors are shown alphabetically. Fixes bug #6219985.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Wed Nov 24 2004 - kazuhiko.maekawa@sun.com
- Add English contents under l10n directory to fix 6197769(P1 STP)
* Fri Oct 29 2004 - vijaykumar.patwari@wipro.com
- Fixes nautilus crash for DnD of 'This Computer'
  icon over staroffice icon on desktop.
* Mon Aug 16 2004 - damien.carbery@sun.com
- Changed SOURCE7 mode to 0755 for Solaris integration.
* Thu Jul 15 2004 - leena.gunda@wipro.com
- Updated spec-file to change the release version to 3 for 
  Solaris. Fixes bug #5073195.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-desktop-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - damien.carbery@sun.com
- Add gnome-feedback.xml to ext-sources and package.
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul  7 2004 - takao.fujiwara@sun.com
- Updated gnome-desktop-02-menu-entries.diff
- Updated gnome-desktop-03-g11n-potfiles.diff
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri May 28 2004 - danek.duvall@sun.com
- Fixed the release version on Solaris.
* Fri May 28 2004 - laca@sun.com
- Added gnome-cleanup script (fixes 5051597)
* Mon May 24 2004 - yuriy.kuznetsov@sun.com
- Added patch gnome-desktop-03-g11n-potfiles.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-desktop-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1
* Tue May 04 2004 - glynn.foster@sun.com
- Add administration directory, so we have a nice icon
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Fri Apr 16 2004 - archana.shah@wipro.com
- Changed spec file to use 'release_version' as a variable and not a string 
  so that it displays release version number correctly.
* Thu Apr 15 2004 - glynn.foster@sun.com
- Bump to 2.6.0.1 and remove the directory entries patch
  since it's upstream and not needed anymore.
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-desktop-l10n-po-1.0.tar.bz2
* Tue Mar 23 2004 - glynn.foster@sun.com
- Bump to 2.6.0 and remove the preference icons
  since they're mostly in gnome-icon-theme now.
* Mon Mar 22 2004 - glynn.foster@sun.com
- Bump to 2.5.92, merge the jds about patches, remove
  some building patches and man page patch.
* Sun Feb 29 2004 - laca@sun.com
- Add patch 09 needed for Solaris build
* Fri Feb 20 2004 - stephen.browne@sun.com
- Added Build req for scrollkeeper 
* Tue Feb 17 2004 - laca@sun.com
- Add uninstalled.pc file needed for the Solaris builds
* Mon Feb 09 2004 - matt.keenan@sun.com
- Bump to 2.5.4, l10n tarball to 0.7
- Port patch 05, 06
- New patch 07 for omf.make, need to run gnome-doc-common to get these
  but not sure how ?
* Mon Dec 15 2003 - glynn.foster@sun.com
- Bump to 2.5.2
* Mon Oct 20 2003 - ghee.teo@sun.com
- included the patches to put in copyrights for Sun Java Desktop and Sun's 
  contributors.
* Sun Oct 19 2003 - damien.donlon@sun.com
- Updated l10n content to gnome-desktop-l10n-po-0.4.tar.bz2
* Fri Oct 17 2003 - michael.twomey@sun.com
- Updated l10n content to gnome-desktop-l10n-po-0.3.tar.bz2
* Thu Oct 16 2003 - <ghee.teo@sun.com>
- Changed the copyright and modify the contributors list
  as in bug 4938100.
* Mon Oct 13 2003 - <matt.keenan@sun.com>
- Man pages update
* Fri Oct 10 2003 - michael.twomey@sun.com
- Updated l10n content to gnome-desktop-l10n-po-0.2.tar.bz2
* Thu Oct 09 2003 - <matt.keenan@sun.com>
- Man pages
* Tue Sep 18 2003 - <markmc@sun.com> 2.3.6-13
- Updated year in copyright. Patch from Bala.
* Tue Aug 19 2003 - <glynn.foster@sun.com>
- Use the release number as a version string.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Aug 07 2003 - <markmc@sun.com> 2.3.6-4
- Add new gnome-about header images
* Thu Aug 07 2003 - <markmc@sun.com> 2.3.6-3
- Include legalaise in the gnome-about dialog.
* Thu Aug 07 2003 - <markmc@sun.com> 2.3.6-2
- Set the distributor correctly
* Thu Aug 07 2003 - <markmc@sun.com> 2.3.6-1
- Update to 2.3.6
* Thu Jul 24 2003 - <glynn.foster@sun.com>
- Give burn:/// and quick-start:/// titles and
  icons.
* Thu Jul 24 2003 - <glynn.foster@sun.com>
- Make preferences:/// use a consistant icon.
* Tue Jul 21 2003 - <glynn.foster@sun.com>
- Remove advanced directory relocation. Something must have
  changed along the way.
* Thu Jul 17 2003 - <glynn.foster@sun.com>
- Add some icons for the preferences menu
* Wed Jul 16 2003 - <Laszlo.Kovacs@sun.com>
- add gnome-desktop-03-network-directory-files.diff
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Fri Jul 03 2003 - <glynn.foster@sun.com>
- New tarball
* Wed Jul 02 2003 - <glynn.foster@sun.com>
- New tarball...whee
* Wed Jul 02 2003 - <glynn.foster@sun.com>
- Move the advanced-directory.png icon to it's 
  proper location. This probably is already fixed
  in HEAD. gnome-desktop-01-advanced-directory-relocation.diff
* Wed Jul 02 2003 - <glynn.foster@sun.com>
- Make sure that we install the .directory files
  as well
* Tue May 13 2003 - <ghee.teo@Sun.COM>
- Created new spec file for gnome-desktop
