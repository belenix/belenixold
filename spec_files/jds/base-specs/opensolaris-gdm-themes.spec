#
# spec file for package opensolaris-gdm-themes
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
# bugdb: defect.opensolaris.org/bz
#
Name:			opensolaris-gdm-themes
License:		LGPL
Group:			System/GUI/GNOME
BuildArchitectures:	noarch
Version:		0.9
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		OpenSolaris login manager theme
Source:			http://dlc.sun.com/osol/jds/downloads/extras/opensolaris-branding/%{name}-%{version}.tar.gz
%if %build_l10n
Source1:		l10n-configure.sh
%endif
URL:			http://www.opensolaris.org/os/project/jds/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%define intltool_version 0.25

BuildRequires:  intltool >= %{intltool_version}

%description
This package contains OpenSolaris login manager [GDM] themes 

%prep
%setup -q -n %name-%version
%if %build_l10n
touch po/LINGUAS
sh -x %SOURCE1 --enable-sun-linguas
%endif

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

intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=/var/lib
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr (-, root, root)
%{_datadir}/gdm/themes/*

%changelog
* Fri Aug 29 2008 - jedy.wang@suncom
- Bump to 0.6.
* Wed Aug 27 2008 - jedy.wang@suncom
- Bump to 0.5.
* Mon Apr 21 2008 - takao.fujiwara@suncom
- Add opensolaris-gdm-themes-01-g11n-passwd-len.diff to adjust password len.
- Add sun-gdm-themes-02-g11n-po.diff
  Fixes opensolaris #1311.
* Wed Jan 23 2007 - glynn.foster@sun.com
- Bump to 0.2
* Sun Oct 21 2007 - glynn.foster@sun.com
- Intial version of opensolaris-gdm-themes
