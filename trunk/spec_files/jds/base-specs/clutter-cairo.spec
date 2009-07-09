#
# spec file for package clutter-cairo
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Summary:      clutter-cairo - An experimental clutter cairo 'drawable' actor.
Name:         clutter-cairo
Version:      0.8.2
Release:      1
License:      LGPL
Group:        System/Libraries
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:       http://www.clutter-project.org/sources/clutter-cairo/0.8/clutter-cairo-%{version}.tar.bz2
URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n clutter-cairo-%version


%build
PUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%{optflags}"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags}"
./configure --prefix=%{_prefix}              \
            --libdir=%{_libdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static                 \

make -j$CPUS 
%install
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


