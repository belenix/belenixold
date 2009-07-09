#
# spec file for package eog
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
%include l10n.inc
Name:         eog
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Eye Of GNOME Image Viewer
Source:       http://ftp.gnome.org/pub/GNOME/sources/eog/2.26/eog-%{version}.tar.bz2
%if %build_l10n
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
%endif
# date:2006-06-06 owner:gman type:branding
Patch1:       eog-01-menu-entry.diff
# date:2009-02-18 owner:davelam type:branding
Patch2:       eog-02-add-libgthread.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on

%define libgnomeui_version 2.5.90
%define libgnomeprintui_version 2.6.0
%define scrollkeeper_version 0.3.12
%define eel_version 2.5.90

Requires:	libgnomeui >= %{libgnomeui_version}
Requires:	libgnomeprintui >= %{libgnomeprintui_version}
Requires:       eel > %{eel_version}
Prereq:         GConf
BuildRequires:	libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:	libgnomeprintui-devel >= %{libgnomeprintui_version}
BuildRequires:	eel-devel >= %{eel_version}
BuildRequires:	scrollkeeper >= %{scrollkeeper_version}
BuildRequires:	intltool

%description
The "Eye of GNOME" is a very fast picture viewer, which can either be used as a 
plugin for Nautilus, or as a standalone application. This version of EOG is 
compiled for the GNOME 2.0 Desktop platform.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1

for po in po/*.po; do
  dos2unix -ascii $po $po
done


%build
%ifos linux
if [ -3 /usr/bin/getconf ]; then
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
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
gtkdocize
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --libexecdir=%{_libexecdir} \
	    --disable-scrollkeeper	\
            --without-lcms
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL  
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
chmod 644 $RPM_BUILD_ROOT%{_datadir}/gnome/help/eog/*/*.xml


