#
# spec file for package libmusicbrainz
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# Bugdb: http://bugs.musicbrainz.org/ticket/
#
Name:         libmusicbrainz
License:      LGPL v2.1, GPL v2, Public Domain
Group:        System Environment/Libraries
Version:      3.0.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Software library for accessing MusicBrainz servers
Source:       http://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz 
URL:          http://musicbrainz.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD-ROMs.

%package devel
Summary: Headers for developing programs that will use libmusicbrainz
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libmusicbrainz.

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

%ifos linux
CFLAGS="$RPM_OPT_FLAGS" \
%else
CFLAGS="$RPM_OPT_FLAGS -I/usr/sfw/include" \
%endif
%if %debug_build
%define build_type Debug
%else
%define build_type Release
%endif

cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=%{build_type} \
                -DBUILD_SHARED_LIBS=On -DLIB_INSTALL_DIR=%{_libdir} .

make -j $CPUS
make docs

%install
make install DESTDIR=$RPM_BUILD_ROOT

#Clean up unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/musicbrainz
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmusicbrainz.pc

%changelog
* Mon May 14 2006 - damien.carbery@sun.com
- Bump to 2.1.5. Remove upstream patch, 01-fixduration.
* Mon Jan 22 2006 - brian.cameron@sun.com
- Add patch comments.
* Thu Nov 30 2006 - brian.cameron@sun.com
- Bump to 2.1.4.
* Fri Jul 21 2006 - brian.cameron@sun.com
- Add patch to fix calculation of track durations on Solaris.
* Tue Jul 11 2006 - brian.cameron@sun.com
- Bump to 2.1.3.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Specify include dir in CFLAGS so configure finds expat files. And lists the
  dir in Makefiles.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.1.2.
* Mon Jul 25 2005 - balamurali.viswanathan@wipro.com
- Change the name of the spec file to libmusicbrainz.spec
* Wed Jun 15 2005 - balamurali.viswanathan@wipro.com
- Initial spec file checkin
