#
# spec file for package SUNWgnome-file-mgr
#
# includes module(s): eel, nautilus, gnome-mount,
#                     gnome-volume-manager
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen

%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use eel = eel.spec
%use nautilus = nautilus.spec
%use open_terminal= nautilus-open-terminal.spec

%if %with_hal
%use gmount = gnome-mount.spec
%endif

Name:                    SUNWgnome-file-mgr
Summary:                 GNOME file manager
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWlibunique-devel
BuildRequires: SUNWgtk-doc
Requires: SUNWgtk2
Requires: SUNWgnome-file-mgr-root
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-config
Requires: SUNWgnome-panel
Requires: SUNWgnome-print
Requires: SUNWgnome-audio
Requires: SUNWgnome-component
Requires: SUNWlibunique
Requires: SUNWlibexif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlibrsvg
Requires: SUNWperl584usr
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWzfsr
Requires: SUNWdesktop-cache
%if %with_hal
Requires: SUNWhal
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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
%eel.prep -d %name-%version
%nautilus.prep -d %name-%version
%open_terminal.prep -d %name-%version

%if %with_hal
%gmount.prep -d %name-%version
%endif
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

export PKG_CONFIG_PATH=../eel-%{eel.version}:../nautilus-%{nautilus.version}/libnautilus-extension:%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir} -DGNOME_DESKTOP_USE_UNSTABLE_API"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

%eel.build -d %name-%version
%nautilus.build -d %name-%version
%open_terminal.build -d %name-%version

%if %with_hal
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lX11 -lresolv"
%gmount.build -d %name-%version
%endif

%install
rm -rf $RPM_BUILD_ROOT
%eel.install -d %name-%version
%nautilus.install -d %name-%version
%open_terminal.install -d %name-%version

%if %with_hal
%gmount.install -d %name-%version
%endif

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# generated in the postinstall scripts (update-mime-database)
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache mime-types-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache mime-types-cache

