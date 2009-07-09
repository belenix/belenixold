#
# spec file for package SUNWgnome-pilot
#
# includes module(s): gnome-pilot
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc
%define makeinstall make install
%use gpilot = gnome-pilot.spec

Name:          SUNWgnome-pilot
Summary:       PalmPilot link utilities
Version:       %{gpilot.version}
Source:        %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:  %{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-panel
Requires:      SUNWgnome-base-libs
Requires:      SUNWgnome-libs
%if %option_without_fox
Requires:      SUNWxwrtl
# SUNWxwplt and SUNWxwice contain the libSM.so.6 and libICE.so.6 libraries while
# SUNWxwrtl contains symlinks pointing to these. ldd points to the symlinks.
Requires:      SUNWxwplt
Requires:      SUNWxwice
%endif
Requires:      SUNWlxml
Requires:      SUNWzlib
Requires:      SUNWlibpopt
Requires:      SUNWmlib
Requires:      SUNWlibms
Requires:      SUNWlibmsr
Requires:      SUNWgnome-component
Requires:      SUNWgnome-config
Requires:      SUNWgnome-vfs
Requires:      SUNWdesktop-cache
Requires:      SUNWpilot-link
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWpilot-link-devel
BuildConflicts:	SUNWgnome-pilot-link
BuildConflicts:	SUNWgnome-pilot-link-root
BuildConflicts:	SUNWgnome-pilot-link-share
BuildConflicts:	SUNWgnome-pilot-link-devel
BuildConflicts:	SUNWgnome-pilot-link-devel-share

%if %build_l10n
%package l10n
Summary:       %{summary} - l10n files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}
%endif

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gpilot.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export LDFLAGS="%_ldflags"
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags" 
export RPM_OPT_FLAGS="$CFLAGS"
%gpilot.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gpilot.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
rm -rf $RPM_BUILD_ROOT%{_bindir}/gnome-pilot-*
rm -rf $RPM_BUILD_ROOT%{_bindir}/gpilotd-session-*
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
# rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
# rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/gnome-pilot-??*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):supported" $RPM_BUILD_ROOT}

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
%{_libdir}/bonobo
%{_libdir}/gnome-pilot/conduits/lib*.so
%{_libexecdir}/gpilotd
%{_libexecdir}/gpilot-applet
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-pilot
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-pilot/C
%{_datadir}/omf/gnome-pilot/*-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc -d gnome-pilot-%{gpilot.version} AUTHORS
%doc(bzip2) -d gnome-pilot-%{gpilot.version} COPYING NEWS 
%doc(bzip2) -d gnome-pilot-%{gpilot.version} ChangeLog README
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/idl

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/pilot.schemas

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Sep 17 2008 - jijun.yu@sun.com
- Add copyright related files per new process.
* Thu May 22 2008 - jijun.yu@sun.com
- Remove 2 comment mark.
* Fri Apr 18 2008 - jijun.yu@sun.com
- Add a patch to fix bug 6690026 and 6668371.
* Thu Apr 17 2008 - matt.keenan@sun.com
- Remove delivery of gpilot-applet.desktop Bug:6690026
* Mon Mar 31 2008 - jijun.yu@sun.com
- add copyright
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Nov 22 2007 - jijun.yu@sun.com
- Remove some unuseful files from the package.
* Sun Oct  7 2007 - laca@sun.com
- omit Nevada X deps if built --with-fox
* Wed Oct  3 2007 - laca@sun.com
- delete unneeded env vars, set LDFLAGS to %_ldflags
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Thu Jan 04 2007 - Jijun.yu@sun.com
- Update to new version 2.0.15
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Wed Jun 28 2006 - halton.huo@sun.com
- Remove Build/Requires SUNWgob.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu Jan 08 2006 - halton.huo@sun.com
- Change dependency from SUNWgob2 to SUNWgob.
* Tue Jun 06 2006 - halton.huo@sun.com
- Add build depend SUNWgob2.
* Fri Jun  2 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Thu Jun 01 2006 - damien.carbery@sun.com
- Remove SUNWlibmr dependency. It was a typo when fixing 6380655. This removal 
  fixes 6432832.
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
- Merge -share pkg(s) into the base pkg(s).
* Mon Mar 20 2006 - glynn.foster@sun.com
- Install capplet into the correct location.
* Fri Feb  3 2006 - damien.carbery@sun.com
- Add multiple Build/Requires to fix 6380655.
* Tue Jan 10 2006 - halton.huo@sun.com
- Inherited from SUNWgnome-pilot-link(tag=cinnabar-solaris)
  to replace SUNWgnome-pilot-link.spec.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Mon Sep 12 2005 - laca@sun.com
- Add missing dir to %files
* Tue Jul 12 2005 - damien.carbery@sun.com
- Disable inclusion of some l10n files as they are not yet available.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004  matt.keenan@sun.com
- Added gpilot-install-file.1, gpilotd-control-applet.1 manpages
* Thu Aug 26 2004  damien.carbery@sun.com
- Minor mod to how omf files specified in l10n package so C locale version is
  not included as it is already in the -share package.
* Wed Aug 25 2004  Kazuhiko.Maekawa@sun.com
- Added l10n help entry in l10 pkg
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Tue Mar 16 2004 - <laca@sun.com>
- initial version created
