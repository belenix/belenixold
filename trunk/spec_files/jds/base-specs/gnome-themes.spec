#
# spec file for package gnome-themes
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: calumb
#
Name:			gnome-themes
License:		GPL
Group:			System/GUI/GNOME
# icon-naming-utils should be bumped at the same time - it's a dependency.
Version:		2.26.0
Release:		3
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		GNOME themes
Source:                 http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:                staroffice8-accessibility-icons.tar.gz
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:calumb date:2005-05-27 bugster:6298139 type:bug
Patch1:			gnome-themes-01-add-so8-a11y-icons.diff
URL:			http://www.gnome.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildArchitectures:     noarch
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

%define gtk2_engines_version 2.2.0

BuildRequires: gtk2-engines >= %{gtk2_engines_version}
BuildRequires: libgnomeui-devel
BuildRequires: intltool
Requires:      gtk2-engines >= %{gtk2_engines_version}

%description
Additional GNOME themes.

%prep
%setup -q
%patch1 -p1
gzip -dc %SOURCE1 | tar xvf -


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

glib-gettextize -f
libtoolize --force
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

export CFLAGS="$RPM_OPT_FLAGS"
./configure \
                --prefix=%{_prefix} \
                --libdir=%{_prefix}/%_lib \
                --sysconfdir=%{_sysconfdir} \
		--enable-all-themes
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr(-, root, root)
%{_datadir}/icons/*
%{_datadir}/themes/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - calum.benson\@sun.com
- Bump to 2.25.90, gnome-themes-01-add-so8-a11y-icons.diff also
  modified accordingly.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Wed May 09 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - calum.benson@sun.com
- Updated gnome-themes-01-add-so8-a11y-icons.diff for 2.18.0.
  Also removed accessibility-icons.tar.gz, which is now upstream.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2. Remove upstream patches, 01-accessibility-icons and 
  03-icon-name-mapping. Rename remainder.
* Wed Nov 15 2006 - calum.benson@sun.com
- Add --enable-all-themes flag, as per UI spec.
* Mon Nov 14 2006 - calum.benson@sun.com
- Add patch owner comments to spec file, and change gnome-main-menu.png
  to start-here.png in patch gnome-themes-01. Fixes bugzilla 357931
  and bugster 6484251.
* Sat Oct 07 2006 - damien.carbery@sun.com
- Bump to 2.16.1.1.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 2.15.91.1.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.4.
- Add patch, 01-icon-name-mapping, to remove path to icon-name-mapping.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.2.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.13.2
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri May 27 2005 - calum.benson@sun.com
- Add high contrast StarOffice8 icons, which were previously
  installed by staroffice-menuintegration. (Any upstream version
  of this patch should probably be tailored to OpenOffice 2.0)
  Fixes 6273621.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Wed Apr 20 2005 - calum.benson@sun.com
- Add high and low contrast launch menu backgrounds and spinners,
  and fix a minor typo in patch 06 that was generating a warning.
  Fixes 5072859, 6255199, and at the very least downgrades
  5072848.
* Fri Apr 08 2005 - glynn.foster@sun.com
- Remove icons being installed into some of the icon
  themes, when they aren't different from the original
  hicolor theme. The correct fix was to install them into 
  hicolor theme in the panel source.
* Thu Apr 07 2005 - muktha.narayan@wipro.com
- Added gnome-themes-06-add-printer-icons.diff and
  updated ext-sources/gnome-themes-icons.tar.gz to install
  printer icons in order to fix #5035243.
* Wed Feb 23 2005 - calum.benson@sun.com
- Added gnome-themes-05-add-missing-hc-launch-icons.diff 
  to add some missing High Contrast and High Contrast Inverse
  icons to the launch menu; fixes CR 6219531.
* Thu Feb 10 2005 - muktha.narayan@wipro.com
- Updated gnome-themes-04-add-panel-icons.diff and
  ext-sources/gnome-themes-icons.tar.gz to include
  gnome-main-menu.png.
* Fri Jan 28 2005 - muktha.narayan@wipro.com
- Added gnome-themes-04-add-panel-icons.diff and
  ext-sources/gnome-themes-icons.tar.gz to install panel
  icons in order to fix #5088581.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-themes-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 - hidetoshi.tajima@sun.com
- run glib-gettextize and intltoolize
* Tue Jun 8 2004 - padraig.obriain@sun.com
- Bump to 2.6.2
* Tue Jun 1 2004 - glynn.foster@sun.com
- Bump to 2.6.1
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-themes-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-themes-l10n-po-1.0.tar.bz2
* Fri Mar 12 2004 - <niall.power@sun.com>
- remove "rm -rf" from install stage.
* Fri Feb 06 2004 - <matt.keenan@sun.com>
- Bump to 2.5.4, remove gnome-theme-02-intltool-merge.diff
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- add patch 02 for intltool-merge and dep. on intltool
* Mon Dec 15 2003 - glynn.foster@sun.com
- Bump to 2.5.1
* Tue Oct 20 2003 - glynn.foster@sun.com
- New tarball. Whee.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Thu Jul 03 2003 - glynn.foster@sun.com
- Actually install the engines 
* Tue Jul 01 2003 - glynn.foster@sun.com
- New tarball, bump version, reset release
* Wed May 14 2003 - Stephen.Browne@sun.com
- initial release

