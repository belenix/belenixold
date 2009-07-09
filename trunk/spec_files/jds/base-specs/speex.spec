#
# spec file for package speex
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: https://trac.xiph.org/
#
Name:         speex
License:      Xiph.org BSD-style
Group:        Application/Devel
%define tarball_version 1.2rc1
Version:      1.2rc1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An open-source, patent-free speech codec
Source:       http://downloads.us.xiph.org/releases/%{name}/%{name}-%{tarball_version}.tar.gz
# date:2009-02-19 type:branding owner:mattman
Patch1:		  speex-01-manpages.diff
URL:          http://speex.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package devel
Summary:	Speex development files
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Speex development files.

%prep
%setup -q -n %{name}-%{tarball_version}
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
./configure --enable-shared     \
            --enable-static     \
            --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir}

make

%install
make DESTDIR=$RPM_BUILD_ROOT install

#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING AUTHORS ChangeLog NEWS README
%{_datadir}/doc/*
%{_datadir}/man/man1/speexenc.1*
%{_datadir}/man/man1/speexdec.1*
%attr(755,root,root) %{_bindir}/speex*
%attr(755,root,root) %{_libdir}/libspeex*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/speex/speex*.h
%{_datadir}/aclocal/speex.m4
%{_libdir}/pkgconfig/speex.pc

%changelog
* Thu Feb 19 2009 - matt.keenan@sun.com
- Add manpages patch for attributes and ARC comment

* Fri Dec 05 2008 - jijun.yu@sun.com
- Bump to 1.2rc1

* Tue Apr 29 2008 - brian.cameron@usn.com
- Bump to 1.2beta3.2

* Tue Dec 11 2007 - brian.cameron@sun.com
- Bump to 1.2beta3.

* Wed Nov 07 2007 - brian.cameron@sun.com
- Bump to 1.2beta2.

* Thu May 17 2007 - damien.carbery@sun.com
- Use a numeric version number. 'beta' is not permitted by WOS integration
  scripts.

* Fri Dec 01 2006 - damien.carbery@sun.com
- Bump to 1.2beta1. Remove obsolete patch, 01-empty-struct.

* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 1.1.12. Add patch, 01-empty-struct, to fix empty struct build error.

* Wed Jan 04 2006 - damien.carbery@sun.com
- Single threaded make because of timing issues.

* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 1.1.11.1.

* Tue Aug 23 2005 - damien.carbery@sun.com
- Remove an incorrect line from %files.

* Mon Aug 16 2005 - damien.carbery@sun.com
- Bump to 1.1.10.

* Tue Aug 02 2005 - balamurali.viswanathan@wipro.com
- Change copyright to license

* Tue Jul 26 2005 - balamurali.viswanathan@wipro.com
- Fix defattr for files and files devel

* Thu Jul 21 2005 - balamurali.viswanathan@wipro.com
- Remove *.a and *.la files. Fix typo. Add proper configure arguments

* Wed Jul 20 2005 - balamurali.viswanathan@wipro.com
- Initial spec file checkin
