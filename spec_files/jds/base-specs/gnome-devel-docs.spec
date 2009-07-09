#
# spec file for package gnome-devel-docs
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#

Name:		        gnome-devel-docs
License:		GPL
Group:			Documentation
BuildArchitectures:	noarch
Version:		2.26.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		documents targeted for GNOME developers
Source:		        http://ftp.gnome.org/pub/gnome/sources/gnome-devel-docs/2.26/gnome-devel-docs-%{version}.tar.bz2
URL:			http://live.gnome.org/DeveloperGuides
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc

%define			scrollkeeper_version 0.3.12

Prereq:			scrollkeeper >= %{scrollkeeper_version}
Requires:		scrollkeeper >= %{scrollkeeper_version}

%description
This package contains documents which will be packaged together and
shipped as gnome-devel-docs in the GNOME Fifth Toe distribution.  They 
should be documents targeted for GNOME developers.

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

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}   \
            --datadir=%{_datadir} \
	    --disable-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod -R a+rX $RPM_BUILD_ROOT%{_datadir}/gnome/help

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "2" ] ; then # upgrade
  if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update -q; fi
fi

%files
%defattr(-,root,bin)
%doc COPYING AUTHORS README ChangeLog NEWS INSTALL
%{_datadir}/gnome/help/*
%{_datadir}/omf/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.

* Tue Sep 09 2008 - patrick.ale@gmail.com
- Correct download URL

* Thu Sep 04 2008 - christian.kelly@sun.com
- Bump to 2.23.1.

* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Sat Sep 01 2007 - Dave Lin <dave.lin@sun.com>
- initial version

