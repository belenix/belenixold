#
# spec file for package file-roller
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:         file-roller
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An archive manager for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/file-roller/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source2:      l10n-configure.sh
%if %build_l10n
Source3:                 l10n-configure.sh
%endif
# date:2003-07-24 type:branding owner:gman
Patch1:       file-roller-01-menu-entry.diff
# date:2009-04-26 type:bug doo #8286 owner:harry.fu@sun.com
Patch2:       file-roller-02-add-folder.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}
Autoreqprov:  on
Prereq:       GConf

%define scrollkeeper_version 0.3.14
%define nautilus_version 2.6.1

BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: nautilus-devel >= %{nautilus_version}
Requires: nautilus >= %{nautilus_version}

%description
File Roller is an archive manager for the GNOME environment.  This means that
you can : create and modify archives; view the content of an archive; view a
file contained in the archive; extract files from the archive.
File Roller is only a front-end (a graphical interface) to archiving programs
like tar and zip. The supported file types are -

 * Tar archives uncompressed (.tar) or compressed with
 * gzip (.tar.gz , .tgz)
 * bzip (.tar.bz , .tbz)
 * bzip2 (.tar.bz2 , .tbz2)
 * compress (.tar.Z , .taz)
 * lzop (.tar.lzo , .tzo)
 * Zip archives (.zip)
 * Jar archives (.jar , .ear , .war)
 * Lha archives (.lzh)
 * Rar archives (.rar)
 * Single files compressed with gzip, bzip, bzip2, compress, lzop

