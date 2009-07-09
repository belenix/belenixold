#
# spec file for package SUNWgnome-archive-mgr
#
# includes module(s): file-roller
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc

%use froller = file-roller.spec

Name:                    SUNWgnome-archive-mgr
Summary:                 GNOME archive manager
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWgnome-archive-mgr-root
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-config
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWdesktop-cache
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWlibpopt-devel

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

%prep
rm -rf %name-%version
mkdir %name-%version
%froller.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags -I%{_includedir}/gnome-vfs-2.0 -I%{_libdir}/gnome-vfs-2.0/include"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH=%{_pkg_config_path}
export LDFLAGS="%_ldflags -L%{_libdir} -lgnomevfs-2"

%froller.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%froller.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

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
%{_libdir}/file-roller
%{_libdir}/nautilus
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/file-roller
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/file-roller/C
%{_datadir}/omf/file-roller/*-C.omf
%attr (-, root, other) %{_datadir}/icons
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc -d file-roller-%{froller.version} README AUTHORS
%doc(bzip2) -d file-roller-%{froller.version} COPYING ChangeLog NEWS help/ChangeLog po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/file-roller.schemas

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 17 2009 - dave.lin@sun.com
- Add %{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf in %files l10n.
* Wed Sep 10 2008 - matt.keenn@sun.com
- Update copyright
* Thu Jan 10 2008 - damien.carbery@sun.com
- Add gnome-vfs info to CFLAGS and LDFLAGS as configure no longer retrieves
  them with pkg-config (libnautilus-extension depends on gio instead of
  gnome-vfs).
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Mon Mar 20 2007 - damien.carbery@sun.com
- Remove omf deletion line from %install, as suggested by reborg on
  desktop-discuss.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Update l10n code for omf files as some locales have been removed.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Update %files for 2.17.2 tarball.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Mon Aug 21 2006 - damien.carbery@sun.com
- Fix l10n package - C locale omf file was in base and l10n package.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu Jun  1 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue Apr 18 2006 - damien.carbery@sun.com
- Icons have moved to %{_datadir}/icons, from pixmaps.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Remove mime-info from %files. No files installed now.
* Sun Jan 22 2006 - damien.carbery@sun.com
- Remove application-registry from share package as no longer installed.
* Mon Jan 09 2006 - damien.carbery@sun.com
- Remove bonobo files from base package as they are no longer installed.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Revised files section
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 01 2004 - <laca@sun.com>
- define PERL5LIB
- fix share subpkg contents/permissions
* Wed Feb 25 2004 - <niall.power@sun.com>
- inital Solaris spec file created