%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="eog.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/eog.schemas
%{_datadir}/applications/eog.desktop
%{_datadir}/eog/*
%{_datadir}/gnome/help/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/eog/*
%{_datadir}/pixmaps/*
%{_datadir}/man/man1/*
%{_prefix}/var/scrollkeeper

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
- Add patch 03-gtkdoc-rebase.diff to fix GTKDOC_REBASE issue.
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Web Mar 04 2009 - chris.wang@sun.com
- Transfer the ownership to bewitche
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
- Add patch 02-add-libgthread.diff to add libgthread-2.0 in LDFLAGS.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92 (d'oh).
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.1. Remove upstream patch, 02-libz.
* Wed Jun 11 2008 - damien.carbery@sun.com
- Add patch 02-libz to link with libz. Fixes bugzilla 537758.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0. Remove upstream patch 02-threads.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92. Remove upstream patch 03-zh_TW-help.
* Wed Feb 20 2007 - damien.carbery@sun.com
- Add patch 03-zh_TW to fix build issue in zh_TW's eog.xml. This patch is a
  hack - it copies zh_CN eog.xml. Bugzilla 517702.
* Wed Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Thu Nov 22 2007 - matt.keenan@sun.com
- Add Patch 02-threads.diff resolves bugs 6536622/498989
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Sep 04 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3. Remove upstream patch, 02-sys-time.
* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 2.19.1. Add patch, 02-sys-time, to fix build issue where sys/time.h
  not included unless included at top of source file.
* Thu Apr 29 2007 - rick.ju@sun.com
- remove the upstreamed patch eog-01-full-screen-show.diff
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Wed Apr 04 2007 - darren.kenny@sun.com
- Wrapped Source1 in a %if %build_l10n
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2005 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Feb 06 2007 - matt.keenan@sun.com
- Remove patch eog-02-jpeg.diff, linker patch no longer needed
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.4.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Fri Oct 20 2006 - damien.carbery@sun.com
- Bump to 2.16.1.1.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Thu Jul 27 2006 - damien.carbery@sun.com
- Add dos2unix call to fix po files.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - laca@sun.com
- add --without-lcms to avoid accidentally picking up liblcms (part of
  spec-files-extra), fixes 6425540
* Web Jul 19 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Sun Mar  5 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Thu Jan 19 2006 - damien.carbery@sun.com
- Running glib-gettextize is a better fix than patching the Makefile to
  not go into the po directory.  This fixes infinite loop also.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Add intltoolize call.
* Tue Jan 17 2006 - glynn.foster@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.3
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Mon Oct 03 2005 - damien.carbery@sun.com
- Add patch to link with X11 to build on Solaris. Bugzilla 317828.
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.90.
* Thu Aug 04 2005 - laca@sun.com
- removed patch image-save-as.diff, fix now in gnome-vfs
* Thu Jun 23 2005 - arvind.samptur@wipro.com
- Fix files getting deleted when doing a save as. Fixes #6288517
* Thu May 19 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Fri May 05 2005 - kieran.colfer@sun.com
- updating l10n po tarball to 1.15. Fixing CR 6265841
* Mon Mar 21 2005 - srirama.sharma@wipro.com
- Added eog-06-full-screen-show.diff to see that gtk_grab_add is
  done only when no other widget holds the grab.
  Fixes bug #6238888.
* Mon Mar 07 2005 - damien.carbery@sun.com
* 6233036: Add Source6 to specify Linux version of docs tarball.
* Thu Mar 03 2005 - srirama.sharma@wipro.com
- Added eog-05-multihead-functionality.diff to 
  make eog functional on a multihead system.
  Fixes bug #4893502.
* Tue Feb 22 2005 - damien.carbery@sun.com
* Correct name of docs tarball.
* Mon Feb 21 2005 - damien.carbery@sun.com
- Correct commit of Jan 25 to update docs tarball to 0.4.
* Tue Feb 08 2005 - srirama.sharma@wipro.com
- Updated eog-02-print-preview.diff to see that the print-preview window 
  does not diminish in size when invoked multiple times. Fixes bug #6221186.
* Tue Jan 25 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from maeve.anslow@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Wed Dec 22 2004 - takao.fujiwara@sun.com
- Added eog-04-g11n-i18n-ui.diff to localize eog printer dialog.
  Fix bug 6174164
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents with patch
* Mon Aug 16 2004 - shirley.woo@sun.com
- Updated /usr/share/gnome/help/eog/*/*.xml to 0644 for Solaris integration 
* Thu Aug 05 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to eog-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Jun 10 2004 - vijaykumar.patwari@wipro.com
- Added patch for print preview.
* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Thu May 13 2004 - narayana.pattipati@wipro.com
- Added patch eog-01-image-collection-viewer.diff to provide viewer_label
  for Image Collection Viewer. Fixes bugtraq bug#5043908. Also the changes 
  have been committed to community CVS HEAD on May 12 2004 
  (bugzilla bug#142347)
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to eog-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Fri Apr 09 2004 - brian.cameron@sun.com
- Change the way the build directory is cleaned so that eog and
  gthumb can be built into the same Solaris package.
* Tue Apr 06 2004 - glynn.foster@sun.com
- Bump to 2.6.0
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to eog-l10n-po-1.0.tar.bz2
* Mon Mar 01 2004 - <laca@sun.com>
- add $ACLOCAL_FLAGS to aclocal args
* Fri Feb 06 2004 - <matt.keenan@sun.com>
- Bump tarball to 2.5.4 because of intltool (OrigTree) Failures
- Remove patch1 and patch2 no longer needed
- bump l10n release
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- add patch 02 for intltool-merge and dep. on intltool
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.1
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove potfiles patch [not needed] and Sun Support 
  keyword patch, since we're no longer using the Extras
  menu.
- Update to 2.4.0
* Fri Oct 10 2003 - <laca@sun.com>
- Update to 2.4.0
* Fri Sep 26 2003 - <laca@sun.com>
- Integrate Sun docs
* Fri Aug 07 2003 - <glynn.foster@sun.com>
- Add mnemonics to some menu items.
* Fri Aug 01 2003 - <glynn.foster@sun.com>
- Add recent files support
* Wed Jul 30 2003 - <glynn.foster@sun.com>
- New tarball
* Mon Jul 28 2003 - <glynn.foster@sun.com>
- Change menu entry.
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Wed Jul 02 2003 - glynn.foster@sun.com
- Fix up the install of the glade file to stop things
  crashing
* Wed May 14 2003 - Stephen.Browne@sun.com
- initial release
