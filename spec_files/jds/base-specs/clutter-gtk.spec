#
# spec file for package clutter-gtk
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Summary:      clutter-gtk - GTK+ integration library for clutter
Name:         clutter-gtk
Version:      0.8.3
Release:      1
License:      GPL
Group:        System/Libraries
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:	  http://www.clutter-project.org/sources/clutter-gtk/0.8/clutter-gtk-%{version}.tar.bz2
URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n clutter-gtk-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
./configure --prefix=%{_prefix}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*


%changelog
* Mon Feb 23 2009  chris.wang@sun.com
- Bump to 0.8.3 version
* Tue Jul  1 2008  chris.wang@sun.com
- Initial build.


