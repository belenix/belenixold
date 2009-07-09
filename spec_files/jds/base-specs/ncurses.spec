#
# spec file for package ncurses
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: rickju
# bugdb :
#
Name:		ncurses
Version:	5.6
Release:  1
License:	MIT
Group:    System/Libraries
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:  A CRT screen handling and optimization package.
Source:   http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
# date:2008-09-12 owner:rickju type:branding
Patch0:			ncurses-01-widec.diff
URL:		  http://www.gnu.org/software/ncurses/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/ncurses
Autoreqprov:	on

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.

%package devel
Summary: The development files for applications which use ncurses.
Group:   Development/Libraries
Requires:     %name = %version
Autoreqprov:  on

%description devel
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

%prep
%setup -q
%patch0 -p1

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

CFLAGS="$RPM_OPT_FLAGS"			  \
./configure 				          \
	--prefix=%{_prefix} 		    \
	--sysconfdir=%{_sysconfdir} \
  --includedir=%{_includedir} \
  --datadir=%{_datadir}       \
  --with-normal   \
  --enable-rpath  \
  --with-shared   \
  --enable-widec  \
%if %debug_build
  --with-debug
%else
  --without-debug
%endif

make -j $CPUS
 
%install
make DESTDIR=$RPM_BUILD_ROOT install \
    SITEPREFIX=/dummy VENDORPREFIX=/dummy PERLPREFIX=/dummy
rm -rf $RPM_BUILD_ROOT/%{_prefix}/man

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_datadir}/terminfo/*
%{_datadir}/tabset/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.a
%{_includedir}/*.h

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Fri Sep 12 2008 - rick.ju@sun.com
- Add widechar support
* Mon Aug 18 2008 - rick.ju@sun.com
- use /usr/gnu as prefix
* Tue Jul 18 2008 - rick.ju@sun.com
- Initial spec file created.
