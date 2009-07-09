#
# spec file for package pkg-config
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			pkg-config
License:		GPL
Group:			System/Libraries
Version:		0.23
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Helper tool used when compiling applications and libraries.
Source:			http://pkgconfig.freedesktop.org/releases/%{name}-%{version}.tar.gz
# date:2004-06-06 owner:laca type:bug bugster:4809315
# upstreamable
Patch1:                 pkgconfig-01-suppress_gnome-config_error_msg.diff
URL:			http://pkgconfig.freedesktop.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%description
pkg-config is a helper tool used when compiling applications and libraries. It helps you insert the correct compiler options on the command line

%prep
%setup -q
%patch1 -p1

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
./configure --prefix=%{_prefix} --mandir=%{_mandir}
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files

%changelog
* Tue Jul 15 2008 - damien.carbery@sun.com
- Separate out from SUNWgnome-common-devel.spec.
