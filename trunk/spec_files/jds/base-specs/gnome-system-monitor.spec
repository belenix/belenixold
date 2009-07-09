#
# spec file for package gnome-system-monitor 
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
%include l10n.inc
Name:         gnome-system-monitor 
License:      GPL v2
Group:        System/GUI/GNOME 
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Simple process monitor 
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# The G_GNUC_INTERNAL portions of the 01-solaris patch are in bugzilla 373041.
# date:2006-11-15 owner:niall type:feature
#This patch make libgtop run at Solaris
Patch1:       gnome-system-monitor-01-solaris.diff
# date:2006-11-15 owner:calumb type:bug bugster:6489289 bugzilla:375669
Patch2:       gnome-system-monitor-02-launch-menu-item.diff
%if %option_with_indiana_branding
# date:2008-11-27 owner:niall type:bug bugster:6777351
Patch3:       gnome-system-monitor-03-zfs.diff
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on
Prereq:       GConf

%define libgnomeui_version 2.6.0
%define libwnck_version 2.6.0
%define libgtop_version 2.9.5
%define scrollkeeper_version 0.3.14

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: libgtop-devel >= %{libgtop_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      libwnck >= %{libwnck_version}
Requires:      libgtop >= %{libgtop_version}


%description
Gnome-system-monitor is a simple process and system monitor for Gnome.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%if %option_with_indiana_branding
%patch3 -p1
%endif

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
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=%{_prefix}	\
	    --disable-scrollkeeper \
            --sysconfdir=%{_sysconfdir} \
            --enable-more-warnings=no

# Create a missing file. Fixed in cvs.
touch pixmaps/side.png
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/


# Delete scrollkeeper files - conflict with eog files!
rm -rf $RPM_BUILD_ROOT%{_prefix}/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-system-monitor.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog HACKING NEWS README TODO
%{_bindir}/gnome-system-monitor
%{_datadir}/applications/gnome-system-monitor.desktop
%{_datadir}/locale/*/*/gnome-system-monitor.mo
%{_datadir}/gnome/help/gnome-system-monitor
%{_datadir}/omf/gnome-system-monitor/*.omf
%{_sysconfdir}/gconf/schemas/*.schemas
%{_mandir}/man1/*

%changelog
* Mon Mar 23 2009 - niall.power@sun.com
  Take ownership of spec file + patches
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Wed Mar 04 2009 - dave.lin@sun.com
- Bump to 2.25.91.
* Fri Nov 27 2008 - hua.zhang@sun.com
- Add patch to fix 6777351
* Fri Feb 22 2008 - damien.carbery@sun.com
- Add --disable-scrollkeeper to configure because scrollkeeper-update breaks
  build.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Wed Apr 11 2007 - damien.carbery@sun.com
- Bump to 2.18.1.1
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.95.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.6.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Thu Jan 04 2007 - damien.carbery@sun.com
- Add patch, 04-src-link, to fix #392776, unresolved symbols during link.
* Wed Dec 20 2006 - damien.carbery@sun.com
- Bump to 2.17.4.2.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4.1.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.4. Remove upstream patch 03-wifexited-wait.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Add patch, 03-wifexited-wait to include sys/wait.h in src/sysinfo.cpp.
  Fixes 383291.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.2.1.
* Thu Nov 16 2006 - hua.zhang@sun.com
- add patch comments.
* Wed Nov 15 2006 - calum.benson@sun.com
- Modify launch menu entry to match latest UI spec.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Wed Sep 06 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed July 19 2006 - hua.zhang@sun.com
- Add one patch so that Monitor can run at Solaris,
  also fix some existed bugs.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
  Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
  Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Thu May 19 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Wed Mar 09 2005 - kazuhiko.maekawa@sun.com
- Updated gnome-system-monitor-01-l10n-online-help.diff for l10n help
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Updated l10n help tarball name for Cinnabar
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs 0.3 tarball from breda.mccoglan@sun.com
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-system-monitor-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - damien.carbery@sun.com
- Integrated docs 0.2 tarball from breda.mccoglan@sun.com
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-system-monitor-l10n-po-1.1.tar.bz2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 08 2004 - niall.power@sun.com
- bump to 2.6.0
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-system-monitor-l10n-po-1.0.tar.bz2
* Mon Feb 16 2004 - matt.keenan@Sun.COM
- Bump to 2.5.3, port docs/l10n
* Tue Dec 16 2003 - glynn.foster@Sun.COM
- Bump to 2.5.2
* Fri Oct 31 2003 - glynn.foster@Sun.COM
- Remove the Sun Supported keyword, reorder patches.
* Tue Oct 14 2003 - niall.power@Sun.COM
- updated to version 2.4.0, reset release
* Fri Aug 08 2003 - niall.power@Sun.COM
- Remove mnemonics from notebook tab labels (#4903256)
* Tue Aug 05 2003 - glynn.foster@Sun.COM
- Update tarball, bump version, reset release.
* Fri Aug 01 2003 - glynn.foster@Sun.COM
- Add menu category to the menu entry.
* Wed May 14 2003 - Laszlo.Kovacs@Sun.COM
- Initial release
