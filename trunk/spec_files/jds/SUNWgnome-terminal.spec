#
# spec file for package SUNWgnome-terminal
#
# includes module(s): vte gnome-terminal
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%use vte = vte.spec
%use gterminal = gnome-terminal.spec

Name:                    SUNWgnome-terminal
Summary:                 GNOME terminal emulator
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-component
Requires: SUNWgnome-vfs
Requires: SFEncurses
Requires: SUNWperl584usr
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWPython
Requires: SUNWgnome-python-libs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWxwxft
Requires: SUNWdesktop-cache
Requires: %{name}-root
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SFEncurses-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWgtk-doc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package  devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWperl584usr
Requires: SUNWgnome-base-libs

%prep
rm -rf %name-%version
mkdir %name-%version
%vte.prep -d %name-%version
%gterminal.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

cd %{_builddir}/%name-%version/gnome-terminal-%{gterminal.version}
ln -s ../vte-%{vte.version}/src vte

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
%vte.build -d %name-%version

export PKG_CONFIG_PATH="../vte-%{vte.version}:%{_pkg_config_path}"
%gterminal.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vte.install -d %name-%version
%gterminal.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

#rmdir $RPM_BUILD_ROOT/usr/var

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif
rm -rf $RPM_BUILD_ROOT/var

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%attr (-, root, bin) %{_libdir}/python*
%attr (0711, root, bin) %{_libexecdir}/gnome-pty-helper
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%doc gnome-terminal-%{gterminal.version}/AUTHORS
%doc gnome-terminal-%{gterminal.version}/README
%doc(bzip2) gnome-terminal-%{gterminal.version}/ChangeLog
%doc(bzip2) gnome-terminal-%{gterminal.version}/ChangeLog.README
%doc(bzip2) gnome-terminal-%{gterminal.version}/ChangeLog.pre-2-23
%doc(bzip2) gnome-terminal-%{gterminal.version}/COPYING
%doc(bzip2) gnome-terminal-%{gterminal.version}/NEWS
%doc vte-%{vte.version}/AUTHORS
%doc vte-%{vte.version}/README
%doc(bzip2) vte-%{vte.version}/COPYING
%doc(bzip2) vte-%{vte.version}/ChangeLog
%doc(bzip2) vte-%{vte.version}/po/ChangeLog 
%doc(bzip2) vte-%{vte.version}/gnome-pty-helper/ChangeLog
%doc(bzip2) vte-%{vte.version}/NEWS
%doc(bzip2) vte-%{vte.version}/gnome-pty-helper/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/gnome-terminal
%{_datadir}/omf/*/*-C.omf
%{_datadir}/vte
%dir %attr (0755, root, bin) %{_datadir}/pygtk
%dir %attr (0755, root, bin) %{_datadir}/pygtk/2.0
%dir %attr (0755, root, bin) %{_datadir}/pygtk/2.0/defs
%{_datadir}/pygtk/2.0/defs/vte.defs
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/vte
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Mar 18 2009 - halton.huo@sun.com
- Add BuildRequires: SUNWgtk-doc
* Tue Jan 20 2009 - brian.cameron@sun.com
- Fix packaging after bumping gnome-terminal to 2.25.5.
* Sat Dec 27 2008 - dave.lin@sun.com
- Add -I/usr/gnu/include in CFLAGS.
* Fri Dec 26 2008 - halton.huo@sun.com
- Remove /usr/sfw from CFLAGS and LDFLAGS since freetype2 is avail in /usr
- Add Requires:SUNWncurses and BuildRequires:SUNWncurses-devel
- Add "-L/usr/gnu/lib -R/usr/gnu/lib" to LDFLAGS since ncurses ship libraries
  under /usr/gnu/lib
- Update %files because vte upgrading
* Wed Sep 24 2008 - christian.kelly@sun.com 
- Take out doc po/ChangeLog from files as it's no longer there.
* Mon Sep 15 2008 - brian.cameron@sun.com
- Add new copyright files.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Remove %{_datadir}/pixmaps from %files as no files delivered there.
* Fri Mar 28 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Tue Nov 06 2007 - brian.cameron@sun.com
- Add -R/usr/sfw/lib to LDFLAGS (-L/usr/sfw/lib was already there)
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
- delete some unneeded env vars
* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of /var dir as it is no longer installed.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Wed Jan 24 2007 - damien.carbery@sun.com
- Add to LDFLAGS to find libXrender.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Thu Jul 27 2006 - damien.carbery@sun.com
- Delete scrollkeeper files before packaging.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun  2 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Feb 21 2006 - damien.carbery@sun.com
- Add X packages to Requires after running check-deps.pl script.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Remove application-registry from %files as it is no longer installed.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Wed Nov 30 2005 - damien.carbery@sun.com
- Add Build/Requires on SUNWPython/-devel and SUNWgnome-python-libs/-devel.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue Sep 20 2005 - laca@sun.com
- update Python paths
* Fri Sep 16 2005 - laca@sun.com
- remove unpackaged files to add to %files
* Thu Sep 01 2005 - damien.carbery@sun.com
- Add /usr/sfw/lib/pkgconfig to PKG_CONFIG_PATH so that pygtk2 can be found.
* Thu May 19 2005 - brian.cameron@sun.com
- Update to 2.10
* Fri Oct 15 2004 - narayana.pattipati@wipro.com
- Remove SGID bit from gnome-pty-helper. Fixes bugtraq bug#5091209.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added libvte.3, vte.1 manpages
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Updated files section to extract only l10n contents 
* Mon Aug 23 2004 - shirley.woo@sun.com
- Bug 5090964 : remove l10n entries from base package into -l10n package
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004  damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Thu Jul 08 2004  ghee.teo@sun.com
- Updated SUNWgnome-terminal.spec to make sure that gnome-pty-helper
  has permission 2711 instead of 2755 so these are the same for
  both Solaris and Linux.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Sat Mar 06 2004 - laca@sun.com
- set LDFLAGS
* Sun Feb 29 2004 - laca@sun.com
- remove dependency on SUNWgnome-libs-share and SUNWgnome-libs-root, they
  are taken care by SUNWgnome-libs; fix gconf permissions
- add -D__STDC_VERSION__=199409L instead of -xc99=none
* Mon Feb 23 2004 - <niall.power@sun.com>
- install gconf schemas at end of install stage.
- run rm -Rf during clean stage.
