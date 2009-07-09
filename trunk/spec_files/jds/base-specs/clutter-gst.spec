#
# spec file for package clutter-gst
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Summary:      clutter-gst - clutter-gst - gstreamer integration library for clutter
Name:         clutter-gst
Version:      0.8.0
Release:      1
License:      LGPL
Group:        System/Libraries
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:	  http://www.clutter-project.org/sources/clutter-gst/0.8/clutter-gst-%{version}.tar.bz2
URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n clutter-gst-%version

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
* Tue Jul  1 2008  chris.wang@sun.com
- Initial build.


