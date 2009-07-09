#
# spec file for package gtkam
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=8874&atid=108874&aid=
#
%include l10n.inc
%define gexif_version 0.5

Name:         gtkam
License:      GPL
Group:        Hardware/Other
Version:      0.1.16.1
Release:      3
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      A GTK Digital Camera Viewing Tool
Source:       http://easynews.dl.sourceforge.net/sourceforge/gphoto/%{name}-%{version}.tar.bz2
Source1:      http://umn.dl.sourceforge.net/libexif/gexif-%{gexif_version}.tar.bz2
Source2:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source3:      gtkam-icons.tar.bz2
%if %build_l10n
Source4:                 l10n-configure.sh
%endif
# date:2003-08-15 type:branding owner:mattman bugid:1619752
Patch1:	      gtkam-01-menu-entry.diff
# date:2004-02-04 type:bug owner:fujiwara bugid:1616317,1616320,1616397,1990311 bugster:6329710
Patch2:       gtkam-02-fixgexif.diff
# date:2008-07-10 owner:dcarbery type:bug
Patch3:       gtkam-03-gtk-deprecated.diff
# date:2008-08-01 owner:mattman type:branding
Patch4:       gtkam-04-man.diff
URL:          http://www.gphoto.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_datadir}/doc 

%define libgphoto2_version 2.1.1
%define libexif_gtk_version 0.3.2

Requires:      libgphoto2 >= %{libgphoto2_version}
Requires:      libexif-gtk >= %{libexif_gtk_version}
BuildRequires: libgphoto2 >= %{libgphoto2_version}
BuildRequires: libexif-gtk >= %{libexif_gtk_version}
BuildRequires: gimp-devel

%description
GTKam is a GTK/GNOME based tool to access Digital Cameras,
view thumbnails and download pictures from the camera.

%prep
%setup -q
bzcat %SOURCE1 | tar xf -
bzcat %SOURCE3 | tar xf -
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%if %build_l10n
sh -x %SOURCE4 --enable-sun-linguas
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
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

glib-gettextize -f
gnome-doc-common
libtoolize --force
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE4 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I ./m4m -I ./gexif-*/m4
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
		--bindir=%{_bindir} \
		--libdir=%{_libdir} \
                --includedir=%{_includedir} \
		--mandir=%{_mandir}		\
		--with-libintl-prefix=/usr
make -j $CPUS INTLLIBS= GMSGFMT=msgfmt

cd gexif-*
  glib-gettextize -f
  libtoolize --force
  intltoolize --copy --force --automake
  aclocal $ACLOCAL_FLAGS
  automake -a -c -f
  autoconf
  CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s %{?arch_ldadd}" ./configure --prefix=%{_prefix}
  make INTLLIBS= GMSGFMT=msgfmt
cd ..

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}
make DESTDIR=$RPM_BUILD_ROOT GMSGFMT=msgfmt install-strip
cd gexif-*
	make prefix=$RPM_BUILD_ROOT%{_prefix} GMSGFMT=msgfmt install-strip
cd ..


# FIXME: Remove scrollkeeper files
rm -rf $RPM_BUILD_ROOT%{_prefix}/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT;

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO
%attr(755,root,root) %{_bindir}/gtkam
%attr(755,root,root) %{_bindir}/gexif
%{_datadir}/gtkam
%{_datadir}/images/gtkam
%{_datadir}/pixmaps/*
%{_datadir}/locale/*/*/*
%{_datadir}/applications/*
%{_datadir}/gnome/help
%{_datadir}/omf/*
%{_libdir}/gimp/*/plug-ins/gtkam-gimp
%{_mandir}/man1/*

%changelog
* Tue Sep 02 2008 - matt.keenan@sun.com
- Patch to set figdir correctly on Makefile.am's for help
* Fri Aug 29 2008 - takao.fujiwara@sun.com
- Bump to 0.1.15. Fixes the part of 3149.
* Fri Aug 08 2008 - harry.fu@sun.com
- Add 'sh -x l10n-configure.sh --enable-sun-linguas' line before po-sun tarball is extracted 
* Fri Aug 01 2008 - matt.keenan@sun.com
- Add gtkam-06-man.diff Attributes man page patch
* Thu Jul 10 2008 - damien.carbery@sun.com
- Remove "-lgailutil" as libgnomecanvas build issue has been fixed.
  Add patch 05-gtk-deprecated to change GtkType to GType.
* Fri Jun 06 2008 - damien.carbery@sun.com
- Add "-lgailutil" to LDFLAGS so that libgailutil is linked in when
  libgnomecanvas is linked.  libgnomecanvas.so includes some gail functions.
* Wed Nov 28 2007 - brian.cameron@sun.com
- Add patch gtkam-04-remove-gp-gettext-flags.diff to avoid using gettext
  m4 macros.  This patch should go away when GNU gettext is added to 
  Nevada.
* Fri Oct  5 2007 - laca@sun.com
- add %{arch_ldadd} to LDFLAGS for GNU libiconv/libintl
* Thu Oct  4 2007 - laca@sun.com
- add gexit-*/m4 to the aclocal search path for AM_LC_MESSAGES, defined
  in lcmessage.m4