%files
%doc eel-%{eel.version}/AUTHORS eel-%{eel.version}/MAINTAINERS 
%doc eel-%{eel.version}/README
%doc(bzip2) eel-%{eel.version}/COPYING eel-%{eel.version}/COPYING.LIB 
%doc(bzip2) eel-%{eel.version}/NEWS eel-%{eel.version}/ChangeLog
%doc gnome-mount-%{gmount.version}/AUTHORS gnome-mount-%{gmount.version}/README
%doc(bzip2) gnome-mount-%{gmount.version}/COPYING 
%doc(bzip2) gnome-mount-%{gmount.version}/NEWS 
%doc(bzip2) gnome-mount-%{gmount.version}/ChangeLog
%doc nautilus-%{nautilus.version}/README
%doc nautilus-%{nautilus.version}/AUTHORS
%doc nautilus-%{nautilus.version}/MAINTAINERS
%doc(bzip2) nautilus-%{nautilus.version}/COPYING
%doc(bzip2) nautilus-%{nautilus.version}/NEWS
%doc(bzip2) nautilus-%{nautilus.version}/ChangeLog
%doc nautilus-open-terminal-%{open_terminal.version}/AUTHORS
%doc nautilus-open-terminal-%{open_terminal.version}/README
%doc(bzip2) nautilus-open-terminal-%{open_terminal.version}/COPYING
%doc(bzip2) nautilus-open-terminal-%{open_terminal.version}/NEWS
%doc(bzip2) nautilus-open-terminal-%{open_terminal.version}/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/bonobo/servers
%{_libdir}/nautilus/extensions-2.0/*.so
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%if %with_hal
%dir %attr (0755, root, other) %{_datadir}/gnome-mount
%{_datadir}/gnome-mount/*
%endif
%{_datadir}/gtk-doc
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/nautilus.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/nautilus.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/nautilus.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/nautilus.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/nautilus.svg
%{_datadir}/nautilus
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/apps_nautilus_preferences.schemas
%{_sysconfdir}/gconf/schemas/nautilus-open-terminal.schemas
%if %with_hal
%{_sysconfdir}/gconf/schemas/gnome-mount.schemas
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 19 2009 - jeff.cai@sun.com
- Remove gnome-volume-manager since it is obsolete in GNOME 2.26.
* Tue Feb 10 2009 - halton.huo@sun.com
- Add BuildRequires: SUNWlibunique-devel, Requires: SUNWlibunique
- Add Requires: SUNWzfsr to fix issue #1 for CR6753371
* Thu Jan 08 2009 - christian.kelly@sun.com
- Add dependency on libunique.
* Thu Sep 11 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Wed Jun 04 2008 - damien.carbery@sun.com
- Update %files (add %{_datadir}/gtk-doc).
* Thu May 01 2008 - damien.carbery@sun.com
- Update %files (remove %{_datadir}/gnome and add %{_sysconfdir}/xdg) after
  bumping gnome-volume-manager.
* Fri Feb 29 2008 - damien.carbery@sun.com
- Add nautilus-open-terminal.schemas to %files and %preun root.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Add -DGNOME_DESKTOP_USE_UNSTABLE_API to CFLAGS to get it to build.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Set ACLOCAL_FLAGS to pick up the modified intltool.m4.
* Fri Jan 11 2008 - padraig.obriain@sun.com
- Change extensions directory to extensions-2.0
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X dep
* Wed Sep 05 2007 - damien.carbery@sun.com
- Remove references to SUNWgnome-a11y-base-libs as its contents have been
  moved to SUNWgnome-base-libs.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Tue Dec 19 2006 - damien.carbery@sun.com
- Update %files for new graphics files.
* Fri Oct 20 2006 - damien.carbery@sun.com
- Remove SUNWhalh BuildRequires because header files are in SUNWhea in snv_51.
* Mon Sep 18 2006 - Brian.Cameron@sun.com
- Add SUNWhalh BuildRequires.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Mon Aug 14 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWhal after check-deps.pl run.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Thu Jul 25 2006 - brian.cameron@sun.com
- Add gnome-volume-manager and gnome-mount for HAL integration.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu Jun  1 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Jan 09 2006 - damien.carbery@sun.com
- Delete mime dir structure.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Thu Jul 28 2005 - damien.carbery@sun.com
- Add SUNWlibrsvg-devel build dependency. Add SUNWlibrsvg runtime dependency.
* Thu Jun 02 2005 - brian.cameron
- Bumped to 2.10, fixed packaging.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added nautlius-file-management-properties.1 manpage
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Tue Jul 27 2004 - damien.carbery@sun.com
- Add SUNWgnome-component-devel as BuildRequires, for ORBit-2.0.
* Sat Jun 26 2004 - shirley.woo@sun.com
- Changed install location to /usr/...
* Mon Jun 07 2004 - brian.cameron@sun.com
- Added SUNWlibexif dependency, then removed it since it is alrady
  a dependency of SUNWgnome-libs.
* Wed Jun 02 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Thu May 20 2004 - brian.cameron@sun.com
- Added man page to share package.
* Thu May 13 2004 - brian.cameron@sun.com
- Removed %{_libdir}/nautilus-*-helper from packages since Glynn
  removed these files that were added via ext-sources on May 5th.
* Fri Apr 30 2004 - niall.power@sun.com
- adjust %files for new nautilus version
* Fri Mar 26 2004 - laca@sun.com
- fix %files for libexecdir change
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 01 2004 - laca@sun.com
- remove dependencies on SUNWgnome-libs-root and -share
* Thu Feb 26 2004 - niall.power@sun.com
- remove clashing (and empty gconf.xml files) after schema installation
- add "-R%{_libdir}" to LDFLAGS
- define PERL5LIB for XML::Parser
- add a defattr for %package devel
* Mon Feb 23 2004 - niall.power@sun.com
- install gconf schemas at the end of the install stage
* Wed Feb 18 2004 - niall.power@sun.com
- removed gnome-desktop as it's provided by the panel pkgs now.
- removed rsvg man pages from file maps + tidy up
- removed unnecessary exported CFLAGS
* Wed Feb 18 2004 - laca@sun.com
- moved librsvg to SUNWgnome-libs as it is required by other modules as well
* Mon Feb 16 2004 - niall.power@sun.com
- initial spec file created

