#
# spec file for package SUNWgnome-camera
#
# includes module(s): libgphoto2, gphoto2, gtkam
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc
%use libgphoto2 = libgphoto2.spec
%use gphoto2 = gphoto2.spec
%use gtkam = gtkam.spec

Name:                    SUNWgnome-camera
Summary:                 GNOME digital camera tool
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWlibusb
Requires: SUNWgnome-component
Requires: SUNWgnome-img-editor
Requires: SUNWjpg
Requires: SUNWlibexif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWmlib
Requires: SUNWdesktop-cache
Requires: SUNWdbus
Requires: SUNWdsdu
Requires: SUNWltdl
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibpopt-devel
# gtkam builds a gimp plug-in, so SUNWgnome-img-editor is a dependancy
BuildRequires: SUNWgnome-img-editor-devel
BuildRequires: SUNWgnu-gettext
BuildRequires: SUNWlibusb
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdsdu
BuildRequires: SUNWlibtool
BuildRequires: SUNWltdl

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libgphoto2.prep -d %name-%version
%gphoto2.prep -d %name-%version
%gtkam.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
# note: This ACLOCAL_FLAGS setting seems unnecessary, but it's
# needed so that gettext.m4 is used from /usr/share/aclocal and
# not from ./m4m
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-R/usr/sfw/lib"

%libgphoto2.build -d %name-%version

export PKG_CONFIG_PATH=%{_builddir}/%name-%version/libgphoto2-%{libgphoto2.version}:%{_builddir}/%name-%version/libgphoto2-%{libgphoto2.version}/libgphoto2_port:%{_pkg_config_path}

%gphoto2.build -d %name-%version

