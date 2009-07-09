#
# spec file for package gdesklets-calendar
#
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#


Name:           gdesklets-calendar
Summary:        GNOME desklets extra package
Version:        0.66
Release:        1
License:	GPL
Group:		Applications/Internet
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Useful desklets
Source:         http://www.gdesklets.de/files/desklets/Calendar/Calendar-%{version}.tar.gz
URL:		http://www.gdesklets.de/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Autoreqprov:	on

%prep


%build
# we just get the bits tarball from developer

%install
cd $RPM_BUILD_ROOT%{_datadir}/gdesklets/Displays
/usr/sfw/bin/gtar -zxf %{SOURCE0}

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Mon Apr 27 2009 - chris.wang@sun.com
- bump to 0.66
* Tue Feb 3  2009 - <chris.wang@sun.com>
- Change Calendar/gfx/months/README file attribute to 644
* Fri Jun 1  2007 - <xusheng.hou@sun.com>
- Point the URL to the new tarball for WorldTime and Clock desklets in official website
- Upgrade Calendar to 0.41
* Fri May 4  2007 - <xusheng.hou@sun.com>
- Upgrade calendar to 0.4
* Mon Apr 9  2007 - <chris.wang@sun.com>
- Remove all buggy desklets, since we will not support them
* Fri Feb 16 2007 - <chris.wang@sun.com>
- Add patch to fix bugs on WeeklyCalendar, Sidecandy CPU SideCandy network 
* Thu Jan 29 2007 - <chris.wang@sun.com>
- initial creation


