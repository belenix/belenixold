#
# spec file for package libIDL
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         libIDL
License:      LGPL
Group:        System/Libraries
Version:      0.8.13
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      IDL parsing library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libIDL/0.8/libIDL-%{version}.tar.bz2
URL:          http://www.gnome.org
Docdir:       %{_defaultdocdir}/doc
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
AutoReqProv:  on
Prereq:       /sbin/ldconfig

%define glib2_version 2.4.0
%define pkgconfig_version 0.15.0

Requires:      glib2 >= %{glib2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}

%description
libIDL is a small library for creating parse trees of CORBA v2.2
compliant Interface Definition Language (IDL) files, which is a
specification for defining interfaces which can be used between
different CORBA implementations.

%package devel
Summary:      IDL parsing library development libraries and header files.
Group:        Development/Languages/Other
Requires:     %{name} = %{version}
Requires:     glib2-devel >= %{glib2_version}

%description devel
libIDL is a small library for creating parse trees of CORBA v2.2
compliant Interface Definition Language (IDL) files, which is a
specification for defining interfaces which can be used between
different CORBA implementations.

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

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
           --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*
%{_infodir}/*.info.gz

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 0.8.13
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 0.8.12
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 0.8.11
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 0.8.10.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 0.8.9.
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Tue Mar 06 2005 - damien.carbery@sun.com
- Bump to 0.8.8.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.8.6.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 0.8.5
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jan 28 2004 - <laca@sun.com> 0.8.3-1
- Upgrade to 0.8.3
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Add back the man pages.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Fri Aug 01 2003 - <markmc@sun.com> 0.8.2-1
- Upgrade to 0.8.2
* Tue May 20 2003 - <Niall.Power@Sun.COM>
- initial Sun release
