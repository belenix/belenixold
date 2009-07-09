#
# spec file for package SUNWgnome-print
#
# includes module(s): libgnomeprint, libgnomeprintui
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%use gprint = libgnomeprint.spec
%use gprintui = libgnomeprintui.spec
%use printman = printman.spec

# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define g20_version sun-1.116.1

Name:                    SUNWgnome-print
Summary:                 GNOME printing technology
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
Source1:                 http://dlc.sun.com/osol/jds/downloads/extras/libgnomeprint-%{g20_version}.tar.bz2
# owner:davelam date:2008-05-14 type:bug bugzilla:532100
Patch1:                  libgnomeprint-sun-01-add-libm.diff

Source2:                 http://dlc.sun.com/osol/jds/downloads/extras/libgnomeprintui-%{g20_version}.tar.bz2
%if %build_l10n
Source3:                 l10n-configure.sh
%endif
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-print-root
Requires: SUNWgnome-libs
Requires: SUNWperl584usr
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWscplp
Requires: SUNWlibms
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWpapi
Requires: SUNWdesktop-cache
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-themes-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWpapi

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-print
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gprint.prep -d %name-%version
%gprintui.prep -d %name-%version
%printman.prep -d %name-%version

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -
bzcat %SOURCE1 | tar xf -
cd libgnomeprint-%{g20_version}
%patch1 -p1
cd ..

bzcat %SOURCE2 | tar xf -

#FIXME - hack needed because subdir gpa does not exist in libgnomeprint
cd libgnomeprint-%{gprint.version}/libgnomeprint
ln -s . private
cd ../../libgnomeprintui-%{gprintui.version}
mkdir libgnomeprint
ln -s ../../libgnomeprint-%{gprint.version}/libgnomeprint/gpa libgnomeprint/private

%build
export PKG_CONFIG_PATH=../libgnomeprint-%{gprint.version}/libgnomeprint:%{_pkg_config_path}
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export CFLAGS="%optflags"

%gprint.build -d %name-%version
%gprintui.build -d %name-%version
%printman.build -d %name-%version

cd %{_builddir}/%name-%version

export PKG_CONFIG_PATH=../libgnomeprint-%{g20_version}/libgnomeprint:%{_pkg_config_path}
cd libgnomeprint-%{g20_version}
libtoolize --force
aclocal $ACLOCAL_FLAGS
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}
make
cd ..

pwd

cd libgnomeprintui-%{g20_version}
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}
make

%install
cd %{_builddir}/%name-%version
cd libgnomeprint-%{g20_version}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1    
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL   
cd ..

cd libgnomeprintui-%{g20_version}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1    
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL   
cd ..

rm -rf $RPM_BUILD_ROOT%{_datadir}/fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/man

cd %{_builddir}
%gprint.install -d %name-%version
%gprintui.install -d %name-%version
%printman.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-print-2.0/*/lib*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/printman/gnome-print-manager-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc libgnomeprint-%{gprint.version}/AUTHORS
%doc libgnomeprint-%{gprint.version}/README
%doc(bzip2) libgnomeprint-%{gprint.version}/COPYING.LIB
%doc(bzip2) libgnomeprint-%{gprint.version}/ChangeLog
%doc libgnomeprintui-%{gprintui.version}/AUTHORS
%doc libgnomeprintui-%{gprintui.version}/README
%doc(bzip2) libgnomeprintui-%{gprintui.version}/COPYING.LIB
%doc(bzip2) libgnomeprintui-%{gprintui.version}/ChangeLog
%doc printman-%{printman.version}/AUTHORS
%doc printman-%{printman.version}/README
%doc(bzip2) printman-%{printman.version}/COPYING
%doc(bzip2) printman-%{printman.version}/ChangeLog
%doc libgnomeprint-%{g20_version}/AUTHORS
%doc libgnomeprint-%{g20_version}/README
%doc(bzip2) libgnomeprint-%{g20_version}/COPYING.LIB
%doc(bzip2) libgnomeprint-%{g20_version}/ChangeLog
%doc libgnomeprintui-%{g20_version}/AUTHORS
%doc libgnomeprintui-%{g20_version}/README
%doc(bzip2) libgnomeprintui-%{g20_version}/COPYING.LIB
%doc(bzip2) libgnomeprintui-%{g20_version}/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgnomeprint/*/modules/transports/*.so
%{_libdir}/libgnomeprint/*/modules/*.so*
%{_libdir}/libgnomeprint/*/modules/filters/*.so
%{_libdir}/lib*.so.*
%{_libdir}/gnome-print-2.0/*/lib*.so*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome-printinfo
%{_bindir}/libgnomeprint-2.0-font-install
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*
%{_datadir}/libgnomeprint
%{_datadir}/gnome-print-2.0
%{_datadir}/libgnomeprint-2.0
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-printinfo/C/
%{_datadir}/omf/printman/gnome-print-manager-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/libgnomeprintui

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-print-manager.schemas
%{_sysconfdir}/gconf/schemas/gnome-print.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/gnome-print-manager-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Jun 24 2008 - damien.carbery@sun.com
- Remove "-lgailutil" from LDFLAGS. Root cause found in gtk+: bugzilla 536430.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Add "-lgailutil" to LIBS so that libgailutil is linked in when libgnomecanvas
  is linked. libgnomecanvas.so includes some gail functions.
* Wed May 14 2008 - dave.lin@sun.com
- Add patch  libgnomeprint-sun-01-add-libm.diff to fix build error
* Th Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu Sep 27 2007 - laca@sun.com
- delete some unnecessary env variables
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Thu Jun 29 2006 - laca@sun.com
- update %post/%preun gconf scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 31 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Mon May 15 2006 - damien.carbery@sun.com
- Change omf ref in l10n package to avoid picking up C locale file.
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Add autofoo to process intltool stuff.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Wed Nov 09 2005 - damien.carbery@sun.com
- Fix share package - add applications dir, remove capplets dir.
* Fri Oct 28 2005 - damien.carbery@sun.com
- Fix removal of l10n files for non-l10n build.
* Tue Sep 20 2005 - <laca@sun.com>
- add unpackaged files to %files
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files or add to %files
* Thu May 19 2005 - brian.cameron@sun.com
- Update to 2.10, add needed calls to libtoolize, aclocal, etc for
  building the gnome 2.0 version of libgnomeprintui.
* Tue Dec 14 2004 - glynn.foster@sun.com
- Remove $(datadir)/fonts and $(datadir)/gnome-print since they've been
  removed from the original libgnomeprint.spec file.
* Sat Nov 27 2004 - laca@sun.com
- integrated the sun-gnome 2.0 versions of libgnomeprint and libgnomeprintui
  for backward compatibility, fixes 6196674
* Wed Oct 13 2004 - laca@sun.com
- added root subpkg
* Mon Oct 04 2004 - takao.fujiwara@sun.com
- Added javahelp in %file section
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added libgnomeprint, libgnomeprintui manpages
* Wed Aug 25 2004 - archana.shah@wipro.com
- Install help files in gnome-printinfo/ instead of gnome-print-manager/
  Also install help files under javahelp/
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Tue Aug 03 2004  glynn.foster@sun.com
- Add printman
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun 02 2004 - danek.duvall@sun.com
- Add PAPI support
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Sun Apr 04 2004 - laca@sun.com
- added SUNWgnome-themes build time dependency (for gnome-icon-themes)
* Fri Feb 27 2004 - <niall.power@sun.com>
- add -R%{_libdir} to LDFLAGS
