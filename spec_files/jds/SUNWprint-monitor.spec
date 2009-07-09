#
# spec file for package SUNWprint-monitor
#
# includes module(s): ospm
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

%use ospm = ospm.spec

Name:               SUNWprint-monitor
Summary:            Print Monitor
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
SUNW_Copyright:     %{name}.copyright
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
Source:             %{name}-exec_attr
Source1:            %{name}-manpages-0.1.tar.gz

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWzlib
Requires: SUNWdesktop-cache
Requires: SUNWgnome-panel
Requires: %{name}-root
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-xml-root
BuildRequires: SUNWgnome-xml-share

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
%ospm.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%ospm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%ospm.install -d %name-%version
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security
install --mode=0644 %SOURCE $RPM_BUILD_ROOT%{_sysconfdir}/security/exec_attr

#delete some unused or not shipped binaries.
rm -rf $RPM_BUILD_ROOT%{_bindir}/test-queues

#delete desktop files are they are now delived in SUNWpcu which uses a wrapper
#to share the same desktop files for lp and cups.
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc(bzip2) -d ospm-%{ospm.version} COPYING ChangeLog po/ChangeLog
%doc -d ospm-%{ospm.version} AUTHORS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ospm
%{_libdir}/ospm/lib*.so*
%{_libdir}/ospm/ospm-applet
%{_libdir}/ospm/lp-queue-exists-by-serial.sh
%attr (0755, root, bin) %{_libdir}/ospm/lp-queue-helper
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ospm
%{_datadir}/omf/ospm-pm/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/ospm-pm/C
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/ospm.schemas
%config %class(rbac) %attr (0644, root, sys) %{_sysconfdir}/security/exec_attr

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Dec 03 2008 - takao.fujiwara@sun.com
- Added BuildRequires of SUNWgnome-xml-root and SUNWgnome-xml-share
* Thu Nov 20 2008 - takao.fujiwara@sun.com
- Fixed pkgmap
* Wed Nov 05 2008 - halton.huo@sun.com
- Add po/ChangeLog to %files
* Thu Oct 30 2008 - evan.yan@sun.com
- Remove the hack of replacing testpages, since we've bumped new tar ball
* Thu Oct 30 2008 - halton.huo@sun.com
- Add non-C locale gnome help and omf to %files
* Wed Sep 10 2008 - halton.huo@sun.com
- Add %doc to %files
* Fri Sep 05 2008 - halton.huo@sun.com
- Fix %files attr conflict for new added help files
* Thu Sep 04 2008 - ghee.teo@sun.com
- Remove the delivery of desktop files as this is now delivered from SUNWpcu
  so that it can be shared by different print system.
* Thu Jul 24 2008 - halton.huo@sun.com
- Reflect change for version bump
* Wed May 07 2008 - damien.carbery@sun.com
- Remove PERL5LIB setting as it is not necessary.
* Thu Mar 27 2008 - halton.huo@sun.com
- Add copyright file
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete SUNWxwrtl dependency, twice...
* Tue Jul 10 2007 - halton.huo@sun.com
- Add man page for ospm-preferences.
* Mon May 21 2007 - ghe.teo@sun.com
- Renamed the spec file to SUNWprint-monitor.spec to match one pager.
* Thu May 17 2007 - ghee.teo@sun.com
- Added lp-queue-helper to exec_attr through the use of rbac class script
  Remove the need to make it setuid.
* Sat May 05 2007 - halton.huo@sun.com
- Remove not shipped binaries ospm-pm and test-queues
* Fri Apr 27 2007 - halton.huo@sun.com
- Initial spec file