%prep
%setup -q
%if %build_l10n
#bugster 6643604 
sh -x %SOURCE2 --disable-gnu-extensions
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p2
for po in po/*.po; do
  dos2unix -ascii $po $po
done

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

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

#FIXME: Disable scrollkeeper for now.
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --sysconfdir=%{_sysconfdir} \
    --disable-scrollkeeper
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

rm $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/libnautilus-fileroller.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="file-roller.schemas"
 for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README COPYING
%{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/file-roller
%{_libdir}/nautilus/extensions-2.0/libnautilus-fileroller.so
%{_datadir}/applications/*.desktop
%{_datadir}/file-roller
%{_datadir}/gnome/help/file-roller
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/file-roller
%{_datadir}/pixmaps/*.png

%changelog
* Sat Apr 26 2009 - harry.fu@sun.com
- Add patch to fix doo bug #8286.
* Wed Apr 15 2009 - dave.lin@sun.com
- Bump to 2.26.1
- Removed upstreamed patch 02-zip-crash.diff.
* Wed Apr 08 2009 - matt.keenan@sun.com
- Remove original 02-zip-crash.diff as fixed in 2.26.0
- Create new 02-zip-crash.diff for doo bug 7965
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Wed Feb 18 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.90
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.2
* Mon Sep 29 2008 - patrick.ale@gmail.com
- Correct download URL
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.6
* Mon Aug 11 2008 - matt.keenan@sun.com
- New patch for zip view crash 02-zip-crash.diff
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.3.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.2.
* Fri Jan 11 2008 - damien.carbery@sun.com
- Update path to nautilus extension dir s/extensions-1.0/extensions-2.0/.
* Mon Jan 07 2008 - damien.carbery@sun.com
- Bump to 2.21.1.
* Wed Dec 26 2007 - harry.fu@sun.com
- Add l10n-configure.sh to remove "%-m" and "%-d". Fixes 6643604
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.2.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Sep 04 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jul 11 2007 - matt.keenan@sun.com
- Remove obsolete patch file-roller-02-properties-dialog-crash.diff
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Wed May 09 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Thu Mar 01 2007 - matt.keenan@sun.com
- Add patch file-roller-02-properties-dialog-crash.diff
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Add --libexecdir to configure call.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Remove upstream patch, 02-rpm-cpio.
* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Wed Oct 04 2006 - matt.keenan@sun.com
- Add patch 02-rpm-cpio.diff : bugster : 6478062, bugzilla : 359629
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Wed Sep 27 2006 - matt.keenan@sun.com
- file-roller-01-rename-contents.diff : bugster:6232106 / bugzilla:168287
- Remove fixed upstream.
* Wed Sep 27 2006 - matt.keenan@sun.com
- Remove patch 01-zip-command.diff, re-enable password option for archives 
  CR 6397899.
- Re-align the remaining patches.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.93.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.1.
* Fri Jun 02 2006 - glynn.foster@sun.com
- Add patch to update the menu entry.
* Wed Apr 19 2006 - damien.carbery@sun.com
- Call dos2unix to fix po files.
* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Remove obsolete patch, 01-rm-jar-association. Reorder remainder.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Sun Jan 22 2006 - damien.carbery@sun.com
- Remove upstream patch, 02-move-menuitem. Renumber rest.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Sat Jan 07 2006 - damien.carbery@sun.com
- Remove ref to bonobo files that are no longer present.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri May 20 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.3
* Tue Mar 15 2005 - laszlo.kovacs@sun.com
- add patch for 6238712
* Wed Mar 02 2005 - glynn.foster@sun.com
- Add patch so that renaming archive contents, prompts for an
  overwrite if the file/directory already exists.
* Tue Jan 25 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from maeve.anslow@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Mon Oct 18 2004 - laszlo.kovacs@sun.com
- file-roller-09-extract-password.diff added
* Fri Sep 10 2004 - kaushal.kumar@wipro.com
- Added patch file-roller-08-fix-dnd-crash.diff to fix the desktop icon
  dnd crash. Fixes bugtraq #5098546.
* Mon Aug 30 2004 - takao.fujiwara@sun.com
- Add file-roller-07-g11n-potfiles.diff
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents
* Fri Aug 20 2004 - damien.carbery@sun.com
- Integrate updated docs tarball from breda.mccolgan@sun.com.
* Thu Aug 05 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Tue Jul 27 2004 - vijaykumar.patwari@wipro.com
- Fix the file extraction for .zip/.jar.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to file-roller-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jul 05 2004 - kaushal.kumar@wipro.com
- Added patch file-roller-05-add-folder-option.diff to add the feature of 
  folder addition in an archive.
* Wed Jun 09 2004 - balamurali.viswanathan@wipro.com
- Modified patch file-roller-04-set-path-gtar.diff to use putenv instead of
  setenv
* Wed Jun 09 2004 - balamurali.viswanathan@wipro.com
- Added patch file-roller-04-set-path-gtar.diff to /usr/sfw/bin so that
  gtar is picked up instead of tar
* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Fri May 14 2004 - balamurali.viswanathan@wipro.com
- Don't show the password in plain text: file-roller-03-password-invisible.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to file-roller-l10n-po-1.1.tar.bz2
* Tue May 04 2004 - glynn.foster@sun.com
- Bump to 2.6.1
* Tue Apr 27 2004 - vijaykumar.patwari@wipro.com
- Move the position of "Archive Manager" from "System Tools"
  to "Accessories" in panel menu.
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Tue Apr 13 2004 - laszlo.kovacs@sun.com
- upgraded tarball
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to file-roller-l10n-po-1.0.tar.bz2
* Tue Mar 16 2004 - glynn.foster@sun.com
- Remove validation of archive check since the patch is 
  wrong.
* Tue Mar 16 2004 - glynn.foster@sun.com
- Bump to 2.5.7 and remove localized documentation
  tarball as it no longer makes sense. Remove the menu
  patch and l10n patches.
* Wed Feb 25 2004 - niall.power@sun.com
- change tar jxvf to bzcat | tar xf - 
- use proper path macros instead of hardcoded paths
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 2.5.4, re-apply patches 01/02
- Add l10n and patch 03
- Add libtoolize/automake etc...
* Wed Dec 17 2003 - glynn.foster@sun.com
- Bump to 2.5.0
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the Sun Supported keyword from the 
  desktop file.
* Mon Oct 13 2003 - Laszlo.Kovacs@sun.com
- tarball upgrade
* Fri Sep 26 2003 - <laca@sun.com>
- integrate Sun docs
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Thu Aug 07 2003 - glynn.foster@sun.com
- Update tarball, bump version, reset release.
* Wed Jul 30 2003 - Laszlo Kovacs@sun.com
- added file-roller-02-validate-new-archive.diff
* Tue May 13 2002 - Niall.Power@Sun.COM
- initial package for GNOME 2.2
