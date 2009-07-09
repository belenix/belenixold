#
# spec file for package libpng12
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:         libpng10
License:      other
Group:        System/Libraries
Version:      1.2.35
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Portable Network Graphics library
Source:       %{sf_download}/sourceforge/libpng/libpng-%{version}.tar.bz2
URL:          http://www.libpng.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
libpng is a C library for working with PNG (Portable Network Graphics) format
images.

%package devel
Summary: Headers for developing programs that will use libpng
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libpng

%prep
%setup -q -n libpng-%{version}

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

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure \
	--prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --bindir=%{_bindir} \
	--sysconfdir=%{_sysconfdir} \
        --with-esd-prefix=%{_prefix} \
	--mandir=%{_mandir}
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# delete libtool .la files and static libs
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig
%{_bindir}/*-config
%{_mandir}/*

%changelog
* Sun Mar 22 2009 - laca@sun.com
- bump to 1.2.35
* Thu May 17 2007 - laca@sun.com
- Create
