#
# spec file for package gnome-utils
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
%define logview_version 2.24.1
Name:         gnome-utils
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Basic Utilities for the GNOME 2.0 Desktop
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#FIXME: Use logview source code from 2.24.1 tarball due to doo6328
Source3:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.24/%{name}-%{logview_version}.tar.bz2
# date:2005-05-02 type:bug bugster:6222777 owner:mattman bugzilla:310112
Patch1:       gnome-utils-01-gfloppy-permission.diff
# date:2006-04-05 type:branding owner:gman
Patch2:       gnome-utils-02-gnome-screenshot.diff
# date:2006-05-03 type:branding owner:gman
Patch3:       gnome-utils-03-search-menu-entry.diff
# date:2007-02-20 type:feature bugster:6491649,6493325,6522889 owner:lin
Patch4:       gnome-utils-04-logview224-plugin.diff
# date:2006-11-15 owner:calumb bugster:6489289 bugzilla:375684 type:bug
Patch6:       gnome-utils-06-baobab-man.diff
# date:2008-07-31 type:branding owner:lin
Patch7:       gnome-utils-07-logviewer224-manpages.diff
%if %option_with_indiana_branding
# date:2009-03-19 type:bug owner:mattman doo:161
Patch8:       gnome-utils-08-zfs.diff
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf

%define glib2_version 2.4.0
%define pango_version 1.4.0
%define gtk2_version 2.4.0
%define libgnome_version 2.6.0
%define libgnomeui_version 2.6.0
%define gail_version 1.6.3
%define gnome_panel_version 2.6.1
%define scrollkeeper_version 0.3.14

