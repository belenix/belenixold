#
# spec file for package bug-buddy
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
Name:         bug-buddy
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Bug Reporting Tool
Source:       http://ftp.gnome.org/pub/GNOME/sources/bug-buddy/2.26/bug-buddy-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# date:2004-11-08 type:feature owner:mattman bugster:5102045 bugzilla:473559
Patch1:       bug-buddy-01-use-pstack.diff
# date:2007-09-07 type:bug owner:mattman bugster:6600538
Patch2:       bug-buddy-02-dlopen-java.diff
# date:2008-11-12 type:bug owner:mattman bugster:6783977
Patch3:       bug-buddy-03-disable-google-breakpad.diff
# date:2009-03-11 type:bug owner:mattman bugster:6652623
Patch4:       bug-buddy-04-printf-null-crash.diff
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/bug-buddy
Autoreqprov:  on

%define libgnomeui_version 2.6.0
%define scrollkeeper_version 0.3.14
%define gnome_desktop_version 2.6.1
%define gnome_doc_utils_version 0.2.0

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gnome-desktop >= %{gnome_desktop_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
Requires: libgnomeui >= %{libgnomeui_version}
Prereq: GConf

%description
Bug Buddy for the GNOME 2.6 Desktop has been ported from the GNOME 1.x releases. Its purpose is to make bug-reporting for end-users as easy as possible. It can generate backtraces of crashes and include the information with the bugreport.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
export CFLAGS="%{optflags} -features=extensions"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags}"

libtoolize --force
glib-gettextize --copy --force
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
automake -a -c -f

# FIXME: Disable scrollkeeper for now 
CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
	    --mandir=%{_mandir} \
	    --disable-scrollkeeper
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

