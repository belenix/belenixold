#
# spec file for package sun-backgrounds
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:			sun-backgrounds
License:		GPL
Group:			System/GUI/GNOME
Version:		0.1
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Selection of backgrounds for the Solaris desktop
Source:			http://dlc.sun.com/osol/jds/downloads/extras/%{name}-%{version}.tar.bz2
URL:			http://www.sun.com
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildArchitectures:     noarch
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

Requires:	glib2
BuildRequires:  intltool
BuildRequires:  glib2

%description
Selection of backgrounds for the Solaris desktop.

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
%{_datadir}/gnome-background-properties
%{_datadir}/pixmaps/backgrounds/
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Mon Jan 21 2008 - glynn.foster@sun.com
- Initial version
