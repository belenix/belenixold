#
# spec file for package SUNWgnome-system-monitor
#
# includes module(s): gnome-system-monitor
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
%include Solaris.inc
%use gnomesystemmonitor = gnome-system-monitor.spec

Name:              SUNWgnome-system-monitor
Summary:           GNOME system monitor
Version:           %{default_pkg_version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build
Source:	           %{name}-manpages-0.1.tar.gz

%include default-depend.inc

Requires:                SUNWgnome-config
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-libs
Requires:                SUNWgnome-themes
Requires: 		 SUNWlibgtop
Requires: 		 SUNWgnome-panel
Requires: 		 SUNWperl-xml-parser
Requires:                SUNWlibC
Requires:                SUNWdesktop-cache
Requires:                %{name}-root
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-libs-devel
BuildRequires:           SUNWgnome-themes-devel
BuildRequires:           SUNWgnome-doc-utils
BuildRequires:           SUNWgnome-config-devel
BuildRequires: 		 SUNWlibgtop-devel
BuildRequires: 		 SUNWgnome-panel-devel
BuildRequires: 		 SUNWperl-xml-parser
BuildRequires: 		 SUNWglibmm-devel
BuildRequires: 		 SUNWgtkmm-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:        GNOME system monitor - platform dependent, / file system
SUNW_BaseDir:   /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%gnomesystemmonitor.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export CXXFLAGS="%cxx_optflags"
%if %cc_is_gcc
export CFLAGS=`echo ${CFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS=`echo ${CXXFLAGS} | sed 's/-features=extensions//'`
export CXXFLAGS="${CXXFLAGS} ${CXXFLAGS_EXTRA}"
export LDFLAGS="${LDFLAGS} ${LDFLAGS_EXTRA}"
%else
export CXX="${CXX} -norunpath"
%endif

%gnomesystemmonitor.build -d %name-%version

%install
%gnomesystemmonitor.install -d %name-%version

##rm -r $RPM_BUILD_ROOT%{_prefix}/var/scrollkeeper
#rm -r $RPM_BUILD_ROOT/var/lib/scrollkeeper
#rm -r $RPM_BUILD_ROOT/var

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gnome-system-monitor-%{gnomesystemmonitor.version} README AUTHORS
%doc(bzip2) -d gnome-system-monitor-%{gnomesystemmonitor.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/*/C
%dir %attr(0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/*/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/gnome-system-monitor/side.png
%{_datadir}/pixmaps/gnome-system-monitor/upload.svg
%{_datadir}/pixmaps/gnome-system-monitor/download.svg
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-system-monitor.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr(0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/help
%dir %attr(0755, root, bin) %{_datadir}/gnome/help/gnome-system-monitor
%{_datadir}/gnome/help/*/[a-z]*
%dir %attr(0755, root, bin) %{_datadir}/omf
%dir %attr(0755, root, bin) %{_datadir}/omf/gnome-system-monitor
%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 24 2009 - dave.lin@sun.com
- Add BuildRequires of SUNWglibmm-devel SUNWgtkmm-devel.
* Mon Mar 23 2009 - Niall Power <niall.power@sun.com>
- Take ownership of spec file
* Wed Sep 17 2008 - Henry Zhang <hua.zhang@sun.com>
- Add  %doc to %files for copyright
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu Oct 11 2007 - damien.carbery@sun.com
- Remove install dependency on SUNWgnome-doc-utils and change the build
  dependency from SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils.
* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of /var dirs as they are no longer installed.
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries
* Tue Apr 24 2007 - laca@sun.com
- use $BASEDIR instead of $PKG_INSTALL_ROOT to fix diskless install
  (CR 6537817)
* Tue Mar 06 2007 - damien.carbery@sun.com
- Add the omf files back to %files. Tweak %install and /var references.
* Wed Feb 14 2007 - damien.carbery@sun.com
- Remove omf files from %files as they aren't in the build! Remove reference
  to ${_prefix}/var too as it is not installed.
* Mon Feb  5 2007 - damien.carbery@sun.com
- Add Requires SUNWlibC after check-deps.pl run.
* Fri Jan 26 2007 - hua.zhang@sun.com
- Delete dependency on SUNWpcre/-devel
* Wed Jan 10 2007 - damien.carbery@sun.com
- Add to LDFLAGS so that libsocket and libnsl are linked against.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Add SUNWgnome-themes/-devel dependency for gnome-icon-theme module.
* Mon Dec 11 2006 - damien.carbery@sun.com
- Add SUNWpcre/-devel dependency.
* Wed Nov 22 2006 - damien.carbery@sun.com
- 2.17 update: Add SUNWgnome-libs/-devel dependency and add pixmaps to %files.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Aug 25 2006 - laca@sun.com
- make the postrun scripts use $BASEDIR instead of $PKG_INSTALL_ROOT so
  that it works during diskless client installation, part of CR6448317
* Mon Jul 31 2006 - damien.carbery@sun.com
- Remove 'devel' package definition as there is no matching %files section.
* Sun Jul 23 2006 - laca@sun.com
- fix gconf schemas installation and attributes
* Fri Jul 21 2006 - hua.zhang@sun.com
- Delete one sentence for gconf problem.
* Thu Jul 20 2006 - hua.zhang@sun.com
- Fix omf file bug
* Wed Jul 19 2006 - damien.carbery@sun.com
- Fix dir perms and merge share pkg into base pkg.
* Fri Apr 21 2006 - hua.zhang@sun.com
- Inital spec file
