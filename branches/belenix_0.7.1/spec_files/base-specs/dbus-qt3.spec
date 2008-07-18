#
# spec file for package dbus-glib
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
Name:         dbus-qt3
License:      GPL/AFL
Group:        System/Libraries
Version:      0.62
Release:      1
Distribution: BeleniX
Vendor:       BeleniX
Summary:      Qt-style interface for D-Bus
Source:       http://ftp.de.debian.org/debian/pool/main/d/dbus-qt3/dbus-qt3_0.62.git.20060814.orig.tar.gz
URL:          http://packages.debian.org/source/etch/dbus-qt3
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

%define glib2_version 2.6.4
%define libxml2_version 2.6.19
BuildRequires: glib2-devel >= %glib2_version
BuildRequires: libxml2-devel >= %libxml2_version
# FIXME: get python rpm: BuildRequires: python >= %python_version
Requires: glib2 >= %glib2_version
Requires: libxml2 >= %libxml2_version

%description
Qt-style interface for D-Bus.

%package devel
Summary:      Simple IPC library based on messages
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
Qt-style interface for D-Bus.

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

aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
export CFLAGS="%optflags -D_REENTRANT -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix}			\
            --includedir=%{_includedir}		\
            --sysconfdir=%{_sysconfdir}		\
            --libdir=%{_libdir}			\
            --bindir=%{_bindir}			\
            --localstatedir=%{_localstatedir}	\
            --mandir=%{_mandir}			\
            --datadir=%{_datadir}		\
            --disable-static

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%{_sysconfdir}
%config %{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/libdbus*.so*
%{_datadir}/man/*
%{_datadir}/dbus-1/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/dbus-1.0/*
%{_libdir}/dbus-1.0/*
%{_libdir}/pkgconfig/*

%changelog
* Wed Nov 07 2007 - damien.carbery@sun.com
- Add -D_REENTRANT to CFLAGS. It was removed during conversion to new style
  multi-ISA build. Fixes 6615221.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 0.74.
* Sun Apr  1 2007 - laca@sun.com
- add missing aclocal calls
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed CC64 and CC32. They are not needed anymore
* Sun Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
* Wed Feb 14 2007 - damien.carbery@sun.com
- Bump to 0.73. Remove upstream patch 01-uninstalled-pc. Rename remainder.
* Thu Nov 27 2006 - brian.cameron@sun.com
- Created.
