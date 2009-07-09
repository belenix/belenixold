#
# spec file for package startup-notification
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         startup-notification
License:      LGPL
Group:        System/Libraries
Version:      0.9
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Startup Notification Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/startup-notification/0.9/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%description
The startup-notification library contains a reference implementation of the startup notification
protocol, as defined on http://www.freedesktop.org.

%package devel
Summary:      Startup Notification Development Library
Group:        Development/Libraries

%description devel
The startup-notification library contains a reference implementation of the startup notification
protocol, as defined on http://www.freedesktop.org.

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

CFLAGS="$RPM_OPT_FLAGS "			\
./configure --prefix=%{_prefix}			\
            --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
make check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/libstartup-notification*so.*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libstartup-notification*so
%{_includedir}/startup-notification-1.0/*

%changelog
* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.

* Mon Mar 20 2007 - damien.carbery@sun.com
- Bump to 0.9. Remove upstream patch, 01-__FUNCTION__.

* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 0.8

* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Sun Feb 15 2004 - <laca@sun.com>
- add patch to change __FUNCTION__ to __func__ for Forte compatibility

* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la

* Thu May 13 2003 - ghee.teo@Sun.COM
- Created new spec file for startup-notification