%gtkam.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libgphoto2.install -d %name-%version
%gphoto2.install -d %name-%version
%gtkam.install -d %name-%version

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/var
# Remove source code files (AUTHORS, README, CHANGELOG etc)
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/gtkam
# Remove Linux specific hotplug stuff
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gphoto2
%{_bindir}/gtkam
%{_bindir}/gexif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/libgphoto2
%{_libdir}/libgphoto2_port
%{_libdir}/gimp
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%doc libgphoto2-%{libgphoto2.version}/AUTHORS
%doc(bzip2) libgphoto2-%{libgphoto2.version}/COPYING
%doc(bzip2) libgphoto2-%{libgphoto2.version}/ChangeLog
%doc(bzip2) libgphoto2-%{libgphoto2.version}/NEWS
%doc(bzip2) libgphoto2-%{libgphoto2.version}/README.in
%doc libgphoto2-%{libgphoto2.version}/libgphoto2_port/AUTHORS
%doc libgphoto2-%{libgphoto2.version}/libgphoto2_port/NEWS
%doc libgphoto2-%{libgphoto2.version}/libgphoto2_port/README
%doc(bzip2) libgphoto2-%{libgphoto2.version}/libgphoto2_port/COPYING.LIB
%doc(bzip2) libgphoto2-%{libgphoto2.version}/libgphoto2_port/ChangeLog
%doc gphoto2-%{gphoto2.version}/NEWS
%doc(bzip2) gphoto2-%{gphoto2.version}/COPYING
%doc(bzip2) gphoto2-%{gphoto2.version}/ChangeLog
%doc(bzip2) gphoto2-%{gphoto2.version}/README
%doc gtkam-%{gtkam.version}/AUTHORS
%doc gtkam-%{gtkam.version}/CHANGES
%doc gtkam-%{gtkam.version}/NEWS
%doc gtkam-%{gtkam.version}/README
%doc(bzip2) gtkam-%{gtkam.version}/COPYING
%doc(bzip2) gtkam-%{gtkam.version}/ChangeLog
%doc gtkam-%{gtkam.version}/gexif-%{gtkam.gexif_version}/AUTHORS
%doc gtkam-%{gtkam.version}/gexif-%{gtkam.gexif_version}/ChangeLog
%doc(bzip2) gtkam-%{gtkam.version}/gexif-%{gtkam.gexif_version}/COPYING
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/gphoto2/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gtkam/C
%{_datadir}/gtkam
%{_datadir}/images
%{_datadir}/libgphoto2
%{_datadir}/omf/*/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gphoto2-port-config
%{_bindir}/gphoto2-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Sep 10 2008 - matt.keenan@sun.com
- Update copyright
* Fri Aug 29 2008 - takao.fujiwara@sun.com
- Add SUNWgnu-gettext build require for gtkam .mo.
* Tue Jun 24 2008 - damien.carbery@sun.com
- Remove "-lgailutil" from LDFLAGS. Root cause found in gtk+: bugzilla 536430.
* Fri Jun 06 2008 - dmaien.carbery@sun.com
- Add "-lgailutil" to LDFLAGS so that libgailutil is linked in when
  libgnomecanvas is linked.  libgnomecanvas.so includes some gail functions.
* Mon Mar 03 2007 - matt.keenan@sun.com
- Remove udev files as udev not supported on solaris
* Mon Dec 17 2007 - patrick.ale@gmail.com
- Add Build/Requires SUNWltdl
- Remove Requires: SUNWlibtool
* Fri Dec  1 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWlibtool.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Oct  4 2007 - laca@sun.com
- define ACLOCAL_FLAGS
* Mon Aug 13 2007 - brian.cameron@sun.com
- Clean up.
* Tue Feb 13 2007 - brian.cameron@sun.com
- Add lib/udev to packaging - new directory in 2.3.1.
* Fri Feb 09 2007 - brian.cameron@sun.com
- Add SUNWdbus dependency since libgphoto2 requires D-Bus.
* Tue Dec 19 2006 - brian.cameron@sun.com
- Rework spec file after updating gtkam, libgphoto2, gphoto2 spec files.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Tue Jul 25 2006 - damien.carbery@sun.com
- Fix 'rm .omf' line to not delete the C locale file.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon May 15 2006 - damien.carbery@sun.com
- Correct l10n package perms.
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Apr 4 2006 - glynn.foster@sun.com
- Remove the hotplug stuff which is Linux specific. This
  cuts out the -root package currently.
* Tue Apr 4 2006 - glynn.foster@sun.com
- Move gphoto2-config into the -devel package.
* Wed Mar 15 2006 - damien.carbery@sun.com
- Add to Build/Requires after running check-deps.pl.
* Mon Jan 09 2006 - damien.carbery@sun.com
- Add SUNWlibusb dependency to get libusb-config.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Sep 30 2005 - damien.carbery@sun.com
- Add root package for _sysconfdir files. Remove javahelp references.
  Delete .la files and others before packaging.
* Mon Dec 13 2004 - damien.carbery@sun.com
- Move to /usr/sfw to implement ARC decision.
* Sun Nov 14 2004 - laca@sun.com
- add /usr/demo/jds/lib to RPATH
* Fri Nov 12 2004 - laca@sun.com
- move to /usr/demo/jds
* Mon Oct 11 2004 - brian.cameron@sun.com
- Corrected packaging of gimp plugin.
* Wed Oct 06 2004 - matt.keenan@sun.com
- added l10n help files section
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Sep 13 2004  vinay.mandyakoppal@wipro.com
- Added code to install javahelp documents. Fixes #5096653.
* Thu Sep 09 2004  kaushal.kumar@wipro.com
- Moved %{_datadir}/pixmaps to '%files share' from '%files l10n'.
  Put %{_datadir}/omf/*/*-C.omf under '%files share'.
* Sun Sep 05 2004 - laca@sun.com
- removed root subpkg as it only contained 2 linux specific files (#5097102)
* Tue Aug 24 2004 - brian.cameron@sun.com
- Remove %{_datadir}/doc from install since these docs are not useful
  to install
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Sun Jun 27 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Mon Jun 07 2004 - brian.cameron@sun.com
- Moved libexif to SUNWlibexif and libexif-gtk to SUNWgnome-libs since
  nautilus also uses these libraries if available.
* Wed Jun 02 2004 - brian.cameron@sun.com
- Added gtkam to package.
* Wed Jun 02 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Mon May 03 2004 - laca@sun.com
- renamed to SUNWgnome-camera
* Fri Mar 31 2004 - brian.cameron@sun.com
- Created,
