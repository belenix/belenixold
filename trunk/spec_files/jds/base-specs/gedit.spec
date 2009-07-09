#
# spec file for package gedit
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: rickju
#
%include l10n.inc
Name:		gedit
License:	GPL
Group:		System/GUI/GNOME
Version:	2.26.0
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Text Editor for GNOME
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:	%{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# date:2006-06-06 owner:gman type:branding
Patch1:         gedit-01-menu-entry.diff
# date:2008-12-26 owner:davelam type:bug bugzilla:N/A
Patch2:         gedit-02-libsocket.diff
# date:2009-02-18 owner:davelam type:bug bugzilla:N/A
Patch3:         gedit-03-py_ssize_t.diff
URL:            http://www.gnome.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_docdir}/doc
Autoreqprov:    off
Prereq:         GConf

%define major_minor 2.12

%define gtksourceview_version 1.0.0
%define libglade_version 2.3.6
%define libgnomeprintui_version 2.6.0
%define libgnomeui_version 2.6.0
%define scrollkeeper_version 0.3.14
%define intltool_version 0.31.3
%define pygtk2_version 2.7.0

BuildRequires: gtksourceview-devel >= %{gtksourceview_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libgnomeprintui-devel >= %{libgnomeprintui_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: intltool >= %intltool_version
BuildRequires: pygtk2-devel >= %{pygtk2_version}
Requires: gtksourceview >= %{gtksourceview_version}
Requires: libglade >= %{libglade_version}
Requires: libgnomeprintui >= %{libgnomeprintui_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: pygtk2 >= %{pygtk2_version}

%description
GEdit is a graphical text editor for GNOME

%package devel
Summary:      Developer files for gedit
Group:        Development/Libraries/GNOME
Requires:     %name = %version-%release

%description devel
GEdit is a graphical text editor for GNOME.  This package contains files
required for building or developing gedit plugins.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

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

rm -f m4/lt*.m4 m4/libtool.m4
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS -I m4
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"				\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --libexecdir=%{_libexecdir}		\
	    --localstatedir=%{_localstatedir}   \
	    --mandir=%{_mandir}			\
	    --disable-scrollkeeper
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1    
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL   
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper


#remove unpackaged files
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.pyo
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*/*.pyo

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gedit.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/*/*.py
%{_libdir}/gedit-2/plugins/*/*.pyc
%{_libdir}/gedit-2/plugins/*.py
%{_libdir}/gedit-2/plugins/*.pyc
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/gedit-2/plugins/*/*.glade
%{_sysconfdir}/gconf/schemas/gedit.schemas
%{_datadir}/applications/*.desktop
%{_datadir}/gedit-2
%{_datadir}/gnome/help/gedit
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/gedit
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.8
* Mon Mar 02 2009 - ke.wang@sun.com
- Use find command to remove *.la files
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.7
- Add patch 03-py_ssize_t.diff to fix undef symbol Py_ssize_t issue.
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.6
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Sep 26 2008 - rick.ju@sun.com
- Bump to 2.24.0
* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 2.23.93.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump tp 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.90
- Removed the upstreamed patch gedit-02-gthread-dependency.diff
* Thu Aug 14 2008 - damien.carbery@sun.com
- Bump to 2.23.3. Remove upstream patches 02-void-return and 03-func-mismatch.
  Add patch, 02-gthread-dependency, to add gthread-2.0 dependency to fix build
  failure.

* Thu Jun 05 2008 - damien.carbery@sun.com
- Add patch 03-func-mismatch to fix bugzilla 536809. Variable type in function
  declaration and definition did not match and broke build.
- Add patch 02-void-return to fix bugzilla 536789. A void function is returning
  a value. Breaks build.

* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.

* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.3.

* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Fri Feb 29 2008 - damien.carbery@sun.com
- Add --libexecdir to configure call.

* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.2. Remove upstream patch, 02-fixcrash.

* Tue Feb 12 2008 - brian.cameron@sunc.om
- Add patch to fix crash in P2 bug 6661324.

* Fri Jan 25 2008 - damien.carbery@sun.com
- Bump to 2.21.1.

* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.4.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.3.

* Thu Sep 27 2007 - damien.carbery@sun.com
- Bump to 2.20.1.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Tue Sep 11 2007 - damien.carbery@sun.com
- Bump to 2.19.92.

* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91.

* Thu Aug 16 2007 - damien.carbery@sun.com
- Bump to 2.19.90.

* Wed Aug 01 2007 - damien.carbery@sun.com
- Bump to 2.19.3.

* Wed Jul 04 2007 - damien.carbery@sun.com
- Bump to 2.19.2.

* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.19.1.

* Sun Jun 17 2007 - damien.carbery@sun.com
- Remove patch 01-no-zh_TW-help as the bug, #397299, has been resolved.

* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.6. Remove upstream patch, 03-grep.

* Mon Feb 26 2007 - jeff.cai@sun.com
- Enable spell checker.
- Add patch -03-grep.diff to remove '-q' option of grep.

* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 2.17.5.

* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.4. Remove upstream patch, 03-void-return.

* Tue Jan 16 2007 - damien.carbery@sun.com
- Remove unnecessary patch, 01-gtksourceview-binding. Renumber rest.

* Wed Jan 10 2007 - damien.carbery@sun.com
- Bump to 2.17.3. Add patch, 04-void-return, to fix #395055.

* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.2.

* Thu Dec 07 2006 - damien.carbery@sun.com
- Add '--disable-spell' to configure so that the enchant module is not needed.

* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.1. Remove upstream patch, 01-spellcheck-fallback-to-enus.
  Renumber remainder.

* Tue Oct 31 2006 - damien.carbery@sun.com
- Bump to 2.16.2.

* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.

* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.

* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.8.

* Tue Aug 15 2006 - damien.carbery@sun.com
- Bump to 2.15.7.

* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.6.

* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.5.

* Tue Jul 25 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.

* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.3.

* Fri Jun 01 2006 - glynn.foster@sun.com
- Add menu entry patch.

* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.2.

* Thu Mar 16 2006 - damien.carbery@sun.com
- Bump to 2.14.1.

* Tue Mar 14 2006 - damien.carbery@sun.com
- Add patch, 02-gtksourceview-binding, to skip non-existant python binding file.
  The file is not in pygtk2 like the other .defs files.
- Add patch, 03-no-zh_TW-help, to skip zh_TW help as it crashes xml2po.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Mon Mar  6 2006 - damien.carbery@sun.com
- Bump to 2.13.93.

* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 2.13.92.

* Wed Feb 22 2006 - damien.carbery@sun.com
- Remove patch, 02-no-zh-help, as issue resolved in latest tarball.

* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.

* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.

* Fri Jan 27 2006 - damien.carbery@sun.com
- Add patch, 02-no-zh-help, to workaround #328888.

* Sat Jan 21 2006 - damien.carbery@sun.com
- Bump to 2.13.4

* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.3

* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.2

* Sat Jan 07 2006 - damien.carbery@sun.com
- Point aclocal to module's m4 files.

* Tue Jan 03 2006 - damien.carbery@sun.com
- Remove obsolete patches, 

* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.0

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1

* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.

* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 2.10.3

* Thu May 19 2005 - glynn.foster@sun.com
- Really port to 2.10.2

* Fri May 05 2005 - kieran.colfer@sun.com
- updating l10n po tarball for CR 6265858

* Thu Mar 31 2005 - vinay.mandyakoppal@wipro.com
- Added intltoolize to get the latest intltool-update/merge to fix 
  intall errors. Fixes bug #6243610.

* Tue Jan 25 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from maeve.anslow@sun.com.

* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
                                                                                
* Wed Dec 22 2004 - srirama.sharma@wipro.com
- Added patch gedit-11-a11y_page_setup.diff so that gnopernicus
  does not read the labels of File->Pagesetup->font tab multiple times.
  Fixes Bug #6199112.

* Wed Dec 22 2004 - srirama.sharma@wipro.com
- Added patch gedit-10-a11y_open_location.diff so that gnopernicus 
  reads the label of File->Open Location dialog. Fixes Bug #6199089. 

* Wed Nov 17 2004 - matt.keenan@sun.com
- #6195855, install correct manpage

* Fri Nov 12 2004 - hidetoshi.tajima@sun.com
- Added patch : gedit-09-spellcheck-fallback-to-enus.diff, #6194573

* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Added patch : gedit-08-g11n-i18n-ms-euc.diff for bug 6194514

* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR

* Fri Sep 24 2004 vinay.mandyakoppal@wipro.com
- Added patch gedit-06-help.diff to fix help issues.
  Fixes bugs #5094026,5094027,5094029,5101694.
 
* Wed Aug 25 2004 Kazuhiko.Maekawa@sun.com
- Updated help tar name for Cinnabar

* Fri Aug 20 2004 damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.

* Fri Aug 20 2004 johan.steyn@sun.com
- Removed  gedit-06-spellchecker-plugin.diff as it won't work on Solaris,
  and also because it has to do with a problem in aspell being built using
  a version of libtool older than 1.5.

* Fri Aug 20 2004 johan.steyn@sun.com
- Added gedit-06-spellchecker-plugin.diff to check the apsell library correctly
  so that spellchecker plugin is built. Fixed bug 5084894.

* Thu Aug 12 2004 takao.fujiwara@sun.com
- Added gedit-05-g11n-i18n-ui.diff to localize taglist. Fixed 5068944.

* Thu Aug 05 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Mon Jul 26 2004 - johan.steyn@sun.com
- added gedit-04-command-pipe.diff to fix bugtraq #5046785

* Fri Jul 23 2004 - hidetoshi.tajima@sun.com
- added gedit-03-g11n-utf8-autodect.diff to fix bugtraq
  5063167

* Tue Jul 20 2004 - glynn.foster@sun.com
- Bump to 2.6.2

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gedit-l10n-po-1.2.tar.bz2

* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Thu Jun 24 2004 - takao.fujiwara@sun.com
- Add gedit-03-g11n-i18n-ui.diff to localize open dialog. bugzilla #144525

* Wed Jun 02 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gedit-l10n-po-1.1.tar.bz2

* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris

* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gedit-l10n-po-1.0.tar.bz2

* Tue Mar 17 2004 - glynn.foster@sun.com
- Add bak schema patch, since we still need it.

* Tue Mar 17 2004 - glynn.foster@sun.com
- Bump to 2.5.92. Remove man page, schema includes, pixmap sources
  build fix and desktop g11n patch.

* Mon Mar 15 2004 - takao.fujiwara@sun.com
- Replaced gedit-04-default-schemas.diff with gedit-04-g11n-schemas.diff 
  to fix 4924569 and 4996253
- Added gedit-06-g11n-desktop.diff to fix 4969602
- Added gedit-07-g11n-potfiles.diff

* Wed Feb 18 2004 - <matt.keenan@sun.com>
- Bump to 2.5.3, add l10n online line
- Ported default schemas patch 04

* Fri Jan 09 2004 - <matt.keenan@sun.com>
- Patch to remove extra includes

* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.0

* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the Sun Supported keyword patch since we're removing
  the Extras menu.

* Tue Oct 21 2003 - <michael.twomey@sun.com>
- Updated to GNOME 2.4.0 version, updated POTFILES.in patch,
  and add patch to use libgnomeprintui 2.3.0 instead of 2.3.1.

* Fri Sep 26 2003 - <laca@sun.com>
- integrate Sun docs

* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files

* Wed May 14 2003 - Matt.Keenan@sun.com
- Initial Sun Release
