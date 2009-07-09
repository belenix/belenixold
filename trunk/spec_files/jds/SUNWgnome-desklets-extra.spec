#
# spec file for package SUNWgnome-desklets-extra
#
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#


%include Solaris.inc
%use gd_calendar = gdesklets-calendar.spec
%use gd_clock = gdesklets-clock.spec
%use gd_worldtime = gdesklets-worldtime.spec

Name:                    SUNWgnome-desklets-extra
Summary:                 Supplied Gnome desktop widgets
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Requires: SUNWgnome-desklets
Requires: SUNWgnome-desktop-prefs
Requires: SUNWgnome-libs
Requires: SUNWdesktop-cache
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SUNWgnome-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version

%build
# we just get the bits tarball from developer

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdesklets/Controls
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdesklets/Displays
%gd_calendar.install -d %name-%version
%gd_clock.install -d %name-%version
%gd_worldtime.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gdesklets
%{_datadir}/gdesklets/*

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Jul 16 2008 - damien.carbery@sun.com
- Add rm/mkdir to %prep because build requires that the dir exists.
* Tue Jul 15 2008 - damien.carbery@sun.com
- Break gdesklets-extra.spec into three spec files (one for each desklet).
  Change this file to use each of the spec files.
* Thu Feb  8 2007 - damien.carbery@sun.com
- Update dependency list for files used in %post and during build.
* Mon Feb  5 2007 - damien.carbery@sun.com
- Add %prep section to create dir in BUILD dir.
* Thu Jan 29 2007 - <chris.wang@sun.com>
- initial creation