rm -f $RPM_BUILD_ROOT%{_datadir}/applications/bug-buddy*.desktop
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="bug-buddy.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/bug-buddy/bug-buddy.*
%{_datadir}/bug-buddy/gdb-cmd
%{_datadir}/bug-buddy/gnome.png
%{_datadir}/bug-buddy/bugzilla/*
%{_datadir}/gnome/help/bug-buddy/*
%{_datadir}/mime-info/*
%{_bindir}/bug-buddy
%{_datadir}/omf/bug-buddy/*.omf
%{_datadir}/pixmaps/*.png
%{_datadir}/man/man1/bug-buddy.1.gz
%{_sysconfdir}/gconf/schemas/bug-buddy.schemas
%{_datadir}/application-registry/*.applications
%{_libdir}/gtk-2.0/modules/*
 

%changelog
* Mon Mar 23 2009 - matt.keenn@sun.com
- Add delivery of 64bit version of libgnomebreakpad.so #6819745
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Wed Mar 11 2009 - matt.keenan@sun.com
- Add patch -04-printf-null-crash.diff, ensure bug-buddy does not crash
  because of NULL paramater to printf, this can be removed when  ARC Case
  http://sac.sfbay/PSARC/2008/403/ gets approved and integrated into nevada.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Thu Dec 11 2008 - matt.keenan@sun.com
- Rework patches 01 and 02 for new tarball, also create new patch 
- 03 to disable building google-breakpad.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Sep 23 2008 - matt.keenan@sun.com
- Bump to 2.24.0.
- Rework patches bug-buddy-01-use-pstack.diff, bug-buddy-02-dlopen-java.diff
- Remove patch bug-buddy-03-disable-google-breakpad.diff applied upstream
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91.1.
* Mon Sep 01 2008 - matt.keenan@sun.com
- Remove patch 01-enable-breakpad, partially fixed upstream, rest of patch has
  been merged into patch 01.
- Merge part of patch 01-enable-breakpad into 01-use-pstack.
- Re-number remaining patches
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.1.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Fri Oct 19 2007 - matt.keenan@sun.com
- Temporary patch to disable google breakpad
* Fri Sep 28 2007 - damien.carbery@sun.com
- Delete libgnomebreakpad.[a|la].
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Fri Aug 31 2007 - matt.keenan@sun.com
- Rename patch 02 from disable to enable
* Tue Aug 28 2007 - matt.keenan@sun.com
- Bump to 2.19.91
* Tue Aug 28 2007 - matt.keenan@sun.com
- Bump back to 2.19.0
- Rework bug-buddy-01-use-pstack.diff
- Add new patch bug-buddy-02-disable-breakpad.diff so that it compiles
* Thu Aug 14 2007 - damien.carbery@sun.com
- Unbump to 2.18.1 to get module to build.
* Thu Aug 09 2007 - damien.carbery@sun.com
- Add patch, 02-solaris-int, to fix some Solaris specific issues.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.0.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.4. Remove deletion of ximian.png as the file is not installed.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.0.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Tue Jan 17 2006 - glynn.foster@sun.com
- Bump 2.13.0
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.01.
* Fri Aug 05 2005 - glynn.foster@sun.com
- Remove the bug reporting branding patch for the moment - we don't even
  ship bug buddy with Solaris, but now with opensolaris.org we should point
  to upstream.
* Fri May 20 2005 - glynn.foster@sun.com
- Update to 2.10.0
* Thu Mar 31 2005 - damien.carbery@sun.com
- Updated docs tarball (bug-buddy-docs-0.6linux) from maeve.anslow@sun.com.
* Wed Feb 09 2005 - damien.carbery@sun.com
- Integrated updated Linux specific docs tarball from maeve.anslow@sun.com.
  Added %ifos to accomodate this.
* Thu Jan 27 2005 - kazuhiko.maekawa@sun.com
- Put l10n help tarball for Cinnabar-linux
* Tue Jan 25 2005 - glynn.foster@sun.com
- Bring back bug-buddy into the Linux build, removing and merging
  some patches.
* Mon Nov 08 2004 - leena.gunda@wipro.com
- Added bug-buddy-05-use-pstack.diff to use pstack to get the stack 
  trace on Solaris as gdb is not available. Fixes bug #5102045.
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents with patch
* Fri Aug 20 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs tarball from breda.mccolgan@sun.com
- Added patch to compensate for Makefiles removed from new tarball.
* Wed Jul 21 2004 - damien.carbery@sun.com
- Add patch to remove --export-dynamic which breaks Solaris build.
- Add $ACLOCAL_FLAGS to build on Solaris.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to bug-buddy-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to bug-buddy-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to bug-buddy-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - glynn.foster@sun.com
- Bump to 2.6.0
* Tue Mar 16 2004 - glynn.foster@sun.com
- Bump to 2.5.92. Remove localized online help since it's upstream
  in the tarball. Remove help button since we're working from head
  and we'll get it with the next iteration. Remove random branding
  in the user interface, just increases more time spent doing pointless
  localizations. Remove the ximian branding patch, since it needs to be
  redone, and we shouldn't do the sendmail edits in that patch.
* Tue Mar 16 2004 - glynn.foster@sun.com
- Removed man, menu patches since we're doing this in spec file now.
  Merged potfile patches and reorder the rest.
* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added bug-buddy-09-g11n-potfiles.diff
* Wed Mar 03 2004 - balamurali.viswanathan@wipro.com
- Added patch bug-buddy-08-enable-help.diff to provide help.
* Mon Feb 23 2004 - matt.keenan@sun.com
- Bump to 2.5.3, update l10n
- Re-merge all patches
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 2.5.1
* Thu Nov 13 2003 - glynn.foster@sun.com
- Remove menu entry
* Fri Oct 10 2003 - niall.power@sun.com
- Updated to version 2.4.0
* Thu Oct 9 2003 - Laca@sun.com
- removed %post, fixed %files list and removed ximian.png.
* Wed Sep 17 2003 - matt.keenan@sun.com
- Man page change, package tarball version of man page
* Tue Aug 19 2003 - Laszlo.Kovacs@sun.com
- add bug-buddy-04-remove-ximian-druid-pages.diff
* Tue Aug 05 2003 - Laszlo.Kovacs@sun.com
- add bug-buddy-03-sensical-check-removed.diff
* Tue Aug 05 2003 - glynn.foster@sun.com
- Update tarball, bump version, reset release.
* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu category thing
* Tue May 13 2003 - matt.keenan@sun.com
- initial Sun Release