Requires:       libgnome >= %{libgnome_version}
Requires:       libgnomeui >= %{libgnomeui_version}
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  pango-devel >= %{pango_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  libgnome-devel >= %{libgnome_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  gail-devel >= %{gail_version}
BuildRequires:  gnome-panel >= %{gnome_panel_version}
BuildRequires:  scrollkeeper >= %{scrollkeeper_version}
BuildRequires:  e2fsprogs-devel

%description
This package contains some essential utilities for the GNOME2 Desktop.


%prep
%setup -q

%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch6 -p1
%if %option_with_indiana_branding
%patch8 -p1
%endif

cd ..
bzcat %SOURCE3 | tar xf -
cd %{name}-%{logview_version}
%patch4 -p1
%patch7 -p0

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
  GREP_COMMAND=/usr/bin/grep
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
  GREP_COMMAND=/usr/xpg4/bin/grep
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

test -d m4  || \
  mkdir m4

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="%_ldflags -lz -lgthread-2.0" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
	--disable-scrollkeeper \
	--disable-static	\
	--enable-shared	\
	--with-grep=$GREP_COMMAND
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

cd ../%{name}-%{logview_version}
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
	--disable-scrollkeeper \
	--disable-static	\
	--enable-shared	\
	--with-grep=$GREP_COMMAND
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages



%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
cd logview
make uninstall DESTDIR=$RPM_BUILD_ROOT
cd -
cd ../%{name}-%{logview_version}/logview
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install --mode=0644 gnome-system-log.1 $RPM_BUILD_ROOT%{_mandir}/man1
install --mode=0644 pipelog.conf.4 $RPM_BUILD_ROOT%{_mandir}/man4
install --mode=0644 grablogs.conf.4 $RPM_BUILD_ROOT%{_mandir}/man4

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gdict.schemas gfloppy.schemas gnome-screenshot.schemas gnome-search-tool.schemas logview.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libdir}/lib*.so.*
%{_libexecdir}/*
%{_datadir}/applications
%{_datadir}/gnome/help
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/gnome-screenshot/
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/gnome-utils
%{_datadir}/pixmaps
%{_datadir}/gnome-dictionary
%{_datadir}/gnome-system-log
%{_datadir}/gdict-1.0
%{_datadir}/omf
%{_mandir}/man1/*
%{_sysconfdir}/gconf/schemas
#FIXME: -devel subpkg?
%{_includedir}/*
%{_datadir}/gtk-doc
%{_libdir}/pkgconfig

%changelog
* Thu Mar 19 2009 - matt.keenan@sun.com
- Add 08-zfs patch for OpenSolaris d.o.o: 161
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
- Removed upstreamed patch 08-xinerama-screenshot.diff.
* Thu Mar 5 2009 - lin.ma@sun.com
- Fixed logview 2.24 manpage installation issue.
* Thu Feb 26 2009 - lin.ma@sun.com
- Hold logview 2.24, append the suffix '224' to logview patches.
* Tue Feb 10 2009 - matt.keenan@sun.com
- Bump to 2.25.90
* Tue Feb 03 2009 - jedy.wang@sun.com
- Remove 09-search-menu-entry-indiana.diff because OpenSolaris will use the same
  menu entry for Nevada.
- Remove option_with_sun_branding for 03-search-menu-entry.diff.
* Wed Oct 15 2008 - jedy.wang@sun.com
- Add 09-search-menu-entry-indiana.diff.
- Use option_with_sun_branding for 03-search-menu-entry.diff.
* Sun Sep 28 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - patrick.ale@gmail.com
- Correct download URL
* Fri Sep 05 2008 - matt.keenan@sun.com
- Add patch -08-xinerama-screenshot, fixes bugster:6392472 bugzilla:166485
- Re-name xx-logviewer-manpages.diff to 07-logviewer-manpages.diff all patches
  should have numbers
* Tue Aug 26 2008 - dave.lin@sun.com
- Bump to 2.23.90, update the follow patches to fix the hunk failures,
    gnome-utils-02-gnome-screenshot.diff
    gnome-utils-03-search-menu-entry.diff
    gnome-utils-04-logview-plugin.diff
    gnome-utils-06-baobab-man.diff
* Fri Aug 01 2008 - matt.keenan@sun.com
- Add attrbutes to baobab.1 community man page
* Thu Jul 31 2008 - lin.ma@sun.com
- Split manpage part from logviewer plugin into a new one dur to the new man
  page process.
* Wed Dec 05 2007 - lin.ma@sun.com
- Changed the type of logview plugin to feature.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.1.
* Thu Sep 06 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.91. Remove upstream patch, gnome-menus-05-iconv-solaris.diff.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Add patch gnome-menus-05-iconv-solaris to fix #467309. Modify
  intltool-merge.in to allow use of non-GNU iconv.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Mon Mar 16 2007 - lin.ma@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Wed Feb 21 2007 - takao.fujiwara@sun.com
- Updated gnome-utils-04-logview-plugin.diff for bug 6522889.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Thu Jan 25 2007 - damien.carbery@sun.com
- Remove -f from rm calls. Will highlight module changes. Remove deletion of
  scrollkeeper and *.a files - they aren't installed.
* Wed Jan 24 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 24 2007 - lin.ma@sun.com
- Updated gnome-utils-04-logview-plugin.diff
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90. Comment out patch4 as it needs rework, ask owner to fix.
* Tue Jan 28 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Jan 10 2007 - lin.ma@sun.com
- Updated gnome-utils-04-logview-plugin.diff
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.1. Comment out patch4 as it needs rework, ask patch owner to fix.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.0.
* Wed Nov 15 2006 - calum.benson@sun.com
- Tweak menu item name to match latest UI spec.
* Mon Nov 13 2006 - lin.ma@sun.com
- Change the name the 4th patch due to plugin integration.
  pass --disable-static and --enable-shared to configure.
* Mon Nov 06 2006 - damien.carbery@sun.com
- Bump to 2.16.2. Remove upstream patch, 05-dictionary-multihead..
* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-f' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.
* Fri Oct 11 2006 - glynn.foster@sun.com
- Add patch to fix multihead issues. Bugzilla #361856.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Fri Aug 25 2006 - damien.carbery@sun.com
- Bump to 2.15.94.
* Wed Aug 23 2006 - takao.fujiwara@sun.com
- Added '--with-grep' option. Fix bug 6453845.
* Mon Aug 21 2006 - damien.carbery@sun.com
- Bump to 2.15.93.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - brian.cameron@sun.com
- Bump to 2.15.91.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Remove upstream patches, 01-logview.diff and 04-gnome-dictionary.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed May 05 2006 - glynn.foster@sun.com
- Add patch to call things 'Find Files...'
* Fri Apr 21 2006 - brian.cameron@sun.com
- Add patch 4 to correct a core dumping problem with gnome-dictionary,
  printing a NULL string.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Sun Mar  5 2006 - damien.carbery@sun.com
- Bump to 2.13.95.
* Fri Feb 24 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Mon Jan 30 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
- Remove javahelp code. No longer used.
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Thu Aug 04 2005 - laca@sun.com
- remove upstream patch searchtool-ceasing.diff
* Mon May 23 2005 - glynn.foster@sun.com
- Move the screenshot stuff here
* Wed May 18 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help patch to add gfloppy help file
* Wed May 11 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.1
* Fri May 06 2005 - dinoop.thomas@wipro.com
- Added patch gnome-utils-10-searchtool-ceasing.diff to fix searchtool ceasing
  to search after entering a regular expression. Fixes #6262944. 
* Mon May 02 2005 - balamurali.viswanathan@wipro.com
- Added patch gnome-utils-09-gfloppy-permission.diff to fix 6222777.
* Fri Apr 22 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-utils_docs-0.9linux) from maeve.anslow@sun.com.
* Tue Apr 05 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-utils_docs-0.8linux) from maeve.anslow@sun.com.
* Thu Mar 31 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-utils_docs-0.7linux) from maeve.anslow@sun.com.
* Wed Mar 16 2005 - vinay.mandyakoppal@wipro.com
- Added patch which fixes the issue of opening a directory in nautilus
  when double clicked in case of multihead. Fixes #6234957.
* Wed Feb 28 2005 - damien.carbery@sun.com
- Update docs with tarball (_docs-0.6linux) from maeve.anslow@sun.com.
* Fri Feb 11 2005 - dinoop.thomas@wipro.com
- Added patch to correct the behaviour of searchtool with
  regular expressions involving '?'.Fixes #6227053.
* Thu Feb 10 2005 - glynn.foster@sun.com
- Add patch to fix gdict tooltip. Fixes #4918783.
* Wed Jan 26 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from maeve.anslow@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and patch
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Wed Aug 25 2004 Kazuhiko.Maekawa@sun.com
- Updated l10n help contents for Cinnabar with patch
* Thu Aug 05 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-utils-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 02 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Thu May 27 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Added gnome-utils-04-g11n-potfiles.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-utils-l10n-po-1.1.tar.bz2
* Mon May 10 2004 - leena.gunda@wipro.com
- added patch gnome-utils-03-gdict-applet-load.diff to fix 5030822.
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.2
* Wed Apr 21 2004 - laca@sun.com
- disable javahelp conversion of gfloppy docs on Solaris
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-utils-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - glynn.foster@sun.com
- Bump to 2.6.0. Refactor potfiles patch, remove ui
  and man page patches.
* Mon Mar 15 2004 - takao.fujiwara@sun.com
- Added gnome-utils-03-g11n-potfiles.diff
- Added gnome-utils-04-g11n-i18n-ui.diff to fix 4954404
* Tue Feb 24 2004 - glynn.foster@sun.com
- Dump all Matt's work on the patches since we've 
  merged most of them upstream. Some of them don't
  apply to HEAD.
* Mon Feb 23 2004 - matt.keenan@sun.com
- Bump to 2.5.2
- Remerge patch 01/02
- Port patches 03/04/05
- Update %files
* Thu Jan 08 2004 - niall.power@sun.com
- Fix incorrect pango version 1.30 -> 1.3.1
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 2.5.0
* Wed Nov 04 2003 - glynn.foster@sun.com
- Remove the dictionary application, but retain
  the applet
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported keyword from the
  desktop since we're removing Extras menu.
* Sat Oct 18 2003 - glynn.foster@sun.com
- update patches
* Sat Oct 18 2003 - laca@sun.com
- update to 2.4.0
* Fri Sep 26 2003 - laca@sun.com
- integrate Sun docs
* Tue Sep 09 2003 - glynn.foster@sun.com
- patch from wipro to stop defunct processes
* Thu Aug 07 2003 - niall.power@sun.com
- added scrollkeeper to base dependencies
* Thu Jul 17 2003 - glynn.foster@sun.com
- Don't install a non-existant logview schema.
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Mon Jul 07 2003 - glynn.foster@sun.com
- Do not install gnome-system-log either
* Tue Jul 01 2003 - glynn.foster@sun.com
- Correct gfloppy icon
* Tue Jul 01 2003 - glynn.foster@sun.com
- Disable gcalc, gcharmap & gdialog from build.
* Tue Jul 01 2003 - glynn.foster@sun.com
- Update version on tarball
* Tue May 13 2003 - ghee.teo@Sun.COM
- Initial Sun release
