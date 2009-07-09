#
# spec file for package gnome-common
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			gnome-common
License:		GPL
Group:			System/Libraries
BuildArchitectures:	noarch
Version:		2.26.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Multiply used files used by the GNOME 2.0 platform
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%description
gnome-common includes files used by pretty much every GNOME 2.0 application.

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

CFLAGS="$RPM_OPT_FLAGS" ./configure $MYARCH_FLAGS \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make prefix=$RPM_BUILD_ROOT%{_prefix} sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/gnome-common
%{_datadir}/aclocal

%changelog
* Mon Mar 23 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Sat Sep 27 2007 - christian.kelly@sun.com
- Bump to 2.24.0.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Mon Sep 26 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Tue Sep 06 2005 - brian.cameron@sun.com
- Add patch 1 from gnome-common CVS head to fix problem with grep
  not working the same way on Solaris as it does on Linux.

* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.0.

* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.8.0

* Thu Jan 27 2005 - brian.cameron@sun.com
- added patch 2 to fix autogen.sh so it works with Solaris find.

* Wed Jan 04 2005 - alvaro.lopez@sun.com
- added patch 1 to fix bug #6206322

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed Feb 18 2004 - matt.keenan@sun.com
- Distro to Cinnabar

* Tue Oct 21 2003 - glynn.foster@sun.com
- Remove the games m4 macro patch, since we're
  moving to 2.4

* Fri Oct 10 2003 - laca@sun.com
- include %_datadir/gnome-common
- use _datadir instead of _prefix/share

* Mon Oct 06 2003 - ghee.teo@sun.com
- Updated 2.4 tarball for Quicksilver.

* Tue Jul 08 2003 - glynn.foster@sun.com
- Add in some gnome-games m4 macros

* Thu May 13 2003 - ghee.teo@Sun.COM
- Initial Sun Release

