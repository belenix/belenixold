#
# spec file for package gnome-icon-theme
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
Name:         		gnome-icon-theme
License:      		GPL
Group:        		System/GUI/GNOME
BuildArchitectures:	noarch
Version:      		2.26.0
Release:      		1
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		GNOME Icon Themes
Source:       		http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %option_with_sun_branding
Source3:		branded-throbber.tar.gz
Source4:		sun_java.png
%endif
%if %build_l10n
Source5:                 l10n-configure.sh
%endif
%if %option_with_sun_branding
#owner:gman date:2005-04-08 type:branding
Patch1:			gnome-icon-theme-01-sun-java-icon.diff
%endif
# This patch removes a path from icon-name-mapping because the binary is being
# run before the module is installed.
#owner:dcarbery date:2005-10-11 type:branding
Patch2:			gnome-icon-theme-02-pkgconfig-dir.diff
URL:          		http://www.gnome.org/
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Docdir:	      		%{_defaultdocdir}/doc
Autoreqprov:  		on

%define hicolor_icon_theme_version 0.4

Requires:		hicolor-icon-theme >= %{hicolor_icon_theme_version}
BuildRequires:		intltool
BuildRequires:		glib2
BuildRequires:		hicolor-icon-theme >= %{hicolor_icon_theme_version}
BuildRequires:		automake >= 1.9

%description
Collection of Icon Themes for the GNOME Desktop

%prep
%setup -q
%if %option_with_sun_branding
gzip -dc %SOURCE3 | tar xvf -
cp %SOURCE4 48x48/apps/
%patch1 -p1
%endif
%patch2 -p1

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

intltoolize --copy --force

%if %build_l10n
bash -x %SOURCE5 --enable-copyright
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
%ifos linux
	    --sysconfdir=%{_sysconfdir}
%else
	    --sysconfdir=%{_sysconfdir} \
	    --disable-hicolor-check
%endif
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_datadir}/icons/gnome
%{_libdir}/pkgconfig/gnome-icon-theme.pc

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Mon Jun 16 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Dec 19 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.21.0.
* Fri Sep 28 2007 - laca@sun.com
- do not install sun java icon when sun branding is not requested
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0. Remove upstream patch, 03-missing-index.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Fri Aug 03 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Thu Dec 21 2006 - damien.carbery@sun.com
- Bump to 2.17.4.1.
* Wed Dec 20 2006 - damien.carbery@sun.com
- Bump to 2.17.4.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.3. Remove obsolete patch, 03-relative-symlinks.
* Fri May 12 2006 - laca@sun.com
- add patch relative-symlinks.diff for making some absolute symlinks relative
* Wed Mar 15 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
- Remove obsolete patch, 03-no-script-path.
* Thu Feb  9 2006 - damien.carbery@sun.com
- Add patch, 03-no-script-path, so not set path to icon-name-mapping script.
* Wed Feb  8 2006 - damien.carbery@sun.com
- Bump to 2.13.7.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Add needed intltoolize call.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
* Wed Dec 21 2005 - glynn.foster@sun.com
- Bump to 2.13.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
- Add patch, gnome-icon-theme-02-pkgconfig-dir, to undo change in 2.12.1 where
  pc file installed into /usr/share instead of /usr/lib. Maintainer queried.
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Thu Aug 25 2005 - damien.carbery@sun.com
- Add automake build dependency, as it will fail for earlier automake.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Fri Apr 08 2005 - glynn.foster@sun.com
- Remove panel-icons.tar.gz from the build, since we should
  be installing these elsewhere, rather than duplicating 
  stuff. Add back sun_java.png since it's not installed
  elsewhere.
* Fri Apr 08 2005 - glynn.foster@sun.com
- Remove the staroffice icons, since now the staroffice team
  are responsible for delivering them.
* Mon Feb 21 2005 - calum.benson@sun.com
- Added Source5 (branded-throbber.tar.gz) to fix 6203001.
* Thu Feb 10 2005 - muktha.narayan@wipro.com
- Updated gnome-icon-theme-05-add-panel-icons.diff and
  ext-sources/panelicons.tar.gz to include gnome-main-menu.png.
* Fri Jan 28 2005 - muktha.narayan@wipro.com
- Added gnome-icon-theme-05-add-panel-icons.diff and
  ext-sources/panelicons.tar.gz to install panel icons 
  in order to fix #5088581.
* Wed Sep 29 2004 - takao.fujiwara@sun.com
- Update gnome-icon-theme-02-g11n-potfiles.diff
- Add gnome-icon-theme-04-g11n-icons.diff to fix 5061956
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-icon-theme-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Jun 01 2004 - danek.duvall@sun.com
- Fixed broken symlink to shellscript mimetype icon
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-icon-theme-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-icon-theme-l10n-po-1.0.tar.bz2
* Thu Mar 25 2004 - niall.power@sun.com
- Bumt to 1.2.0, add proper hicolor-icon-theme dependencies
* Mon Mar 22 2004 - glynn.foster@sun.com
- Bump to 1.1.91, remove weird linking patch, 
  and timezone icon patch
* Tue Mar 16 2004 - takao.fujiwara@sun.com
- Added gnome-icon-theme-04-g11n-icon.diff to fix 4957964
* Mon Feb 16 2004 - <niall.power@sun.com>
- disable-hicolor-check on Solaris. It will fail.
- Add ACLOCAL_FLAGS to aclocal invocation
* Thu Feb 12 2004 - <matt.keenan@sun.com>
- Amend files to install all hicolor icons !!
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Patch for install data hook to use DESTDIR
* Tue Feb 10 2004 - <matt.keenan@sun.com>
- Bump to 1.1.6, l10n to 0.7
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add dependency on intltool
* Fri Jan 16 2004 - matt.keenan@sun.com
- Remove reference to SOURCE4 :)
* Fri Jan 16 2004 - glynn.foster@sun.com
- Remove the jar icon since it's gone into HEAD
* Tue Jan 06 2004 - niall.power@sun.com
- Update to 1.1.4. Fixes build breakage.
* Mon Dec 15 2003 - glynn.foster@sun.com
- Update to 1.1.3
* Fri Oct 10 2003 - laca@sun.com
- Update to 1.0.9
* Thu Jul 24 2003 - glynn.foster@sun.com
- Add jar icon
* Wed Jul 23 2003 - glynn.foster@sun.com
- New my computer icon
* Wed Jul 23 2003 - glynn.foster@sun.com
- New timezone icon
* Tue Jul 08 2003 - glynn.foster@sun.com
- New tarball, bump version, reset release
* Wed Jul 01 2003 - glynn.foster@sun.com
- New tarball, bump version, reset release
* Tue Jun 30 2003 - Stephen.Browne@sun.com
- Add pngs for StarOffice launchers and mimetypes
* Tue May 13 2003 - Stephen.Browne@sun.com
- initial release
