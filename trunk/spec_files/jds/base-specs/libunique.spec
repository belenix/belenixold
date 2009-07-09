#
# spec file for package unique
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:           libunique
License:        LGPL v2.1
Group:          System/Libraries
Version:        1.0.8
Release:        1	
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:        A library for writing single instance applications
Source:         http://download.gnome.org/sources/%{name}/1.0/%{name}-%{version}.tar.bz2
URL:            http://live.gnome.org/LibUnique
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:on
Prereq:        /sbin/ldconfig

%define gtk2_version 2.4.0
%define pkgconfig_version 0.15.0
%define gtk_doc_version 1.1

Requires: gtk2 >= %{gtk2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}

%description
LibUnique is a library for writing single instance applications, that is
applications that are run once and every further call to the same binary
either exits immediately or sends a command to the running instance.

LibUnique can be compiled against various backends, to allow the usage of
different IPC mechanisms depending on the platform.

%package devel
Summary:        unique development headers
Group:          Development/Libraries

%description devel
unique development headers

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
aclocal $ACLOCAL_FLAGS  -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir}         \
            %{gtk_doc_option}           \
%if %debug_build
            --enable-debug=yes          \
%else
            --enable-debug=no           \
%endif

# FIXME: hack: stop the build from looping
touch po/stamp-it

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
#Clean up unpackaged files
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/unique/*

%changelog
* Sat Mar 28 2009 - halton.huo@sun.com
- Bump to 1.0.8
- Remove upstreamed patch gcc-warn-flags.diff
* Sat Jan 24 2009 - halton.huo@sun.com
- Initial package