* Fri Jun 01 2007 - takao.fujiwara@sun.com
- Add GMSFMT=msgfmt for the workaround of bug 6559323/sourforge #1599622.
* Wed Apr 04 2007 - glynn.foster@sun.com
- Temporary addition of icon tarball to replace corrupt icons.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 06 2007 - matt.keenan@sun.com
- Update patch comments
* Tue Dec 19 2006 - brian.cameron@sun.com
- Bump to 0.1.14.  Fix patches, removing upstream patches.
* Thu Dec 14 2006 - matt.keenan@sun.com
- Remove gtkam-05-short-cut-key.diff : not needed anymore
* Tue Dec 12 2006 - takao.fujiwara@sun.com
- Added gtkam-06-g11n-i18n-menu.diff. Fixes 6488200
* Mon Jul 24 2006 - irene.huang@sun.com
- add option --with-libintl-prefix=/usr
* Mon May 29 2006 - glynn.foster@sun.com
- Remove sfw patch since we're now in /usr/bin by default.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 0.1.13.
- Remove obsolete patches -06-wall and -07-gimp-plugin. Renumber remaining.
* Fri Dec 02 2005 - srirama.sharma@wipro.com
- Added gtkam-08-sfw-path.diff to use the absolute path of the executable 
  in the .desktop file as usr/sfw/bin should not be included in $PATH.
  Fixes bug #6345489.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Sun Sep 18 2005 - glynn.foster@sun.com
- Add gimp-devel as BuildRequires, and add patch so that we install into the
  correct plugin directory.
* Fri Jul 08 2005 - damien.carbery@sun.com
- Add patch 08 to remove '-W -Wall -Wno-unused' as they do not work on Solaris.
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 0.1.12
* Thu May 05 2005 - damien.carbery@sun.com
- 6227253: Change xml file in gtkam-C.omf from gtkam.xml to
  sample_apps_info.xml (part of gnome-user-docs). Bit of a hack but a very easy
  one to maintain.
* Thu Mar 10 2005 - damien.carbery@sun.com
- Add docs tarball (Source4) to %setup section.
* Fri Feb 25 2005 - kazuhiko.maekawa@sun.com
- Added dummy l10n online help to follow base update
* Wed Feb 16 2005 - damien.carbery@sun.com
- Integrate docs tarball (gtkam-docs-0.1) from irene.ryan@sun.com.
* Fri Nov 12 2004 - laca@sun.com
- added --libdir and --bindir to configure opts so they can be redirected
  on Solaris
* Mon Oct 11 2004 - brian.cameron@sun.com
- Move gtkam-gimp plugin to lib/gimp/2.0.
* Wed Sep 15 2004 - yuriy.kuznetsov@sun.com
- Added gtkam-06-g11n-potfiles.diff
* Mon Sep 13 2004 - vinay.mandyakoppal@wipro.com
- Added code to install javahelp documents. Fixes #5096653
* Wed Aug 25 2004 - laszlo.kovacs@sun.com
- fixed man pages and docs installation
* Wed Aug 25 2004 - laszlo.kovacs@sun.com
- fixed glib-gettextize call
* Wed Aug 25 2004 - damien.carbery@sun.com
- Add unpackaged files to %files section.
* Mon Aug 09 2004 - archana.shah@wipro.com
- Added patch gtkam-05-short-cut-key.diff
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gtkam-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 18 2004 - hidetoshi.tajima@sun.com
- Run glib-gettexttize and intltoolize for both Solaris and Linux
- merge i18n patches
* Thu Jun 10 2004 - dermot.mccluskey@sun.com
- make patch5 solaris-only
* Wed Jun 02 2004 - brian.cameron@sun.com
- Added needed patches for Solaris.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gtkam-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gtkam-l10n-po-1.0.tar.bz2
* Thu Mar 18 2004 - matt.keenan@sun.com
- Bump to 0.1.11
* Thu Mar 04 2004 - takao.fujiwara@sun.com
- Updated gtkam-03-l10n-and-utf8.diff to gtkam-03-g11n-i18n-ui.diff 
  to fix 4935751, 4981813
* Thu Feb 04 2004 - matt.keenan@sun.com
- Add l10n tarball, edit to gtkam-04-gexif-i18n.diff
* Wed Feb 04 2004 - matt.keenan@sun.com
- Port Patches, gexif version
* Fri Jan 16 2004 - matt.keenan@sun.com
- Enable deprecated patch
* Thu Aug 14 2003 - matt.keenan@sun.com
- desktop file for menu entry
* Wed Jul 16 2003 - matt.keenan@sun.com
- Initial version
