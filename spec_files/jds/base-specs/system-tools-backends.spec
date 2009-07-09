#
# spec file for package system-tools-backends
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
Name:		system-tools-backends
License:	GPL
Group:		System/GUI/GNOME
# WARNING: Do NOT bump version as other dependencies (e.g DBUS) need work first.
Version:	1.4.2
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Backends for the GNOME System Tools
Source:		http://ftp.gnome.org/pub/GNOME/sources/system-tools-backends/1.4/%{name}-%{version}.tar.bz2
# date:2006-03-15 owner:padraig type:feature
Patch1:		system-tools-backends-01-boot.diff
# date:2006-03-16 owner:padraig type:feature
Patch2:		system-tools-backends-02-common.diff
# date:2006-03-16 owner:padraig type:feature
Patch3:		system-tools-backends-03-disks.diff
# date:2006-03-16 owner:padraig type:feature
Patch4:		system-tools-backends-04-network.diff
# date:2006-03-16 owner:padraig type:feature
Patch5:		system-tools-backends-05-services.diff
# date:2006-03-16 owner:padraig type:feature
Patch6:		system-tools-backends-06-shares.diff
# date:2006-03-16 owner:padraig type:feature
Patch7:		system-tools-backends-07-time.diff
# date:2006-03-16 owner:padraig type:feature
Patch8:		system-tools-backends-08-users.diff
# date:2006-07-05 owner:mattman type:feature
Patch9:		system-tools-backends-09-grub-path.diff
URL:		http://www.gnome.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/%{name}
Autoreqprov:	on

%define glib2_version 2.3.0

Requires:	glib2 >= %{glib2_version}
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  intltool

%description
The System Tools Backends are a set of cross-platform scripts for Linux and 
other Unix systems. The backends provide an standard XML interface for 
modifying the configuration regarless of the distribution that's being used.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1


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

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir}
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_libdir}/pkgconfig/
%{_datadir}/setup-tool-backends/
%{_datadir}/aclocal/
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Wed Aug 30 2006 - darren.kenny@sun.com
- Remove boot stuff, no longer supporting it.

* Wed Jul 05 2006 - matt.keenan@sun.com
- Add patch for location of sungrub for boot-conf to work.

* Thu Mar 16 2006 - damien.carbery@sun.com
- Move patches here from Solaris package spec file.

* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 1.4.2

* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 1.3.92.

* Mon Aug 16 2005 - damien.carbery@sun.com
- Bump to 1.3.2.

* Tue May 24 2005 - glynn.foster@sun.com
- Initial spec
