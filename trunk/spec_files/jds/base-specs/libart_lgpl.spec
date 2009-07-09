#
# spec file for package libart_lgpl
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:			libart_lgpl
License:		LGPL
Group:			System/Libraries/GNOME
Version:		2.3.20
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Libart is a library for high-performace 2D graphics
Source:			http://ftp.gnome.org/pub/GNOME/sources/libart_lgpl/2.3/libart_lgpl-%{version}.tar.bz2
URL:			http://www.levien.com/libart
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:			/sbin/ldconfig

%description
Libart is a library for high-performace 2d graphics. It
is currently being used as the anti-aliased rendering
engine for the GNOME Canvas.


%package devel
Summary:		Libart is a library for high-performace 2D graphics
Group:			System/Libraries/GNOME
Requires:		%{name} = %{version}

%description devel
Libart is a library for high-performace 2d graphics. It
is currently being used as the anti-aliased rendering
engine for the GNOME Canvas.

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
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"	\
./configure --prefix=%{_prefix}
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/libart2-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libart-2.0
%{_mandir}/man3/*

%changelog
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.3.20.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.3.19.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.3.17
* Tue Aug 24 2004 - laca@sun.com
- Added libart2-config back
* Fri Aug 20 2004 - niall.power@sun.com
- packaging fixes for rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Feb 20 2004 - <matt.keenan@sun.com>
- Update Distro
* Fri Feb 06 2004 - <niall.power@sun.com>
- small patch typo: missing "-"p1
* Fri Feb 06 2004 - <niall.power@sun.com>
- add patch for -uninstalled pkgconfig file
- autotoolize
* Fri Oct 06 2003 - <ghee.teo@sun.com>
- Created Quicksilver build.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Sun Jul 26 2003 - <markmc@sun.com> 2.3.13
- Initial spec file
